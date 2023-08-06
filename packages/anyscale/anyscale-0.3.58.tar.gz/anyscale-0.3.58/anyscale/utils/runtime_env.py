import argparse
import asyncio
import copy
from enum import Enum
import hashlib
import io
import json
import logging
import os
from pathlib import Path
import pickle
import platform
import sys
import tarfile
import tempfile
from typing import Any, Dict, List, Optional, Tuple
from urllib.parse import urlparse
import uuid

import aiobotocore  # type: ignore
import conda_pack  # type: ignore
from filelock import FileLock
from ray.job_config import JobConfig
import yaml

from anyscale.util import get_wheel_url
import anyscale.utils.conda as ray_conda
from anyscale.utils.ray_utils import _dir_travel, _get_excludes  # type: ignore


logger = logging.getLogger(__name__)

SINGLE_FILE_MINIMAL = 25 * 1024 * 1024  # 25MB
DELTA_PKG_LIMIT = 100 * 1024 * 1024  # 100MB


DIR_META_FILE_NAME = ".anyscale_runtime_dir"

event_loop = asyncio.new_event_loop()

# TODO (yic): Use ray._private.runtime_env.PKG_DIR instead
# Right now, with client server manager, the tmp dir is not set properly
# PKG_DIR will be set after node is constructed
PKG_DIR = "/tmp/ray/session_latest/runtime_resources/"


class ResourceType(Enum):
    WORKING_DIR: str = "working_dir_"
    CONDA: str = "conda_"


class PackagePrefix(Enum):
    """Theses are prefix of different packages. Packages are composed by
        base + [add] - del ==> resource_dir
    """

    # Base package is the base part for the resource
    BASE_PREFIX: str = "base_"
    # Add package is what to add to for the resource.
    ADD_PREFIX: str = "add_"
    # Del package is what to be deleted after
    DEL_PREFIX: str = "del_"
    # Resoruce dir pkg is where to unpack the data
    RESOURCE_DIR_PREFIX: str = "resource_dir_"


def _gen_token() -> Any:
    import anyscale
    from anyscale.api import get_api_client
    from anyscale.credentials import load_credentials
    from anyscale.sdk.anyscale_client.sdk import AnyscaleSDK

    sdk = AnyscaleSDK(
        auth_token=load_credentials(), host=f"{anyscale.conf.ANYSCALE_HOST}/ext"
    )
    api_client = get_api_client()
    org_id = api_client.get_user_info_api_v2_userinfo_get().result.organization_ids[0]
    token = sdk.get_organization_temporary_object_storage_credentials(
        organization_id=org_id, region="default",
    ).result.s3
    logger.debug(f"S3: bucket({token.bucket}) path({token.path})")
    token.path = org_id + "/"
    return token


def _create_s3_client(session: aiobotocore.AioSession, token: Any):  # type: ignore
    return session.create_client(
        "s3",
        region_name=token.region,
        aws_access_key_id=token.aws_access_key_id,
        aws_secret_access_key=token.aws_secret_access_key,
        aws_session_token=token.aws_session_token,
    )


async def _get_object(  # type: ignore
    s3, bucket: str, key: str,
):
    obj = await s3.get_object(Bucket=bucket, Key=key)
    return obj["Body"]


async def _put_object(s3, bucket: str, key: str, local_path: str,) -> None:  # type: ignore
    await s3.put_object(Body=open(local_path, "rb"), Bucket=bucket, Key=key)


async def _object_exists(s3, bucket: str, key: str,) -> bool:  # type: ignore
    try:
        await s3.head_object(
            Bucket=bucket, Key=key,
        )
    except Exception:
        return False
    return True


def _object_exists_sync(token: Any, bucket: str, key: str) -> bool:
    async def helper(key: str,) -> bool:
        session = aiobotocore.get_session()
        async with _create_s3_client(session, token) as s3:
            exists = await _object_exists(s3, bucket, key)
            return exists

    return event_loop.run_until_complete(helper(key))


def _hash_file_contents(local_path: Path, hasher: "hashlib._Hash") -> "hashlib._Hash":
    if local_path.is_file():
        buf_size = 4096 * 1024
        with local_path.open("rb") as f:
            data = f.read(buf_size)
            while len(data) != 0:
                hasher.update(data)
                data = f.read(buf_size)
    return hasher


def _entry_hash(local_path: Path, tar_path: Path) -> bytes:
    """Calculate the hash of a path

    If it's a directory:
        dir_hash = hash(tar_path)
    If it's a file:
        file_hash = dir_hash + hash(file content)
    """
    hasher = hashlib.md5()
    hasher.update(str(tar_path).encode())
    return _hash_file_contents(local_path, hasher).digest()


def _xor_bytes(left: Optional[bytes], right: Optional[bytes]) -> Optional[bytes]:
    """Combine two hashes that are commutative.

    We are combining hashes of entries. With this function, the ordering of the
    entries combining doesn't matter which avoid creating huge list and sorting.
    """
    if left and right:
        return bytes(a ^ b for (a, b) in zip(left, right))
    return left or right


class _PkgURI(object):
    """This class represents an internal concept of URI.

    An URI is composed of: pkg_type + hash_val. pkg_type is an entry of
    PackagePrefix.

    For example, `add_<content_hash>` or `del_<content_hash>`.

    The purpose of this class is to make the manipulation of URIs easier.
    """

    @classmethod
    def from_uri(cls, pkg_uri: str) -> "_PkgURI":
        """Constructor of _PkgURI from URI."""
        uri = urlparse(pkg_uri)
        assert uri.scheme == "s3"
        name = uri.netloc
        resource_type = None
        pkg_type = None
        for r in ResourceType:
            if name.startswith(r.value):
                resource_type = r
                name = name[len(r.value) :]
                break
        assert resource_type is not None

        for p in PackagePrefix:
            if name.startswith(p.value):
                pkg_type = p
                name = name[len(p.value) :]
        assert pkg_type is not None
        hash_val = name
        assert len(hash_val) != 0
        return cls(resource_type, pkg_type, hash_val)

    def __init__(
        self, resource_type: ResourceType, pkg_type: PackagePrefix, hash_val: str
    ):
        """Constructor of _PkgURI."""
        self._resource_type = resource_type
        self._pkg_type = pkg_type
        self._hash_val = hash_val
        # Right now we only support s3. Hard code it here.
        self._scheme = "s3"

    def __eq__(self, other: Any) -> bool:
        if not isinstance(other, _PkgURI):
            return NotImplemented
        return (
            self._scheme == other._scheme
            and self._pkg_type == other._pkg_type
            and self._hash_val == other._hash_val
        )

    def uri(self) -> str:
        return self._scheme + "://" + self.name()

    def local_path(self) -> Path:
        return Path(PKG_DIR) / self.name()

    def resource_type(self) -> ResourceType:
        return self._resource_type

    def name(self) -> str:
        assert isinstance(self._pkg_type.value, str)
        assert isinstance(self._resource_type.value, str)
        return self._resource_type.value + self._pkg_type.value + self._hash_val

    def is_base_pkg(self) -> bool:
        return self._pkg_type == PackagePrefix.BASE_PREFIX

    def is_add_pkg(self) -> bool:
        return self._pkg_type == PackagePrefix.ADD_PREFIX

    def is_del_pkg(self) -> bool:
        return self._pkg_type == PackagePrefix.DEL_PREFIX

    def is_resource_dir_pkg(self) -> bool:
        return self._pkg_type == PackagePrefix.RESOURCE_DIR_PREFIX


class _Pkg:
    """Class represent a package.

    A package is composed by pkg_uri + contents."""

    def __init__(
        self,
        root_dir: Path,
        resource_type: ResourceType,
        pkg_type: PackagePrefix,
        hash_val: str,
        contents: Optional[List[Tuple[Path, bytes]]] = None,
    ):
        self._uri = _PkgURI(resource_type, pkg_type, hash_val)
        self._root_dir = root_dir
        if contents is None:
            contents = []
        self._contents = contents

    def __eq__(self, other: Any) -> bool:
        if not isinstance(other, _Pkg):
            return NotImplemented
        return (
            self._uri == other._uri
            and self._root_dir == other._root_dir
            and set(self._contents) == set(other._contents)
        )

    def create_tar_file(self) -> str:
        """Create a physical package.

        It'll to through contents and put every file into a tar file.
        This function will return the path to the physical package. The caller
        need to clean it up once finish using it.

        TODO (yic): Support steaming way to update the pkg.
        """
        empty_file = io.BytesIO()
        with tempfile.NamedTemporaryFile(delete=False) as f:
            with tarfile.open(fileobj=f, mode="w:") as tar:
                for (to_path, _) in self._contents:
                    file_path = self._root_dir / to_path
                    if self._uri.is_del_pkg():
                        info = tarfile.TarInfo(str(to_path))
                        info.size = 0
                        tar.addfile(info, empty_file)
                    else:
                        tar.add(file_path, to_path)
            return f.name

    def name(self) -> str:
        return self._uri.name()

    def uri(self) -> str:
        return self._uri.uri()

    def update_meta(self) -> None:
        """Persist the meta info into disk.

        This function is for base package only. It'll transform the contents
        into meta and writing to a disk file.
        """
        assert self._uri.is_base_pkg()
        files = {}
        for (to_path, hash_val) in self._contents:
            files[str(to_path)] = hash_val.hex()
        meta = {"hash_val": self._uri._hash_val, "files": files}
        with (self._root_dir / DIR_META_FILE_NAME).open("w") as meta_file:
            meta_file.write(json.dumps(meta))


def _read_dir_meta(
    work_dir: Path, _skip_check: bool = False
) -> Optional[Dict[str, Any]]:
    """Read meta from the meta file.

    Meta file is composed by json string. The structure of the file is like this:
    {
       "hash_val": "base_pkg_hash",
       "files": {
         "file1": "hash1",
         "file2": "hash2",
       }
    }
    """
    meta_file_path = work_dir / DIR_META_FILE_NAME
    if not meta_file_path.exists():
        return None
    meta_valid = True
    if not meta_file_path.is_file():
        meta_valid = False
    try:
        meta = json.loads(meta_file_path.read_text())
        if "hash_val" not in meta or "files" not in meta:
            meta_valid = False
    except Exception:
        meta_valid = False
        meta = None
    if not meta_valid or not isinstance(meta, dict):
        raise ValueError(
            f"Invalid meta file: f{meta_file_path}. This should be a"
            "file managed by anyscale. The content of the file is broken."
            "Please consider delete/move it and retry"
        )
    if _skip_check:
        return meta
    pkg_uri = _PkgURI(
        ResourceType.WORKING_DIR, PackagePrefix.BASE_PREFIX, meta["hash_val"]
    )
    try:
        token = _gen_token()
        if _object_exists_sync(token, token.bucket, token.path + pkg_uri.name()):
            logger.debug("Base meta exists in s3")
            # For mypy warning. It will raise exception before.
            assert isinstance(meta, dict)
            return meta
        else:
            return None
    except Exception:
        logger.error("Failed to check the meta existence. Treat it as not existing")
        return None


def _get_base_pkg_from_meta(working_dir: Path, meta: Dict[str, Any]) -> _Pkg:
    files = []
    for (f, h) in meta["files"].items():
        files.append((Path(f), bytes.fromhex(h)))
    return _Pkg(
        working_dir,
        ResourceType.WORKING_DIR,
        PackagePrefix.BASE_PREFIX,
        meta["hash_val"],
        files,
    )


""""
The following functions are related with package splitting and uploading
"""


def _calc_pkg_for_working_dir(
    working_dir: Path, excludes: List[str], meta: Optional[Dict[str, Any]]
) -> Tuple[
    Optional[_Pkg], Optional[_Pkg], Optional[_Pkg], List[_Pkg]
]:  # base  # add  # del  # files
    """Split the working directory and calculate the pkgs.

    The algorithm will go with this way:
       - create delta if we have base.
       - (or) create the base if no base.
       - if delta is too big (DELTA_PKG_LIMIT, default as 100MB), we update the
         base.

    All big files will be put into a separate package.

    Args:
        working_dir (Path): The working directory to split.
        excludes (List[str]): The pattern to exclude from. It follows gitignore.
        meta (Optional[Dict[str, Any]]): This is the base meta we have.

    Returns:
        List of packages(base_pkg, add_pkg, del_pkg, pkgs)
    """
    # TODO (yic) Try to avoid calling ray internal API
    if ".anyscale_runtime_dir" not in excludes:
        excludes.append(".anyscale_runtime_dir")
    excludes = _get_excludes(working_dir, excludes)
    pkgs = []
    files = []
    hash_val = None
    base_files = copy.deepcopy(meta["files"]) if meta is not None else {}
    delta_size = 0

    all_files = []
    all_hash_val = None

    def handler(path: Path) -> None:
        # These nonlocals are output of the traveling.
        #   hash_val: the hash value of delta package
        #   all_files: contain all files for the new base which will be used if we re-base
        #   all_hash_val: the hash value of new base
        #   pkgs: contains big files which size is greater than SINGLE_FILE_MINIMAL
        #   delta_size: the size of the delta
        nonlocal hash_val, all_files, all_hash_val, files, pkgs, delta_size
        if path.is_dir() and next(path.iterdir(), None) is not None:
            return
        to_path = path.relative_to(working_dir)
        file_hash = _entry_hash(path, to_path)
        entry = (to_path, file_hash)
        # If it's a big file, put it into a separate pkg
        if path.is_file() and path.stat().st_size >= SINGLE_FILE_MINIMAL:
            pkg = _Pkg(
                working_dir,
                ResourceType.WORKING_DIR,
                PackagePrefix.ADD_PREFIX,
                file_hash.hex(),
                [entry],
            )
            pkgs.append(pkg)
        else:  # If it's an empty directory or just a small file
            if base_files.pop(str(to_path), None) != file_hash.hex():
                files.append(entry)
                hash_val = _xor_bytes(hash_val, file_hash)
                delta_size += path.stat().st_size
            # We also put it into all_files in case the delta is too big and we'd need
            # to change the base
            all_files.append(entry)
            all_hash_val = _xor_bytes(all_hash_val, file_hash)

    # Travel the dir with ray runtime env's api
    _dir_travel(working_dir, [excludes] if excludes else [], handler)

    # If there is no base or the delta is too big, we'll update the base
    if meta is None or delta_size > DELTA_PKG_LIMIT:
        base_pkg = None
        if all_hash_val is not None:
            base_pkg = _Pkg(
                working_dir,
                ResourceType.WORKING_DIR,
                PackagePrefix.BASE_PREFIX,
                all_hash_val.hex(),
                all_files,
            )
        return (base_pkg, None, None, pkgs)

    # Otherwise reuse base pkg
    base_pkg = _get_base_pkg_from_meta(working_dir, meta)
    add_pkg = None
    if hash_val is not None:
        add_pkg = _Pkg(
            working_dir,
            ResourceType.WORKING_DIR,
            PackagePrefix.ADD_PREFIX,
            hash_val.hex(),
            files,
        )
    # If there is some files existing in base, it means this files have been deleted.
    # In this case, we need to generate a del pkg.
    del_pkg = None
    if len(base_files) != 0:
        hash_val = None
        del_files = []
        for (del_file, _) in base_files.items():
            hasher = hashlib.md5()
            hasher.update(del_file.encode())
            hash_val = _xor_bytes(hash_val, hasher.digest())
            del_files.append((Path(del_file), bytes()))
        assert hash_val is not None
        del_pkg = _Pkg(
            working_dir,
            ResourceType.WORKING_DIR,
            PackagePrefix.DEL_PREFIX,
            hash_val.hex(),
            del_files,
        )
    return (base_pkg, add_pkg, del_pkg, pkgs)


async def _upload_pkg(
    session: aiobotocore.AioSession, token: Any, file_pkg: _Pkg
) -> bool:
    """Upload the package if it doesn't exist in s3"""
    async with _create_s3_client(session, token) as s3:
        # The content hash is encoded in the path of the package, so we don't
        # need to compare the contents of the package. Although, there might be
        # hash collision, given that it's using md5 128bits and we also put
        # files from different orgs into different paths, it won't happen in
        # the real world.
        exists = await _object_exists(s3, token.bucket, token.path + file_pkg.name())
        if exists:
            logger.debug(f"{file_pkg.name()} exists in s3. Skip uploading.")
            return False
        local_pkg = file_pkg.create_tar_file()
        logger.info(f"Uploading runtime env {file_pkg.name()}")
        await _put_object(s3, token.bucket, token.path + file_pkg.name(), local_pkg)
        os.unlink(local_pkg)
        return True


async def _upload_file_pkgs(
    session: aiobotocore.AioSession, token: Any, file_pkgs: List[_Pkg],
) -> None:
    tasks = [_upload_pkg(session, token, pkg) for pkg in file_pkgs]
    done, pending = await asyncio.wait(tasks)
    assert not pending


"""
The following functions are related with package downloading and construction
"""


async def _fetch_dir_pkg(
    session: aiobotocore.AioSession, token: Any, pkg_uri: _PkgURI
) -> None:
    local_path = pkg_uri.local_path()
    with FileLock(str(local_path) + ".lock"):
        if local_path.exists():
            assert local_path.is_dir()
        else:
            async with _create_s3_client(session, token) as s3:
                local_path.mkdir()
                streambody = await _get_object(
                    s3, token.bucket, token.path + pkg_uri.name()
                )
                # TODO (yic) Use streaming mode instead of downloading everything
                with tempfile.NamedTemporaryFile() as tmp_tar:
                    async for data in streambody.iter_chunks():
                        tmp_tar.write(data)
                    tmp_tar.flush()
                    with tarfile.open(tmp_tar.name, mode="r:*") as tar:
                        tar.extractall(local_path)


async def _fetch_uris(
    session: aiobotocore.AioSession, token: Any, pkg_uris: List[_PkgURI],
) -> None:
    tasks = [
        _fetch_dir_pkg(session, token, pkg_uri)
        for pkg_uri in pkg_uris
        if not pkg_uri.is_resource_dir_pkg()
    ]
    if len(tasks) != 0:
        done, pending = await asyncio.wait(tasks)
        assert not pending


def _is_fs_leaf(path: Path) -> bool:
    return path.is_file() or (path.is_dir() and next(path.iterdir(), None) is None)


def _link_fs_children(from_path: Path, to_path: Path) -> None:
    assert from_path.is_dir() and to_path.is_dir()
    for f in from_path.glob("*"):
        (to_path / f.name).symlink_to(f)


def _merge_del(working_dir: Path, del_path: Path) -> None:
    """Recursively iterate through `del_path` and delete it from `working_dir`"""
    assert working_dir.is_dir() and not working_dir.is_symlink()
    for f in del_path.glob("*"):
        to_path = working_dir / f.name
        # If the target is a leaf, we can just delete it
        if _is_fs_leaf(f):
            to_path.unlink()
        else:
            # If the to_path is a symlink, it means it's a link from shared
            # resources. For isolation, we create a new dir and link all
            # children to the physical dir
            if to_path.is_symlink():
                true_path = to_path.resolve()
                to_path.unlink()
                to_path.mkdir()
                _link_fs_children(true_path, to_path)
            # We go one step deeper in the dir here.
            # to_path is working_dir/some_path
            # f is del_path/some_path
            _merge_del(to_path, f)


def _merge_add(working_dir: Path, delta_path: Path) -> None:
    """Recursively iterate through delta_path and merge it to working_dir"""
    assert working_dir.is_dir() and not working_dir.is_symlink()
    for f in delta_path.glob("*"):
        to_path = working_dir / f.name
        # We link it to the target directly if the target doesn't exist
        if not to_path.exists():
            to_path.symlink_to(f)
            continue
        else:
            # If the target exist, it means we might need to overwrite it
            if to_path.is_file() or (to_path.is_dir() and f.is_file()):
                # Working dir is not symlink, which means it's only visible
                # to current job. So we can delete the file directly from it.
                to_path.unlink()
                to_path.symlink_to(f)
            else:
                # If the target is a symlink, we need to create a folder and
                # link all the children to this new created one.
                if to_path.is_symlink():
                    true_path = to_path.resolve()
                    to_path.unlink()
                    to_path.mkdir()
                    _link_fs_children(true_path, to_path)
                _merge_add(to_path, f)


def _construct_from_uris(pkg_uris: List[_PkgURI]) -> Path:
    """Construct the working directory from the pkgs"""

    # Firstly, we split `pkg_uris` into three parts: base, adds and del.
    base_pkg = None
    add_pkg = []
    del_pkg = None
    resource_dir_pkg = None
    for p in pkg_uris:
        if p.is_base_pkg():
            assert base_pkg is None
            base_pkg = p
        elif p.is_add_pkg():
            add_pkg.append(p)
        elif p.is_del_pkg():
            assert del_pkg is None
            del_pkg = p
        elif p.is_resource_dir_pkg():
            assert resource_dir_pkg is None
            resource_dir_pkg = p
        else:
            assert False
    assert resource_dir_pkg is not None
    resource_dir = resource_dir_pkg.local_path()
    # Lock is necessary since multiple workers might be generating working dir at the same time.
    with FileLock(str(resource_dir) + ".lock"):
        if resource_dir.exists():
            assert resource_dir.is_dir()
            logger.debug("Skipping construction of working dir")
            return resource_dir
        # if we only have base_pkg, we'll use it directly
        # otherwise, soft link them to the temp dir
        if base_pkg is not None and len(add_pkg) == 0 and del_pkg is None:
            # We only have working dir, so link it directly
            resource_dir.symlink_to(base_pkg.local_path())
        else:
            resource_dir.mkdir()
            if base_pkg is not None:
                _link_fs_children(base_pkg.local_path(), resource_dir)
        # If there is delete pkg, merge it
        if del_pkg:
            _merge_del(resource_dir, del_pkg.local_path())
        # merge all add pkg
        for pkg in add_pkg:
            _merge_add(resource_dir, pkg.local_path())
        return resource_dir


"""
The following functions are to support working dir caching.
Ray setup script will use these functions instead of open source ones
"""


def rewrite_runtime_env_uris(job_config: JobConfig) -> None:
    """Rewriting the job_config to calculate the pkgs needed for this runtime_env"""

    # If the uris has been set, we'll use this directly
    if job_config.runtime_env.get("uris") is not None:
        return
    working_dir = job_config.runtime_env.get("working_dir")
    excludes = job_config.runtime_env.get("excludes") or []
    if working_dir is None:
        return
    working_path = Path(working_dir).absolute()
    assert working_path.is_dir()
    meta = _read_dir_meta(Path(working_dir))
    # get working_dir pkgs
    (base_pkg, add_pkg, del_pkg, file_pkgs) = _calc_pkg_for_working_dir(
        working_path, excludes, meta
    )
    # Put all uris into `uris` field.
    job_config.runtime_env["uris"] = [p.uri() for p in file_pkgs]
    job_config.runtime_env["uris"].extend(
        [p.uri() for p in [base_pkg, add_pkg, del_pkg] if p is not None]
    )
    # Generate a random working dir.
    # Here we use a random working dir instead of the hash of the contents is
    # right now writing to working dir is not disabled, so we'd like to generate
    # new working dir instead of sharing it with other jobs.
    working_dir_uri = _PkgURI(
        ResourceType.WORKING_DIR, PackagePrefix.RESOURCE_DIR_PREFIX, uuid.uuid4().hex
    )
    job_config.runtime_env["uris"].append(working_dir_uri.uri())
    # Create a temp file to share infos around to avoid re-calculating the content hash
    # TODO (yic) We need better way to support this
    with tempfile.NamedTemporaryFile(delete=False) as f:
        Path(f.name).write_bytes(pickle.dumps((base_pkg, add_pkg, del_pkg, file_pkgs)))
        job_config.runtime_env["_pkg_contents"] = f.name
    logger.debug("rewriting finished")


def upload_runtime_env_package_if_needed(job_config: JobConfig) -> None:
    """If the uris doesn't exist, we'll upload them"""
    uris = job_config.runtime_env.get("uris")
    if not uris:
        return
    if "_skip_uploading" in job_config.runtime_env:
        logger.info("Skipping uploading for preset uris")
        return
    tmp_file = Path(job_config.runtime_env["_pkg_contents"])
    base_pkg, add_pkg, del_pkg, file_pkgs = pickle.loads(tmp_file.read_bytes())
    tmp_file.unlink()
    assert base_pkg is not None or (add_pkg is None and del_pkg is None)
    session = aiobotocore.get_session()
    all_pkgs = [p for p in ([base_pkg, add_pkg, del_pkg] + file_pkgs) if p is not None]
    token = _gen_token()
    if len(all_pkgs) != 0:
        event_loop.run_until_complete(_upload_file_pkgs(session, token, all_pkgs))
    if base_pkg is not None:
        base_pkg.update_meta()
    logger.debug("uploading finished")


def ensure_runtime_env_setup(uris: List[str]) -> Optional[str]:
    """Download uris from s3 if it doesn't exist locally."""
    if len(uris) == 0:
        return None
    pkg_uris = [_PkgURI.from_uri(uri) for uri in uris]
    # This funciton only take care of working dir right now.
    pkg_uris = [
        pkg_uri
        for pkg_uri in pkg_uris
        if pkg_uri.resource_type() == ResourceType.WORKING_DIR
    ]
    token = _gen_token()
    session = aiobotocore.get_session()
    task = _fetch_uris(session, token, pkg_uris)
    event_loop.run_until_complete(task)
    working_dir = _construct_from_uris(pkg_uris)
    sys.path.insert(0, str(working_dir))
    return str(working_dir)


"""
The following functions are to support caching conda
"""


async def _prepare_conda_env(
    base_pkg: _PkgURI, resource_dir_pkg: _PkgURI, conda_env: Dict[str, Any],
) -> None:
    token = _gen_token()
    session = aiobotocore.get_session()
    async with _create_s3_client(session, token) as s3:
        exists = await _object_exists(s3, token.bucket, token.path + base_pkg.name())
        if not exists:
            logger.debug("Conda env doesn't exist in s3.")
            # if not exist, install first
            if not resource_dir_pkg.local_path().exists():
                yaml_str = yaml.dump(conda_env)
                logger.debug(f"Install conda env: {yaml_str}")
                with tempfile.NamedTemporaryFile(suffix=".yml") as f:
                    Path(f.name).write_text(yaml_str)
                    env_dir = Path(
                        ray_conda.get_or_create_conda_env(  # type: ignore
                            f.name, resource_dir_pkg.name(), PKG_DIR
                        )
                    )
                    assert env_dir == resource_dir_pkg.local_path()
            # create package and upload it to s3
            with tempfile.NamedTemporaryFile() as f:
                logger.debug(f"Uploading conda package to: {base_pkg.name()}")
                conda_pack.pack(
                    prefix=str(resource_dir_pkg.local_path()),
                    dest_prefix=str(resource_dir_pkg.local_path()),
                    ignore_missing_files=True,
                    output=f.name,
                    compress_level=0,
                    format="tar",
                    n_threads=4,
                    force=True,
                )
                await _put_object(
                    s3, token.bucket, token.path + base_pkg.name(), f.name
                )
        else:
            logger.debug("Conda env has existed in s3.")
            if not resource_dir_pkg.local_path().exists():
                logger.debug("Fetching conda env from s3")
                # fetch it from s3 and unpack
                streambody = await _get_object(
                    s3, token.bucket, token.path + base_pkg.name()
                )
                with tempfile.NamedTemporaryFile() as tmp_tar:
                    async for data in streambody.iter_chunks():
                        tmp_tar.write(data)
                    tmp_tar.flush()
                    with tarfile.open(tmp_tar.name, mode="r:*") as tar:
                        tar.extractall(resource_dir_pkg.local_path())
            else:
                logger.debug("No need to prepare conda. It has been setup locally.")


# To make it compatible with shim process in oss ray
parser = argparse.ArgumentParser()

parser.add_argument(
    "--serialized-runtime-env", type=str, help="the serialized parsed runtime env dict"
)

parser.add_argument(
    "--session-dir", type=str, help="the directory for the current session"
)


def ray_client_server_env_prep(job_config: JobConfig) -> JobConfig:
    """Preparation function for client server manager
    Before rewriting, conda field should be:
       runtime_env: {
           "conda": str|dict,
           "working_dir": ...,
           "uris": []
       }

    After rewriting, conda field should be:
       runtime_env: {
          "conda": str|dict,
          uris: [] // s3 pkgs. It can be base_/add_
       }

    This function will do:
      - generate env_dir and file locking
      - if local_exist == False
        - if s3_exist == True
          download from s3 && unpack it to env_dir
        - else install it from cmd to env_dir
      - if s3_exist == False
        - pack the env from env_dir and upload it to s3

    The rewriting runtime env will be returned.
    """
    runtime_env = job_config.runtime_env
    conda_env = runtime_env.get("conda")
    pip_config = runtime_env.get("pip")

    if conda_env is None and pip_config is None:
        logger.debug("No conda/pip, do nothing in prep")
        return job_config

    if isinstance(conda_env, str):
        logger.debug("preset conda env, do nothing in prep")
        return job_config

    # Add anyscale && ray installation into conda explicitly
    ray_release = runtime_env["_ray_release"]
    wheel_url = get_wheel_url(ray_release)
    py_dep = f"python={platform.python_version()}"
    if conda_env is None:
        pip_config += "\nanyscale\n" + wheel_url
        runtime_env["pip"] = pip_config
        config_str = pip_config
    else:
        if "dependencies" not in conda_env:
            conda_env["dependencies"] = [
                py_dep,
                "pip",
                {"pip": ["anyscale", wheel_url]},
            ]
        else:
            pip_packages = None
            for dep in conda_env["dependencies"]:
                if isinstance(dep, dict) and "pip" in dep:
                    pip_packages = dep["pip"]
            if pip_packages is None:
                pip_packages = []
                conda_env["dependencies"].append({"pip": pip_packages})
            pip_packages.append(wheel_url)
            pip_packages.append("anyscale")
            conda_env["dependencies"].append(py_dep)

        config_str = yaml.dump(conda_env)
    pkg_hash = hashlib.md5(config_str.encode()).hexdigest()
    resource_dir_pkg = _PkgURI(
        ResourceType.CONDA, PackagePrefix.RESOURCE_DIR_PREFIX, pkg_hash
    )
    # Right now base pkg is alway the same as resource pkg since we don't
    # support delta pkgs
    base_pkg = _PkgURI(ResourceType.CONDA, PackagePrefix.BASE_PREFIX, pkg_hash)
    if "uris" not in runtime_env:
        runtime_env["uris"] = []
    runtime_env["uris"].append(resource_dir_pkg.uri())
    runtime_env["uris"].append(base_pkg.uri())
    job_config.set_runtime_env(runtime_env)
    return job_config


def _get_conda_packages(uris: List[str]) -> Tuple[_PkgURI, _PkgURI]:
    base_pkg = None
    resource_dir_pkg = None
    pkgs = [_PkgURI.from_uri(uri) for uri in uris]
    for pkg in pkgs:
        if pkg.resource_type() == ResourceType.CONDA:
            if pkg.is_base_pkg():
                assert base_pkg is None
                base_pkg = pkg
            elif pkg.is_resource_dir_pkg():
                assert resource_dir_pkg is None
                resource_dir_pkg = pkg
            else:
                assert False
    assert base_pkg is not None and resource_dir_pkg is not None
    return (resource_dir_pkg, base_pkg)


def worker_setup_func(input_args: Any) -> None:
    """This func will install conda env if not exists. And it'll activate it.

    conda env should be:
      {
          uris: [] // s3 pkgs. It can be base_/add_
      }
    We'll use ensure_runtime_env_setup to prepare the local dir and we'll use
    code from oss ray to activate it.
    """
    # remaining_args contains the arguments to the original worker command,
    # minus the python executable, e.g. default_worker.py --node-ip-address=...
    args, remaining_args = parser.parse_known_args(args=input_args)

    commands = []
    runtime_env = json.loads(args.serialized_runtime_env or "{}")

    conda_env = runtime_env.get("conda")
    pip_env = runtime_env.get("pip")

    # We have conda here, need to set it up
    if conda_env is not None or pip_env is not None:
        if isinstance(conda_env, str):
            conda_env_path = conda_env
        else:
            # TODO: HACKY: Ray need to call prep
            if len(runtime_env.get("uris", [])) == 0:
                if conda_env is None:
                    runtime_env.pop("conda")
                if pip_env is None:
                    runtime_env.pop("pip")
                runtime_env.pop("working_dir")
                import ray

                runtime_env["_ray_release"] = f"master/{ray.__commit__}"
                job_config = ray_client_server_env_prep(
                    JobConfig(runtime_env=runtime_env)
                )
                runtime_env = job_config.runtime_env

            resource_dir_pkg, base_pkg = _get_conda_packages(
                runtime_env.get("uris", [])
            )
            local_path = resource_dir_pkg.local_path()
            with FileLock(str(local_path) + ".local"):
                if pip_env is not None:
                    with tempfile.NamedTemporaryFile(suffix=".txt") as f:
                        Path(f.name).write_text(pip_env)
                        pip_conda = {
                            "dependencies": [
                                f"python={platform.python_version()}",
                                "pip",
                                "pip",
                                {"pip": [f"-r {f.name}"]},
                            ]
                        }
                        event_loop.run_until_complete(
                            _prepare_conda_env(base_pkg, resource_dir_pkg, pip_conda)
                        )
                else:
                    event_loop.run_until_complete(
                        _prepare_conda_env(base_pkg, resource_dir_pkg, conda_env)
                    )
            conda_env_path = str(local_path)
        commands += ray_conda.get_conda_activate_commands(conda_env_path)  # type: ignore

    commands += [" ".join(["exec python"] + remaining_args)]
    command_separator = " && "
    command_str = command_separator.join(commands)
    os.execvp("bash", ["bash", "-c", command_str])


"""
The following functions are anyscale related functions
"""


def register_runtime_env(env: Dict[str, Any]) -> List[str]:
    job_config = JobConfig(runtime_env=env)
    rewrite_runtime_env_uris(job_config)
    upload_runtime_env_package_if_needed(job_config)
    uris = job_config.runtime_env["uris"]
    assert isinstance(uris, list)
    return uris


def runtime_env_setup() -> None:
    import ray._private.runtime_env as ray_runtime_env

    ray_runtime_env.rewrite_runtime_env_uris = rewrite_runtime_env_uris
    ray_runtime_env.upload_runtime_env_package_if_needed = (
        upload_runtime_env_package_if_needed
    )
    ray_runtime_env.ensure_runtime_env_setup = ensure_runtime_env_setup

    import ray.ray_constants as ray_constants

    ray_constants.DEFAULT_WORKER_SETUP_HOOK = (
        "anyscale.utils.runtime_env.worker_setup_func"
    )

    import ray.util.client.server.proxier as proxier

    proxier.ray_client_server_env_prep = ray_client_server_env_prep
