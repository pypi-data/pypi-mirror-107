from datetime import datetime
import os
from pathlib import Path
import platform
import subprocess
import tempfile
from typing import Any, Callable, cast, Dict, List, Optional, Tuple
from unittest.mock import ANY, Mock

import pytest
import requests
import yaml

import anyscale
from anyscale.client.openapi_client.models.app_config import AppConfig
from anyscale.client.openapi_client.models.build import Build
from anyscale.client.openapi_client.models.project import Project
from anyscale.client.openapi_client.models.project_response import ProjectResponse
from anyscale.client.openapi_client.models.session import Session
from anyscale.connect import (
    _is_in_shell,
    ClientBuilder,
    PINNED_IMAGES,
    REQUIRED_RAY_COMMIT,
    REQUIRED_RAY_VERSION,
)
from anyscale.util import get_wheel_url
import anyscale.utils.runtime_env


def _make_session(i: int, state: str) -> Session:
    return Session(
        id="session_id",
        name="session-{}".format(i),
        created_at=datetime.now(),
        snapshots_history=[],
        idle_timeout=120,
        tensorboard_available=False,
        project_id="project_id",
        state=state,
        service_proxy_url="http://session-{}.userdata.com/auth?token=value&bar".format(
            i
        ),
        connect_url="session-{}.userdata.com:8081?port=10001".format(i),
        jupyter_notebook_url="http://session-{}.userdata.com/jupyter/lab?token=value".format(
            i
        ),
        access_token="value",
    )


def _make_app_template() -> AppConfig:
    return AppConfig(
        project_id="project_id",
        id="application_template_id",
        name="test-app-config",
        creator_id="creator_id",
        created_at=datetime.now(),
        last_modified_at=datetime.now(),
    )


def _make_build() -> Build:
    return Build(
        id="build_id",
        revision=0,
        application_template_id="application_template_id",
        config_json="",
        creator_id="creator_id",
        status="succeeded",
        created_at=datetime.now(),
        last_modified_at=datetime.now(),
        docker_image_name="docker_image_name",
    )


def _connected(ray: Mock, ret: Dict[str, Any],) -> Callable[[Any, Any], Dict[str, Any]]:
    def connected(*a: Any, **kw: Any) -> Dict[str, Any]:
        ray.util.client.ray.is_connected.return_value = True
        returnable = {
            "num_clients": 1,
            "ray_version": REQUIRED_RAY_VERSION,
            "ray_commit": REQUIRED_RAY_COMMIT,
            "python_version": platform.python_version(),
        }
        returnable.update(**ret)
        return returnable

    return connected


def _make_test_builder(
    tmp_path: Path,
    session_states: Optional[List[str]] = None,
    setup_project_dir: bool = True,
) -> Tuple[Any, Any, Any, Any]:
    if session_states is None:
        session_states = ["Running"]

    scratch = tmp_path / "scratch"
    sdk = Mock()
    sess_resp = Mock()
    ray = Mock()

    ray.__commit__ = REQUIRED_RAY_COMMIT
    ray.__version__ = REQUIRED_RAY_VERSION
    ray.util.client.ray.is_connected.return_value = False
    anyscale.utils.runtime_env.runtime_env_setup = Mock()

    def disconnected(*a: Any, **kw: Any) -> None:
        ray.util.client.ray.is_connected.return_value = False

    # Emulate session lock failure.
    ray.util.connect.side_effect = _connected(ray, {"num_clients": 1})
    ray.util.disconnect.side_effect = disconnected
    if os.environ.get("ANYSCALE_ENABLE_RUNTIME_ENV") == "1":
        job_config_mock = Mock()
        job_config_mock.runtime_env = {}
        job_config_mock.set_runtime_env.return_value = Mock()
        job_config_mock.metadata = {}
        ray.job_config.JobConfig.return_value = job_config_mock
    else:
        ray.job_config.JobConfig.return_value = None
    sess_resp.results = [
        _make_session(i, state) for i, state in enumerate(session_states)
    ]
    sess_resp.metadata.next_paging_token = None
    sdk.list_sessions.return_value = sess_resp
    proj_resp = Mock()
    proj_resp.result.name = "scratch"
    sdk.get_project.return_value = proj_resp
    subprocess = Mock()
    _os = Mock()
    _api_client = Mock()
    _api_client.get_user_info_api_v2_userinfo_get.return_value.result = Mock(
        organizations=[Mock(default_cloud_id=None)]
    )
    builder = ClientBuilder(
        scratch_dir=scratch.absolute().as_posix(),
        anyscale_sdk=sdk,
        subprocess=subprocess,
        _ray=ray,
        _os=_os,
        _ignore_version_check=False,
        api_client=_api_client,
    )
    if setup_project_dir:
        builder.project_dir(scratch.absolute().as_posix())
    else:
        builder._in_shell = True
    builder._find_project_id = lambda _: None  # type: ignore

    def create_session(*a: Any, **kw: Any) -> None:
        sess_resp.results = sess_resp.results + [
            _make_session(len(sess_resp.results), "Running")
        ]
        sdk.list_sessions.return_value = sess_resp

    setattr(builder, "_up_session", Mock())
    setattr(builder, "_start_session", Mock())
    builder._up_session.side_effect = create_session  # type: ignore
    builder._start_session.side_effect = create_session  # type: ignore

    setattr(
        builder, "_get_last_used_cloud", Mock(return_value="anyscale_default_cloud")
    )
    return builder, sdk, subprocess, ray


def test_parse_address() -> None:
    """Tests ClientBuilder._parse_address which parses the anyscale address."""

    sdk = Mock()
    _api_client = Mock()
    connect_instance = ClientBuilder(anyscale_sdk=sdk, api_client=_api_client)

    connect_instance._parse_address(None)
    assert connect_instance._session_name is None
    assert connect_instance._autosuspend_timeout == 120
    assert connect_instance._cluster_compute_name is None
    assert connect_instance._cluster_env_name is None

    connect_instance._parse_address("")
    assert connect_instance._session_name is None
    assert connect_instance._autosuspend_timeout == 120
    assert connect_instance._cluster_compute_name is None
    assert connect_instance._cluster_env_name is None

    connect_instance._parse_address("cluster_name")
    assert connect_instance._session_name == "cluster_name"
    assert connect_instance._autosuspend_timeout == 120
    assert connect_instance._cluster_compute_name is None
    assert connect_instance._cluster_env_name is None

    connect_instance._parse_address(
        "my_cluster?cluster_compute=my_template&autosuspend=5&cluster_env=bla:1"
    )
    assert connect_instance._session_name == "my_cluster"
    assert connect_instance._autosuspend_timeout == 5
    assert connect_instance._cluster_compute_name == "my_template"
    assert connect_instance._cluster_env_name == "bla"

    with pytest.raises(ValueError):
        # we only support cluster_compute, cluster_env, autosuspend
        connect_instance._parse_address("my_cluster?random=5")


@pytest.mark.parametrize("enable_runtime_env", [True, False])
def test_new_proj_connect_params(
    enable_runtime_env: bool, tmp_path: Path, project_test_data: Project
) -> None:
    os.environ["ANYSCALE_ENABLE_RUNTIME_ENV"] = "1" if enable_runtime_env else "0"
    project_dir = (tmp_path / "my_proj").absolute().as_posix()
    builder, sdk, subprocess, ray = _make_test_builder(tmp_path)
    sdk.create_project.return_value = ProjectResponse(result=project_test_data)

    # Should create a new .anyscale.yaml file
    builder.project_dir(project_dir).connect()

    assert anyscale.project.get_project_id(project_dir)
    if enable_runtime_env:
        builder._start_session.assert_called_once_with(
            project_id=project_test_data.id,
            session_name="session-1",
            cloud_name="anyscale_default_cloud",
            build_id=None,
            yaml_filepath=ANY,
        )
    else:
        builder._up_session.assert_called_once_with(
            project_test_data.id,
            "session-1",
            "anyscale_default_cloud",
            project_dir,
            dangerously_set_build_id=None,
            yaml_filepath=ANY,
        )

    # Also check connection params in this test.
    ray.util.connect.assert_called_with(
        "session-1.userdata.com:8081",
        metadata=[("cookie", "anyscale-token=value"), ("port", "10001")],
        secure=False,
        connection_retries=10,
        ignore_version=True,
        job_config=ray.job_config.JobConfig(),
    )


@pytest.mark.parametrize("enable_runtime_env", [True, False])
def test_detect_existing_proj(enable_runtime_env: bool, tmp_path: Path) -> None:
    os.environ["ANYSCALE_ENABLE_RUNTIME_ENV"] = "1" if enable_runtime_env else "0"
    nested_dir = (tmp_path / "my_proj" / "nested").absolute().as_posix()
    parent_dir = os.path.dirname(nested_dir)
    os.makedirs(nested_dir)
    builder, sdk, subprocess, ray = _make_test_builder(
        tmp_path, setup_project_dir=False
    )

    # Setup project in parent dir
    project_yaml = os.path.join(parent_dir, ".anyscale.yaml")
    with open(project_yaml, "w+") as f:
        f.write(yaml.dump({"project_id": 12345}))

    # Should detect the parent project dir
    cwd = os.getcwd()
    try:
        os.chdir(nested_dir)
        builder.session("session-0").connect()
    finally:
        os.chdir(cwd)

    if enable_runtime_env:
        builder._start_session.assert_called_once_with(
            project_id=ANY,
            session_name="session-0",
            cloud_name="anyscale_default_cloud",
            build_id=None,
            yaml_filepath=ANY,
        )
    else:
        builder._up_session.assert_called_once_with(
            ANY,
            "session-0",
            "anyscale_default_cloud",
            parent_dir,
            dangerously_set_build_id=None,
            yaml_filepath=ANY,
        )


@pytest.mark.parametrize("enable_runtime_env", [True, False])
def test_fallback_scratch_dir(
    enable_runtime_env: bool, tmp_path: Path, project_test_data: Project
) -> None:
    os.environ["ANYSCALE_ENABLE_RUNTIME_ENV"] = "1" if enable_runtime_env else "0"
    scratch_dir = (tmp_path / "scratch").absolute().as_posix()
    builder, sdk, subprocess, ray = _make_test_builder(tmp_path)
    sdk.create_project.return_value = ProjectResponse(result=project_test_data)

    # Should create a new .anyscale.yaml file in the scratch dir
    builder.connect()

    assert anyscale.project.get_project_id(scratch_dir)
    if enable_runtime_env:
        builder._start_session.assert_called_once_with(
            project_id=project_test_data.id,
            session_name="session-1",
            cloud_name="anyscale_default_cloud",
            build_id=None,
            yaml_filepath=ANY,
        )
    else:
        builder._up_session.assert_called_once_with(
            project_test_data.id,
            "session-1",
            "anyscale_default_cloud",
            scratch_dir,
            dangerously_set_build_id=None,
            yaml_filepath=ANY,
        )


@pytest.mark.parametrize("enable_runtime_env", [True, False])
def test_background_run_mode(
    enable_runtime_env: bool, tmp_path: Path, project_test_data: Project
) -> None:
    os.environ["ANYSCALE_ENABLE_RUNTIME_ENV"] = "1" if enable_runtime_env else "0"
    scratch_dir = (tmp_path / "scratch").absolute().as_posix()
    builder, sdk, subprocess, ray = _make_test_builder(tmp_path)
    sdk.create_project.return_value = ProjectResponse(result=project_test_data)

    # Should create a new .anyscale.yaml file in the scratch dir
    builder.run_mode("background").connect()

    assert anyscale.project.get_project_id(scratch_dir)
    builder._subprocess.check_output.assert_called_with(
        ["anyscale", "push", "session-1", "-s", ANY, "-t", ANY], stderr=ANY
    )
    builder._subprocess.check_call.assert_called_with(ANY)
    builder._os._exit.assert_called_once_with(0)


@pytest.mark.parametrize("enable_runtime_env", [True, False])
def test_local_docker_run_mode(
    enable_runtime_env: bool, tmp_path: Path, project_test_data: Project
) -> None:
    os.environ["ANYSCALE_ENABLE_RUNTIME_ENV"] = "1" if enable_runtime_env else "0"
    scratch_dir = (tmp_path / "scratch").absolute().as_posix()
    builder, sdk, subprocess, ray = _make_test_builder(tmp_path)
    sdk.create_project.return_value = ProjectResponse(result=project_test_data)

    # Should create a new .anyscale.yaml file in the scratch dir
    builder.run_mode("local_docker").connect()

    assert anyscale.project.get_project_id(scratch_dir)
    builder._subprocess.check_call.assert_called_with(
        [
            "docker",
            "run",
            "--env",
            ANY,
            "--env",
            ANY,
            "-v",
            ANY,
            "--entrypoint=/bin/bash",
            ANY,
            "-c",
            ANY,
        ]
    )
    builder._os._exit.assert_called_once_with(0)


@pytest.mark.parametrize("enable_runtime_env", [True, False])
def test_connect_with_cloud(
    enable_runtime_env: bool, tmp_path: Path, project_test_data: Project
) -> None:
    os.environ["ANYSCALE_ENABLE_RUNTIME_ENV"] = "1" if enable_runtime_env else "0"
    scratch_dir = (tmp_path / "scratch").absolute().as_posix()
    builder, sdk, subprocess, ray = _make_test_builder(tmp_path)
    sdk.create_project.return_value = ProjectResponse(result=project_test_data)

    # Should create a new .anyscale.yaml file in the scratch dir
    builder.session("session-0").cloud("test_cloud").connect()

    if enable_runtime_env:
        builder._start_session.assert_called_once_with(
            project_id=project_test_data.id,
            session_name="session-0",
            cloud_name="test_cloud",
            build_id=None,
            yaml_filepath=ANY,
        )
    else:
        builder._up_session.assert_called_once_with(
            project_test_data.id,
            "session-0",
            "test_cloud",
            scratch_dir,
            dangerously_set_build_id=None,
            yaml_filepath=ANY,
        )


@pytest.mark.parametrize("enable_runtime_env", [True, False])
def test_clone_scratch_dir(
    enable_runtime_env: bool, tmp_path: Path, project_test_data: Project
) -> None:
    os.environ["ANYSCALE_ENABLE_RUNTIME_ENV"] = "1" if enable_runtime_env else "0"
    scratch_dir = (tmp_path / "scratch").absolute().as_posix()
    builder, sdk, subprocess, ray = _make_test_builder(
        tmp_path, setup_project_dir=False
    )
    builder._find_project_id = lambda _: "foo"
    sdk.create_project.return_value = ProjectResponse(result=project_test_data)

    def clone_project(*a: Any, **kw: Any) -> None:
        os.makedirs(scratch_dir, exist_ok=True)
        project_yaml = os.path.join(scratch_dir, ".anyscale.yaml")
        with open(project_yaml, "w+") as f:
            f.write(yaml.dump({"project_id": 12345}))

    builder._subprocess.check_call.side_effect = clone_project

    # Should create a new .anyscale.yaml file in the scratch dir
    builder.session("session-0").connect()

    builder._subprocess.check_call.assert_called_once_with(
        ["anyscale", "clone", "scratch"]
    )
    if enable_runtime_env:
        builder._start_session.assert_called_once_with(
            project_id="12345",
            session_name="session-0",
            cloud_name="anyscale_default_cloud",
            build_id=None,
            yaml_filepath=ANY,
        )
    else:
        builder._up_session.assert_called_once_with(
            "12345",
            "session-0",
            "anyscale_default_cloud",
            scratch_dir,
            dangerously_set_build_id=None,
            yaml_filepath=ANY,
        )


@pytest.mark.parametrize("enable_runtime_env", [True, False])
def test_new_session(
    enable_runtime_env: bool, tmp_path: Path, project_test_data: Project
) -> None:
    os.environ["ANYSCALE_ENABLE_RUNTIME_ENV"] = "1" if enable_runtime_env else "0"
    scratch_dir = (tmp_path / "scratch").absolute().as_posix()
    builder, sdk, subprocess, ray = _make_test_builder(tmp_path, session_states=[])
    sdk.create_project.return_value = ProjectResponse(result=project_test_data)

    # Should create a new session.
    builder.session("session-0").connect()

    if enable_runtime_env:
        builder._start_session.assert_called_once_with(
            project_id=ANY,
            session_name="session-0",
            cloud_name="anyscale_default_cloud",
            build_id=None,
            yaml_filepath=ANY,
        )
    else:
        builder._up_session.assert_called_once_with(
            ANY,
            "session-0",
            "anyscale_default_cloud",
            scratch_dir,
            dangerously_set_build_id=None,
            yaml_filepath=ANY,
        )


@pytest.mark.parametrize("enable_runtime_env", [True, False])
@pytest.mark.parametrize("static_ray_version_mismatch", [True, False])
@pytest.mark.parametrize("use_compute_config", [True, False])
def test_base_docker_image(
    enable_runtime_env: bool,
    static_ray_version_mismatch: bool,
    use_compute_config: bool,
    tmp_path: Path,
    project_test_data: Project,
) -> None:
    os.environ["ANYSCALE_COMPUTE_CONFIG"] = "1" if use_compute_config else "0"
    os.environ["ANYSCALE_ENABLE_RUNTIME_ENV"] = "1" if enable_runtime_env else "0"
    scratch_dir = (tmp_path / "scratch").absolute().as_posix()
    builder, sdk, subprocess, ray = _make_test_builder(
        tmp_path, session_states=["Running"]
    )
    if static_ray_version_mismatch:
        ray.__commit__ = "abcdef"
        ray.util.connect.side_effect = _connected(ray, {"ray_commit": "abcdef"},)
    sdk.create_project.return_value = ProjectResponse(result=project_test_data)

    yaml_filepath = None

    def get_yaml_filepath(*n: Any, **kw: Any) -> None:
        nonlocal yaml_filepath
        yaml_filepath = kw["yaml_filepath"]
        sess_resp = Mock()
        sess_resp.results = [_make_session(0, "Running"), _make_session(1, "Running")]
        sess_resp.metadata.next_paging_token = None
        sdk.list_sessions.return_value = sess_resp

    if use_compute_config and enable_runtime_env:
        # Base docker images are no longer supported when starting a session with build id
        # and compute config.
        with pytest.raises(ValueError):
            builder.project_dir(scratch_dir).base_docker_image(
                "anyscale/ray-ml:custom"
            ).connect()
    else:
        builder._up_session.side_effect = get_yaml_filepath
        builder._start_session.side_effect = get_yaml_filepath
        builder.project_dir(scratch_dir).base_docker_image(
            "anyscale/ray-ml:custom"
        ).connect()

        with open(cast(str, yaml_filepath)) as f:
            data = yaml.safe_load(f)

        assert data["docker"]["image"] == "anyscale/ray-ml:custom"
        for nodes_type, node_config in data["available_node_types"].items():
            assert node_config["docker"]["worker_image"] == "anyscale/ray-ml:custom"


@pytest.mark.parametrize("enable_runtime_env", [True, False])
def test_requirements_list(
    enable_runtime_env: bool, tmp_path: Path, project_test_data: Project
) -> None:
    scratch_dir = (tmp_path / "scratch").absolute().as_posix()
    builder, sdk, subprocess, ray = _make_test_builder(tmp_path, session_states=[])
    sdk.create_project.return_value = ProjectResponse(result=project_test_data)

    yaml_filepath = None

    def create_session(*a: Any, **kw: Any) -> None:
        nonlocal yaml_filepath
        yaml_filepath = kw["yaml_filepath"]
        sess_resp = Mock()
        sess_resp.results = [_make_session(0, "Running")]
        sess_resp.metadata.next_paging_token = None
        sdk.list_sessions.return_value = sess_resp

    builder._up_session.side_effect = create_session
    builder._start_session.side_effect = create_session

    # Create a new session with a list of requirements.
    builder.project_dir(scratch_dir).require(["pandas", "wikipedia"]).connect()

    with open(cast(str, yaml_filepath)) as f:
        data = yaml.safe_load(f)

    assert (
        'echo "pandas\nwikipedia" | pip install -r /dev/stdin' in data["setup_commands"]
    )


@pytest.mark.parametrize("enable_runtime_env", [True, False])
def test_requirements_file(
    enable_runtime_env: bool, tmp_path: Path, project_test_data: Project
) -> None:
    os.environ["ANYSCALE_ENABLE_RUNTIME_ENV"] = "1" if enable_runtime_env else "0"
    scratch_dir = (tmp_path / "scratch").absolute().as_posix()
    builder, sdk, subprocess, ray = _make_test_builder(tmp_path, session_states=[])
    sdk.create_project.return_value = ProjectResponse(result=project_test_data)

    yaml_filepath = None

    def create_session(*a: Any, **kw: Any) -> None:
        nonlocal yaml_filepath
        yaml_filepath = kw["yaml_filepath"]
        sess_resp = Mock()
        sess_resp.results = [_make_session(0, "Running")]
        sess_resp.metadata.next_paging_token = None
        sdk.list_sessions.return_value = sess_resp

    builder._up_session.side_effect = create_session
    builder._start_session.side_effect = create_session

    with open("/tmp/requirements.txt", "w") as f:
        f.write("pandas\nwikipedia\ndask")
    # Create a new session with a requiremttns file.
    builder.project_dir(scratch_dir).require("/tmp/requirements.txt").connect()

    with open(cast(str, yaml_filepath)) as f:
        data = yaml.safe_load(f)

    assert (
        'echo "pandas\nwikipedia\ndask" | pip install -r /dev/stdin'
        in data["setup_commands"]
    )

    if enable_runtime_env:
        builder._start_session.assert_called_once_with(
            project_id=project_test_data.id,
            session_name="session-0",
            cloud_name="anyscale_default_cloud",
            build_id=None,
            yaml_filepath=ANY,
        )
    else:
        builder._up_session.assert_called_once_with(
            project_test_data.id,
            "session-0",
            "anyscale_default_cloud",
            scratch_dir,
            dangerously_set_build_id=None,
            yaml_filepath=ANY,
        )


@pytest.mark.parametrize("enable_runtime_env", [True, False])
def test_new_session_lost_lock(
    enable_runtime_env: bool, tmp_path: Path, project_test_data: Project
) -> None:
    os.environ["ANYSCALE_ENABLE_RUNTIME_ENV"] = "1" if enable_runtime_env else "0"
    scratch_dir = (tmp_path / "scratch").absolute().as_posix()
    builder, sdk, subprocess, ray = _make_test_builder(tmp_path, session_states=[])
    sdk.create_project.return_value = ProjectResponse(result=project_test_data)

    def create_session(*a: Any, **kw: Any) -> None:
        sess_resp = Mock()
        sess_resp.results = [_make_session(0, "Running")]
        sess_resp.metadata.next_paging_token = None
        sdk.list_sessions.return_value = sess_resp

    builder._up_session.side_effect = create_session

    # Emulate session lock failure.
    ray.util.connect.side_effect = _connected(ray, {"num_clients": 999999})

    # Should create a new session.
    with pytest.raises(RuntimeError):
        builder.connect()

    if enable_runtime_env:
        builder._start_session.assert_called_once_with(
            project_id=project_test_data.id,
            session_name="session-0",
            cloud_name="anyscale_default_cloud",
            build_id=None,
            yaml_filepath=ANY,
        )
    else:
        builder._up_session.assert_called_once_with(
            project_test_data.id,
            "session-0",
            "anyscale_default_cloud",
            scratch_dir,
            dangerously_set_build_id=None,
            yaml_filepath=ANY,
        )


@pytest.mark.parametrize("enable_runtime_env", [True, False])
def test_reuse_session_hash_match(
    enable_runtime_env: bool, tmp_path: Path, project_test_data: Project
) -> None:
    os.environ["ANYSCALE_ENABLE_RUNTIME_ENV"] = "1" if enable_runtime_env else "0"
    scratch_dir = (tmp_path / "scratch").absolute().as_posix()
    builder, sdk, subprocess, ray = _make_test_builder(
        tmp_path, session_states=["Running"]
    )
    sdk.create_project.return_value = ProjectResponse(result=project_test_data)

    # Create fake cluster yaml for fingerprinting.
    os.makedirs(scratch_dir)
    builder.require(["wikipedia", "dask"]).project_dir(scratch_dir)
    cluster_yaml = yaml.safe_load(anyscale.project.CLUSTER_YAML_TEMPLATE)
    cluster_yaml = builder._populate_cluster_config(
        cluster_yaml, "project_id", "scratch", build=None
    )
    with tempfile.NamedTemporaryFile(mode="w+", delete=False) as f:
        f.write(yaml.dump(cluster_yaml))
        yaml_filepath = f.name
    if enable_runtime_env:
        import hashlib

        hasher = hashlib.sha1()
        hasher.update(yaml.dump(cluster_yaml).encode())
        local_config_hash = hasher.hexdigest().encode()
    else:
        local_config_hash = builder._fingerprint(scratch_dir, yaml_filepath).encode()
    # Emulate session hash code match.
    ray.util.connect.return_value = {
        "num_clients": 1,
        "ray_version": REQUIRED_RAY_VERSION,
        "ray_commit": REQUIRED_RAY_COMMIT,
    }
    ray.experimental.internal_kv._internal_kv_get.return_value = local_config_hash

    # Hash code match, no update needed.
    builder.session("session-0").require(["wikipedia", "dask"]).connect()

    builder._up_session.assert_not_called()

    ray.util.disconnect()
    # Hash code doesn't match, update needed.
    builder.require(["wikipedia", "dask", "celery"]).connect()

    if enable_runtime_env:
        builder._start_session.assert_called_once_with(
            project_id=project_test_data.id,
            session_name="session-0",
            cloud_name="anyscale_default_cloud",
            build_id=None,
            yaml_filepath=ANY,
        )
    else:
        builder._up_session.assert_called_once_with(
            project_test_data.id,
            "session-0",
            "anyscale_default_cloud",
            scratch_dir,
            dangerously_set_build_id=None,
            yaml_filepath=ANY,
        )


@pytest.mark.parametrize("enable_runtime_env", [True, False])
def test_reuse_session_hash_mismatch(
    enable_runtime_env: bool, tmp_path: Path, project_test_data: Project
) -> None:
    os.environ["ANYSCALE_ENABLE_RUNTIME_ENV"] = "1" if enable_runtime_env else "0"
    scratch_dir = (tmp_path / "scratch").absolute().as_posix()
    builder, sdk, subprocess, ray = _make_test_builder(
        tmp_path, session_states=["Running"]
    )
    sdk.create_project.return_value = ProjectResponse(result=project_test_data)

    local_config_hash = b"wrong-hash-code"

    # Emulate session hash code mismatch.
    ray.experimental.internal_kv._internal_kv_get.return_value = local_config_hash

    # Should connect and run 'up'.
    builder.session("session-0").connect()

    if enable_runtime_env:
        builder._start_session.assert_called_once_with(
            project_id=project_test_data.id,
            session_name="session-0",
            cloud_name="anyscale_default_cloud",
            build_id=None,
            yaml_filepath=ANY,
        )
    else:
        builder._up_session.assert_called_once_with(
            project_test_data.id,
            "session-0",
            "anyscale_default_cloud",
            scratch_dir,
            dangerously_set_build_id=None,
            yaml_filepath=ANY,
        )


@pytest.mark.parametrize("enable_runtime_env", [True, False])
def test_reuse_session_lock_failure(
    enable_runtime_env: bool, tmp_path: Path, project_test_data: Project
) -> None:
    os.environ["ANYSCALE_ENABLE_RUNTIME_ENV"] = "1" if enable_runtime_env else "0"
    scratch_dir = (tmp_path / "scratch").absolute().as_posix()
    builder, sdk, subprocess, ray = _make_test_builder(
        tmp_path, session_states=["Running"]
    )
    sdk.create_project.return_value = ProjectResponse(result=project_test_data)

    def create_session(*a: Any, **kw: Any) -> None:
        sess_resp = Mock()
        sess_resp.results = [
            _make_session(0, "Running"),
            _make_session(1, "Running"),
        ]
        sess_resp.metadata.next_paging_token = None
        sdk.list_sessions.return_value = sess_resp
        ray.util.connect.side_effect = _connected(ray, {})

    builder._up_session.side_effect = create_session
    builder._start_session.side_effect = create_session

    cluster_yaml = yaml.safe_load(anyscale.project.CLUSTER_YAML_TEMPLATE)
    builder._populate_cluster_config(cluster_yaml, "project_id", "scratch", build=None)
    with tempfile.NamedTemporaryFile(mode="w+", delete=False) as f:
        f.write(yaml.dump(cluster_yaml))
    import hashlib

    hasher = hashlib.sha1()
    hasher.update(yaml.dump(cluster_yaml).encode())
    local_config_hash = hasher.hexdigest().encode()
    # Emulate session hash code match but lock failure.
    ray.util.connect.side_effect = _connected(ray, {"num_clients": 9999999})
    ray.experimental.internal_kv._internal_kv_get.return_value = local_config_hash

    # Creates new session-1.
    builder.connect()

    if enable_runtime_env:
        builder._start_session.assert_called_once_with(
            project_id=project_test_data.id,
            session_name="session-1",
            cloud_name="anyscale_default_cloud",
            build_id=None,
            yaml_filepath=ANY,
        )
    else:
        builder._up_session.assert_called_once_with(
            project_test_data.id,
            "session-1",
            "anyscale_default_cloud",
            scratch_dir,
            dangerously_set_build_id=None,
            yaml_filepath=ANY,
        )


@pytest.mark.parametrize("enable_runtime_env", [True, False])
def test_restart_session_conn_failure(
    enable_runtime_env: bool, tmp_path: Path, project_test_data: Project
) -> None:
    os.environ["ANYSCALE_ENABLE_RUNTIME_ENV"] = "1" if enable_runtime_env else "0"
    scratch_dir = (tmp_path / "scratch").absolute().as_posix()
    builder, sdk, subprocess, ray = _make_test_builder(
        tmp_path, session_states=["Running"]
    )
    sdk.create_project.return_value = ProjectResponse(result=project_test_data)

    def fail_first_session(url: str, *a: Any, **kw: Any) -> Any:
        raise ConnectionError("mock connect failure")

    # Emulate session hash code match but conn failure.
    ray.util.connect.side_effect = fail_first_session

    # Tries to restart it, but fails.
    with pytest.raises(ConnectionError):
        builder.connect()

    if enable_runtime_env:
        builder._start_session.assert_called_once_with(
            project_id=project_test_data.id,
            session_name="session-1",
            cloud_name="anyscale_default_cloud",
            build_id=None,
            yaml_filepath=ANY,
        )
    else:
        builder._up_session.assert_called_once_with(
            project_test_data.id,
            "session-1",
            "anyscale_default_cloud",
            scratch_dir,
            dangerously_set_build_id=None,
            yaml_filepath=ANY,
        )


@pytest.mark.parametrize("enable_runtime_env", [True, False])
def test_fixed_session(
    enable_runtime_env: bool, tmp_path: Path, project_test_data: Project
) -> None:
    os.environ["ANYSCALE_ENABLE_RUNTIME_ENV"] = "1" if enable_runtime_env else "0"
    scratch_dir = (tmp_path / "scratch").absolute().as_posix()
    builder, sdk, subprocess, ray = _make_test_builder(
        tmp_path, session_states=["Running", "Running"]
    )
    sdk.create_project.return_value = ProjectResponse(result=project_test_data)

    # Should connect and run 'up'.
    builder.session("session-1", update=True).connect()

    if enable_runtime_env:
        builder._start_session.assert_called_once_with(
            project_id=project_test_data.id,
            session_name="session-1",
            cloud_name="anyscale_default_cloud",
            build_id=None,
            yaml_filepath=ANY,
        )
    else:
        builder._up_session.assert_called_once_with(
            project_test_data.id,
            "session-1",
            "anyscale_default_cloud",
            scratch_dir,
            dangerously_set_build_id=None,
            yaml_filepath=ANY,
        )


@pytest.mark.parametrize("enable_runtime_env", [True, False])
def test_fixed_session_not_running(
    enable_runtime_env: bool, tmp_path: Path, project_test_data: Project,
) -> None:
    os.environ["ANYSCALE_ENABLE_RUNTIME_ENV"] = "1" if enable_runtime_env else "0"
    scratch_dir = (tmp_path / "scratch").absolute().as_posix()
    builder, sdk, subprocess, ray = _make_test_builder(
        tmp_path, session_states=["Running", "Stopped"]
    )
    sdk.create_project.return_value = ProjectResponse(result=project_test_data)

    # Should connect and run 'up'.
    builder.session("session-1").connect()

    if enable_runtime_env:
        builder._start_session.assert_called_once_with(
            project_id=project_test_data.id,
            session_name="session-1",
            cloud_name="anyscale_default_cloud",
            build_id=None,
            yaml_filepath=ANY,
        )
    else:
        builder._up_session.assert_called_once_with(
            project_test_data.id,
            "session-1",
            "anyscale_default_cloud",
            scratch_dir,
            dangerously_set_build_id=None,
            yaml_filepath=ANY,
        )


@pytest.mark.parametrize("enable_runtime_env", [True, False])
def test_fixed_session_static_ray_version_mismatch(
    enable_runtime_env: bool, tmp_path: Path, project_test_data: Project,
) -> None:
    os.environ["ANYSCALE_ENABLE_RUNTIME_ENV"] = "1" if enable_runtime_env else "0"
    builder, sdk, subprocess, ray = _make_test_builder(
        tmp_path, session_states=["Running", "Stopped"]
    )
    sdk.create_project.return_value = ProjectResponse(result=project_test_data)
    ray.__commit__ = "fake_commit"

    # Should connect and not run 'up'.
    with pytest.raises(ValueError):
        builder.session("session-1").connect()

    builder._up_session.assert_not_called()


@pytest.mark.parametrize("enable_runtime_env", [True, False])
@pytest.mark.parametrize("remote_version_mismatch", [True, False])
def test_fixed_session_no_update(
    enable_runtime_env: bool,
    remote_version_mismatch: bool,
    tmp_path: Path,
    project_test_data: Project,
) -> None:
    os.environ["ANYSCALE_ENABLE_RUNTIME_ENV"] = "1" if enable_runtime_env else "0"
    builder, sdk, subprocess, ray = _make_test_builder(
        tmp_path, session_states=["Running", "Running"]
    )
    sdk.create_project.return_value = ProjectResponse(result=project_test_data)

    if remote_version_mismatch:
        ray.util.connect.side_effect = _connected(ray, {"ray_commit": "bad commit"},)

    # Should connect and run 'up'.
    if remote_version_mismatch:
        with pytest.raises(ValueError):
            builder.session("session-1", update=False).connect()
    else:
        builder.session("session-1", update=False).connect()

    builder._up_session.assert_not_called()
    builder._ray.util.connect.assert_called_once()


@pytest.mark.parametrize("enable_runtime_env", [True, False])
def test_new_fixed_session(
    enable_runtime_env: bool, tmp_path: Path, project_test_data: Project
) -> None:
    os.environ["ANYSCALE_ENABLE_RUNTIME_ENV"] = "1" if enable_runtime_env else "0"
    scratch_dir = (tmp_path / "scratch").absolute().as_posix()
    builder, sdk, subprocess, ray = _make_test_builder(tmp_path, session_states=[])
    sdk.create_project.return_value = ProjectResponse(result=project_test_data)

    def create_session(*a: Any, **kw: Any) -> None:
        sess_resp = Mock()
        sess_resp.results = [_make_session(i, "Running") for i in range(3)]
        sess_resp.metadata.next_paging_token = None
        sdk.list_sessions.return_value = sess_resp

    builder._up_session.side_effect = create_session
    builder._start_session.side_effect = create_session

    # Should create a new session.
    builder.session("session-2").connect()

    if enable_runtime_env:
        builder._start_session.assert_called_once_with(
            project_id=project_test_data.id,
            session_name="session-2",
            cloud_name="anyscale_default_cloud",
            build_id=None,
            yaml_filepath=ANY,
        )
    else:
        builder._up_session.assert_called_once_with(
            project_test_data.id,
            "session-2",
            "anyscale_default_cloud",
            scratch_dir,
            dangerously_set_build_id=None,
            yaml_filepath=ANY,
        )


class MockPopen(object):
    def __init__(self) -> None:
        pass

    def communicate(self) -> Tuple[str, str]:
        return (
            '[{"id": "cloud2", "name": "second cloud"}, {"id": "cloud1", "name": "first cloud"}]',
            "",
        )


@pytest.mark.parametrize("enable_runtime_env", [True, False])
@pytest.mark.parametrize("org_default_cloud", [None, "mock_cloud_id"])
def test_get_default_cloud(
    enable_runtime_env: bool,
    org_default_cloud: Optional[str],
    tmp_path: Path,
    project_test_data: Project,
) -> None:
    os.environ["ANYSCALE_ENABLE_RUNTIME_ENV"] = "1" if enable_runtime_env else "0"
    subprocess = Mock()
    subprocess.Popen.return_value = MockPopen()
    sdk = Mock()
    project_test_data.last_used_cloud_id = None
    sdk.get_project.return_value = ProjectResponse(result=project_test_data)
    _api_client = Mock()
    _api_client.get_user_info_api_v2_userinfo_get.return_value.result = Mock(
        organizations=[Mock(default_cloud_id=org_default_cloud)]
    )
    _api_client.get_cloud_api_v2_clouds_cloud_id_get.return_value.result.name = (
        "mock_cloud_name"
    )
    builder = ClientBuilder(
        anyscale_sdk=sdk, subprocess=subprocess, api_client=_api_client
    )
    if org_default_cloud:
        # Check the correct default cloud is returned
        assert builder._get_organization_default_cloud() == "mock_cloud_name"
    else:
        # Check that we get the "default cloud" (cloud first created)
        # if there is no last used cloud.
        assert builder._get_last_used_cloud("prj_1") == "first cloud"
        project_test_data.last_used_cloud_id = "cloud2"
        # If there is a last used cloud, use that instead.
        assert builder._get_last_used_cloud("prj_1") == "second cloud"


@pytest.mark.parametrize("enable_runtime_env", [True, False])
@pytest.mark.parametrize("static_ray_version_mismatch", [True, False])
@pytest.mark.parametrize("use_compute_config", [True, False])
def test_cluster_env(
    enable_runtime_env: bool,
    static_ray_version_mismatch: bool,
    use_compute_config: bool,
    tmp_path: Path,
    project_test_data: Project,
) -> None:
    os.environ["ANYSCALE_ENABLE_RUNTIME_ENV"] = "1" if enable_runtime_env else "0"
    os.environ["ANYSCALE_COMPUTE_CONFIG"] = "1" if use_compute_config else "0"
    scratch_dir = (tmp_path / "scratch").absolute().as_posix()
    builder, sdk, subprocess, ray = _make_test_builder(tmp_path, session_states=[])
    sdk.create_project.return_value = ProjectResponse(result=project_test_data)

    if static_ray_version_mismatch:
        ray.__commit__ = "abcdef"
        ray.util.connect.side_effect = _connected(ray, {"ray_commit": "abcdef"},)

    app_templates_resp = Mock()
    app_templates_resp.results = [_make_app_template()]
    app_templates_resp.metadata.next_paging_token = None
    sdk.list_app_configs.return_value = app_templates_resp

    build = _make_build()
    builds_resp = Mock()
    builds_resp.results = [build]
    builds_resp.metadata.next_paging_token = None
    sdk.list_builds.return_value = builds_resp

    get_build_resp = Mock()
    get_build_resp.result = build
    sdk.get_build.return_value = get_build_resp

    yaml_filepath = None

    def create_session(*a: Any, **kw: Any) -> None:
        nonlocal yaml_filepath
        yaml_filepath = kw["yaml_filepath"]
        sess_resp = Mock()
        sess_resp.results = [_make_session(0, "Running")]
        sess_resp.metadata.next_paging_token = None
        sdk.list_sessions.return_value = sess_resp

    builder._start_session.side_effect = create_session
    builder._up_session.side_effect = create_session

    with pytest.raises(RuntimeError):
        builder.cluster_env("non-existent-app-config").connect()
    with pytest.raises(TypeError):
        builder.cluster_env([])

    builder.cluster_env(
        {"name": "my_custom_image", "base_image": "anyscale/ray-ml:pinned-nightly"}
    )
    assert builder._cluster_env_name == "my_custom_image"
    assert builder._cluster_env_dict == {"base_image": "anyscale/ray-ml:pinned-nightly"}
    builder.cluster_env({"base_image": "anyscale/ray-ml:pinned-nightly"})
    assert builder._cluster_env_name is None
    assert builder._cluster_env_dict == {"base_image": "anyscale/ray-ml:pinned-nightly"}

    if use_compute_config and enable_runtime_env:
        with pytest.raises(RuntimeError):
            # Must provide build identifier if using compute config path and starting
            # session from sdk (with runtime env)
            builder.connect()
        builder.cluster_env(
            {"name": "test-app-config", "base_image": "anyscale/ray-ml:pinned-nightly"}
        ).connect()
    else:
        builder.cluster_env("test-app-config").connect()

    with open(cast(str, yaml_filepath)) as f:
        data = yaml.safe_load(f)

    assert data["docker"]["image"] == "localhost:5555/docker_image_name"
    for nodes_type, node_config in data["available_node_types"].items():
        assert (
            node_config["docker"]["worker_image"] == "localhost:5555/docker_image_name"
        )

    if enable_runtime_env:
        builder._start_session.assert_called_once_with(
            project_id=project_test_data.id,
            session_name="session-0",
            cloud_name="anyscale_default_cloud",
            build_id="build_id",
            yaml_filepath=ANY,
        )
    else:
        builder._up_session.assert_called_once_with(
            project_test_data.id,
            "session-0",
            "anyscale_default_cloud",
            scratch_dir,
            dangerously_set_build_id="build_id",
            yaml_filepath=ANY,
        )


def test_get_wheel_url() -> None:
    wheel_prefix = (
        "https://s3-us-west-2.amazonaws.com/ray-wheels/master/COMMIT_ID/ray-2.0.0.dev0"
    )
    assert (
        get_wheel_url("master/COMMIT_ID", "36", "darwin")
        == f"{wheel_prefix}-cp36-cp36m-macosx_10_13_intel.whl"
    )
    assert (
        get_wheel_url("master/COMMIT_ID", "37", "darwin")
        == f"{wheel_prefix}-cp37-cp37m-macosx_10_13_intel.whl"
    )
    assert (
        get_wheel_url("master/COMMIT_ID", "38", "darwin")
        == f"{wheel_prefix}-cp38-cp38-macosx_10_13_x86_64.whl"
    )

    assert (
        get_wheel_url("master/COMMIT_ID", "36", "linux")
        == f"{wheel_prefix}-cp36-cp36m-manylinux2014_x86_64.whl"
    )
    assert (
        get_wheel_url("master/COMMIT_ID", "37", "linux")
        == f"{wheel_prefix}-cp37-cp37m-manylinux2014_x86_64.whl"
    )
    assert (
        get_wheel_url("master/COMMIT_ID", "38", "linux")
        == f"{wheel_prefix}-cp38-cp38-manylinux2014_x86_64.whl"
    )

    assert (
        get_wheel_url("master/COMMIT_ID", "36", "win32")
        == f"{wheel_prefix}-cp36-cp36m-win_amd64.whl"
    )
    assert (
        get_wheel_url("master/COMMIT_ID", "37", "win32")
        == f"{wheel_prefix}-cp37-cp37m-win_amd64.whl"
    )
    assert (
        get_wheel_url("master/COMMIT_ID", "38", "win32")
        == f"{wheel_prefix}-cp38-cp38-win_amd64.whl"
    )


def test_commit_url_is_valid() -> None:
    for python_version in ["36", "37", "38"]:
        for pltfrm in ["win32", "linux", "darwin"]:
            url = get_wheel_url(
                "master/{}".format(REQUIRED_RAY_COMMIT), python_version, pltfrm
            )
            # We use HEAD, because it is faster than downloading with GET
            resp = requests.head(url)
            assert resp.status_code == 200, f"Cannot find wheel for: {url}"


def test_version_mismatch() -> None:
    sdk = Mock()
    _api_client = Mock()
    connect_instance = ClientBuilder(anyscale_sdk=sdk, api_client=_api_client)
    connect_instance_ignore = ClientBuilder(
        anyscale_sdk=sdk, _ignore_version_check=True, api_client=_api_client
    )

    both_wrong = ["1.1.0", "fake_commit"]
    commit_is_wrong = [REQUIRED_RAY_VERSION, REQUIRED_RAY_COMMIT[2:]]
    version_is_wrong = ["1.0.0", REQUIRED_RAY_COMMIT]
    for attempt in [both_wrong, version_is_wrong, commit_is_wrong]:
        with pytest.raises(ValueError):
            connect_instance._check_required_ray_version(*attempt)
        connect_instance_ignore._check_required_ray_version(*attempt)

    both_correct = [REQUIRED_RAY_VERSION, REQUIRED_RAY_COMMIT]
    connect_instance_ignore._check_required_ray_version(*both_correct)
    connect_instance._check_required_ray_version(*both_correct)


def test_set_metadata_in_job_config() -> None:
    sdk = Mock()
    _api_client = Mock()
    sdk.get_project.return_value = Mock(result=Mock(creator_id="mock_creator_id"))

    def mock_set_metadata(key: str, val: str) -> None:
        connect_instance._job_config.metadata[key] = val

    # Test no user specified job name
    connect_instance = ClientBuilder(anyscale_sdk=sdk, api_client=_api_client)
    connect_instance._enable_runtime_env = True
    connect_instance._job_config.metadata = {}
    connect_instance._job_config.set_metadata = mock_set_metadata
    connect_instance._set_metadata_in_job_config("mock_project_id")
    assert connect_instance._job_config.metadata["job_name"].startswith("job")
    assert connect_instance._job_config.metadata["creator_id"] == "mock_creator_id"

    # Test user specified job name
    connect_instance = ClientBuilder(anyscale_sdk=sdk, api_client=_api_client)
    connect_instance._enable_runtime_env = True
    connect_instance._job_config.metadata = {}
    connect_instance._job_config.set_metadata = mock_set_metadata
    connect_instance.job_name("mock_job_name")._set_metadata_in_job_config(
        "mock_project_id"
    )
    assert connect_instance._job_config.metadata["job_name"].startswith("mock_job_name")
    assert connect_instance._job_config.metadata["creator_id"] == "mock_creator_id"


def test_namespace() -> None:
    sdk = Mock()
    _api_client = Mock()

    # Test no user specified job name
    connect_instance = ClientBuilder(anyscale_sdk=sdk, api_client=_api_client)

    def mock_set_ray_namespace(namespace: str) -> None:
        connect_instance._job_config.ray_namespace = namespace

    connect_instance._job_config.set_ray_namespace = mock_set_ray_namespace
    connect_instance._enable_runtime_env = True
    connect_instance.namespace("mock_namespace")
    assert connect_instance._job_config.ray_namespace == "mock_namespace"


def test_set_runtime_env_in_job_config(
    tmp_path: Path, project_test_data: Project
) -> None:

    sdk = Mock()
    _api_client = Mock()
    connect_instance = ClientBuilder(anyscale_sdk=sdk, api_client=_api_client)
    connect_instance._job_config.set_runtime_env = Mock()
    connect_instance.env({"working_dir": "/tmp"})._set_runtime_env_in_job_config("/")
    assert connect_instance._job_config.runtime_env["working_dir"] == "/tmp"
    assert connect_instance._job_config.runtime_env["excludes"] == [
        ".git",
        "__pycache__",
        "/.anyscale.yaml",
        "/session-default.yaml",
    ]

    connect_instance = ClientBuilder(anyscale_sdk=sdk, api_client=_api_client)
    connect_instance._job_config.set_runtime_env = Mock()
    connect_instance.env({})._set_runtime_env_in_job_config("/tmp")
    assert connect_instance._job_config.runtime_env["working_dir"] == "/tmp"
    assert connect_instance._job_config.runtime_env["excludes"] == [
        ".git",
        "__pycache__",
        "/tmp/.anyscale.yaml",
        "/tmp/session-default.yaml",
    ]

    connect_instance = ClientBuilder(anyscale_sdk=sdk, api_client=_api_client)
    connect_instance._job_config.set_runtime_env = Mock()
    connect_instance.env(
        {"working_dir": "/tmp", "excludes": [".gitignore"], "pip_packages": ["numpy"]}
    )._set_runtime_env_in_job_config("/")
    assert connect_instance._job_config.runtime_env["working_dir"] == "/tmp"
    assert connect_instance._job_config.runtime_env["excludes"] == [
        ".git",
        "__pycache__",
        "/.gitignore",
        "/.anyscale.yaml",
        "/session-default.yaml",
    ]
    assert connect_instance._job_config.runtime_env["pip_packages"] == ["numpy"]

    os.environ["ANYSCALE_ENABLE_RUNTIME_ENV"] = "1"
    connect_instance, sdk, _, _ = _make_test_builder(tmp_path, [])
    sdk.create_project.return_value = ProjectResponse(result=project_test_data)

    connect_instance.env({"working_dir": "/tmp"}).connect()
    assert connect_instance._job_config.runtime_env["working_dir"] == "/tmp"
    excludes = [
        e.split("/")[-1] for e in connect_instance._job_config.runtime_env["excludes"]
    ]
    assert excludes == [
        ".git",
        "__pycache__",
        ".anyscale.yaml",
        "session-default.yaml",
    ]
    connect_instance._start_session.assert_called_once_with(  # type: ignore
        project_id=ANY,
        session_name="session-0",
        cloud_name="anyscale_default_cloud",
        build_id=None,
        yaml_filepath=ANY,
    )
    connect_instance._up_session.assert_not_called()  # type: ignore


def test_is_in_shell() -> None:
    def frame_mock(name: str) -> Any:
        mock = Mock()
        mock.filename = name
        return mock

    anycale_call_frames = [
        "/path/anyscale/connect.py",
        "/path/anyscale/connect.py",
        "/path/anyscale/__init__.py",
    ]

    ipython_shell = [
        "<ipython-input-2-f869cc61c5de>",
        "/home/ubuntu/anaconda3/envs/anyscale/bin/ipython",
    ]
    assert _is_in_shell(list(map(frame_mock, anycale_call_frames + ipython_shell)))

    python_shell = ["<stdin>"]
    assert _is_in_shell(list(map(frame_mock, anycale_call_frames + python_shell)))

    # Running file via `ipython random_file.py`
    ipython_from_file = [
        "random_file.py",
        "/home/ubuntu/anaconda3/envs/anyscale/bin/ipython",
    ]
    assert not _is_in_shell(
        list(map(frame_mock, anycale_call_frames + ipython_from_file))
    )

    # Running file via `python random_file.py`
    python_from_file = ["random_file.py"]
    assert not _is_in_shell(
        list(map(frame_mock, anycale_call_frames + python_from_file))
    )


@pytest.mark.skip(
    "This test is very, very long, and should only be run locally if connect.py::PINNED_IMAGES are updated"
)
def test_pinned_images() -> None:
    """
    This test should be run every time PINNED_IMAGES is changed in connect.py.
    This test ensures:
    - Python versions match.
    - Ray commits match.
    - CUDA is present for GPU images (determined by the presence of the file /usr/local/cuda)
    """
    for image, pinned_image in PINNED_IMAGES.items():
        cmd = "-c \"python --version; python -c 'import ray; print(ray.__commit__)'; ls -l 2>&1 /usr/local/cuda/bin/nvcc; anyscale --version\""
        print(f"Checking: {image} with SHA: {pinned_image} ")
        output = subprocess.run(  # noqa: B1
            f"docker run --rm -it --entrypoint=/bin/bash {pinned_image} {cmd}",
            shell=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
        )
        py_version, ray_commit, cuda_info, anyscale_version, _ = output.stdout.decode(
            "UTF-8"
        ).split("\n")

        _, desired_py_version, desired_arch = image.split(":")[-1].split("-")
        assert (
            desired_py_version[-1] in py_version
        ), f"Wrong python version found in {pinned_image}!"

        if desired_arch == "gpu":
            assert ("ls: cannot access" not in cuda_info) and (
                "nvcc" in cuda_info
            ), f"CUDA install incorrect in {pinned_image}"
        else:
            assert (
                "ls: cannot access"
            ) in cuda_info, f"CUDA found in CPU image {pinned_image}"

        assert (
            ray_commit.strip() == REQUIRED_RAY_COMMIT
        ), f"Wrong ray commit installed in {pinned_image}"

        assert (
            anyscale_version.strip() == anyscale.__version__
        ), f"Anyscale version is different than latest master in {pinned_image}"
