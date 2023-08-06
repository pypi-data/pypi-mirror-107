"""Anyscale connect implementation.

Here's an overview of how a connect call works. It goes through a few steps:
    1. Detecting the project and hashing the files
    2. Getting or creating a session
    3. Acquiring a session lock via the Ray client

Detecting the project: If the user is in a shell, we will create a
"scratch" project by default which is the empty directory. Otherwise, the
project must either be specified explicitly, or we autodetect it based on
the current working directory.

Getting or creating a session: Anyscale connect will look through the list of
sessions for the project and try to find one to connect to. If there are no
active sessions, or the session files hash (generated when the session was
created) is different from the local project hash, a session is
created / updated using "anyscale up".

A new session is 'created' when all other sessions are in-use, otherwise
an existing one is updated. Note that we perform this check while holding the
session lock (below) to avoid race conditions. However note that the
"anyscale up" part is not under the lock (this is a TODO).

Acquiring a session lock via the Ray client: To avoid multiple clients from
connecting to the same session, we acquire an exclusive lock on the session
before returning. This is done by checking that "num_clients" == 1 in the
returned connection info object, which means that we are the first client.
If we are not the first client, we disconnect from the session and try the
next one.
"""

import copy
from datetime import datetime, timezone
import getpass
import hashlib
import inspect
import json
import os
from pathlib import Path
import shlex
import subprocess
import sys
import tempfile
import time
from types import ModuleType
from typing import Any, Callable, cast, Dict, List, Optional, Tuple, Union
from urllib.parse import parse_qs, urlparse
import uuid

import colorama  # type: ignore
import requests
import yaml

from anyscale.api import get_api_client
from anyscale.client.openapi_client.api.default_api import DefaultApi
from anyscale.client.openapi_client.models.app_config import AppConfig
from anyscale.client.openapi_client.models.build import Build
from anyscale.client.openapi_client.models.session import Session
from anyscale.cloud import get_cloud_id_and_name
from anyscale.credentials import load_credentials
from anyscale.fingerprint import fingerprint
import anyscale.project
from anyscale.sdk.anyscale_client import (
    ComputeTemplateConfig,
    ComputeTemplateQuery,
    CreateComputeTemplate,
    CreateSession,
    StartSessionOptions,
    UpdateSession,
)
from anyscale.sdk.anyscale_client.sdk import AnyscaleSDK
from anyscale.util import get_endpoint, get_wheel_url, slugify, wait_for_session_start


# The default project directory to use, if no project is specified.
DEFAULT_SCRATCH_DIR = "~/.anyscale/scratch_{}".format(getpass.getuser())

# The key used to identify the session's latest file hash.
ANYSCALE_CONFIG_HASH = "anyscale.com/config_hash"

# Max number of auto created sessions.
MAX_SESSIONS = 20

# Default minutes for autosuspend.
DEFAULT_AUTOSUSPEND_TIMEOUT = 120

# The required Ray version on the client side.
REQUIRED_RAY_VERSION = "2.0.0.dev0"
REQUIRED_RAY_COMMIT = "9bdd2cbe4921a08040508dc2e0d0f465170383e2"

# The paths to exclude when syncing the working directory in runtime env.
EXCLUDE_DIRS = [".git", "__pycache__"]
EXCLUDE_PATHS = [".anyscale.yaml", "session-default.yaml"]

# The supported parameters that we can provide in the url.
# e.g url="anyscale://ameer?param1=val1&param2=val2"
CONNECT_URL_PARAMS = ["cluster_compute", "cluster_env", "autosuspend"]

# The type of the dict that can be passed to create a cluster env.
# e.g., {"base_image": "anyscale/ray-ml:1.1.0-gpu"}
CLUSTER_ENV_DICT_TYPE = Dict[str, Union[str, List[str]]]

# The cluster compute type. It can either be a string, eg my_template or a dict,
# eg, {"cloud_id": "id-123" ...}
CLUSTER_COMPUTE_DICT_TYPE = Dict[str, Any]

# Pin images to use on the server side.
# NOTE: If these are modified, `frontend/cli/tests/test_connect.py::test_pinned_images` must be run
# to verify that the new images use the right python version, CUDA files & ray commit!
# Instructions here: https://docs.google.com/document/d/1dsK4dzugvNgJebA4esOhloe3DpXqRVVhv_NlbDMqVJ4/
PINNED_IMAGES = {
    "anyscale/ray-ml:nightly-py36-cpu": "anyscale/ray-ml@sha256:439860c94e71facb13f0021e35494098440de4739ec6aa732280ce8e54106e15",
    "anyscale/ray-ml:nightly-py36-gpu": "anyscale/ray-ml@sha256:bac4c5216a78bf2a21e865079acf16d06b90a82d2ce7ebe73f1ea59f14f180b1",
    "anyscale/ray-ml:nightly-py37-cpu": "anyscale/ray-ml@sha256:abd9c1cd2c35a0ae35db6ec4dbf729efb81f0ca0c25c2009c59edb6baf4afad6",
    "anyscale/ray-ml:nightly-py37-gpu": "anyscale/ray-ml@sha256:12ca744055054baff6f1574ab6dea9d4e8ebd6f31cf8d61a4b736d3782c8778b",
    "anyscale/ray-ml:nightly-py38-cpu": "anyscale/ray-ml@sha256:116b9e42449fa0d3ce4094cd35d9bacbb01f678e6ed24e9b43fe8d967b650107",
    "anyscale/ray-ml:nightly-py38-gpu": "anyscale/ray-ml@sha256:425a193567e4ee1fd80515083c637f5b793342a931a5a0930788d020c4c04160",
    "anyscale/ray:nightly-py36-cpu": "anyscale/ray@sha256:9b98efa1159846a2ea3bbed3823bc0ce73022c633fb87809820235bc7d1f4237",
    "anyscale/ray:nightly-py36-gpu": "anyscale/ray@sha256:04f30ee16588836728eb59df4ba08269699932a4b8ead48562640044d68b2a98",
    "anyscale/ray:nightly-py37-cpu": "anyscale/ray@sha256:4c8e85867d3f322794896a254336a1a74f2b7aa11dad5a57b073fd17564d0dc1",
    "anyscale/ray:nightly-py37-gpu": "anyscale/ray@sha256:2ad00534e67c84834495344a699f83b8ccf288fc8c85ae78761539559814329b",
    "anyscale/ray:nightly-py38-cpu": "anyscale/ray@sha256:e12ccf67291bb554257a56e717e6978ad88f3453ade373c2871d1e80b5871529",
    "anyscale/ray:nightly-py38-gpu": "anyscale/ray@sha256:802f2694cd1e78220424b6785fb92a0f7ce9d09b51b8180b771a7f97a0ddb9b1",
}

# Commands used to build Ray from source. Note that intermediate stages will
# be cached by the app config builder.
BUILD_STEPS = [
    "git clone https://github.com/ray-project/ray.git",
    "curl -fsSL https://bazel.build/bazel-release.pub.gpg | gpg --dearmor > bazel.gpg",
    "sudo mv bazel.gpg /etc/apt/trusted.gpg.d/",
    'echo "deb [arch=amd64] https://storage.googleapis.com/bazel-apt stable jdk1.8" | sudo tee /etc/apt/sources.list.d/bazel.list',
    "sudo apt-get update && sudo apt-get install -y bazel=3.2.0",
    'cd ray/python && sudo env "PATH=$PATH" python setup.py develop',
    "pip uninstall -y ray",
]


# Default docker images to use for connect sessions.
def _get_base_image(cpu_or_gpu: str = "cpu") -> str:
    py_version = "".join(str(x) for x in sys.version_info[0:2])
    if py_version not in ["36", "37", "38"]:
        raise ValueError("No default docker image for py{}".format(py_version))
    key = "anyscale/ray-ml:nightly-py{}-{}".format(py_version, cpu_or_gpu)
    if "ANYSCALE_NIGHTLY_IMAGES" in os.environ:
        return key
    else:
        return PINNED_IMAGES[key]


def _get_interactive_shell_frame(frames: Optional[List[Any]] = None) -> Optional[Any]:
    if frames is None:
        frames = inspect.getouterframes(inspect.currentframe())

    first_non_anyscale = None

    for i, frame in enumerate(frames):
        if "anyscale" not in frame.filename:
            first_non_anyscale = i
            break

    if first_non_anyscale is None:
        return None

    return frames[first_non_anyscale]


def _is_in_shell(frames: Optional[List[Any]] = None) -> bool:
    """
    Determines whether we are in a Notebook / shell.
    This is done by inspecting the first non-Anyscale related frame.
    If this is from an interactive terminal it will be either STDIN or IPython's Input.
    If connect() is being run from a file (like python myscript.py), frame.filename will equal "myscript.py".
    """
    fr = _get_interactive_shell_frame(frames)

    if fr is None:
        return False

    is_ipython = fr.filename.startswith("<ipython-input") and fr.filename.endswith(">")
    is_regular_python_shell: bool = fr.filename == "<stdin>"
    return is_regular_python_shell or is_ipython


class _ConsoleLog:
    def __init__(self) -> None:
        self.t0 = time.time()

    def zero_time(self) -> None:
        self.t0 = time.time()

    def info(self, *msg: Any) -> None:
        print(
            "{}{}(anyscale +{}){} ".format(
                colorama.Style.BRIGHT,
                colorama.Fore.CYAN,
                self._time_string(),
                colorama.Style.RESET_ALL,
            ),
            end="",
        )
        print(*msg)

    def debug(self, *msg: str) -> None:
        if os.environ.get("ANYSCALE_DEBUG") == "1":
            print(
                "{}{}(anyscale +{}){} ".format(
                    colorama.Style.DIM,
                    colorama.Fore.CYAN,
                    self._time_string(),
                    colorama.Style.RESET_ALL,
                ),
                end="",
            )
            print(*msg)

    def error(self, *msg: str) -> None:
        print(
            "{}{}(anyscale +{}){} ".format(
                colorama.Style.BRIGHT,
                colorama.Fore.RED,
                self._time_string(),
                colorama.Style.RESET_ALL,
            ),
            end="",
        )
        print(*msg)

    def warning(self, *msg: str) -> None:
        print(
            "{}{}(anyscale +{}){} ".format(
                colorama.Style.NORMAL,
                colorama.Fore.YELLOW,
                self._time_string(),
                colorama.Style.RESET_ALL,
            ),
            end="",
        )
        print(*msg)

    def _time_string(self) -> str:
        delta = time.time() - self.t0
        hours = 0
        minutes = 0
        while delta > 3600:
            hours += 1
            delta -= 3600
        while delta > 60:
            minutes += 1
            delta -= 60
        output = ""
        if hours:
            output += "{}h".format(hours)
        if minutes:
            output += "{}m".format(minutes)
        output += "{}s".format(round(delta, 1))
        return output


class ClientBuilder:
    """This class lets you set session options and connect to Anyscale.

    It should not be constructed directly, but instead via ray.client("anyscale://").* methods
    exported at the package level.

    Examples:
        >>> # Raw client, creates new session on behalf of user
        >>> ray.client("anyscale://").connect()

        >>> # Get or create a named session
        >>> ray
        ...   .client("anyscale://my_named_session")
        ...   .connect()

        >>> # Specify a previously created cluster environment
        >>> ray
        ...   .client("anyscale://<cluster-name>?cluster_compute=compute:1")
        ...   .cluster_env(prev_created_config:2")
        ...   .autosuspend(hours=2)
        ...   .connect()

        >>> # Create new session from local env / from scratch
        >>> ray
        ...   .client("anyscale://<cluster-name>")
        ...   .project_dir("~/dev/my-project-folder")
        ...   .connect()

        >>> # Ray client connect is setup automatically
        >>> @ray.remote
        ... def my_func(value):
        ...   return value ** 2

        >>> # Remote functions are executed in the Anyscale session
        >>> print(ray.get([my_func.remote(x) for x in range(5)]))
        >>> [0, 1, 4, 9, 16]
    """

    def __init__(
        self,
        address: Optional[str] = None,
        scratch_dir: str = DEFAULT_SCRATCH_DIR,
        anyscale_sdk: AnyscaleSDK = None,
        subprocess: ModuleType = subprocess,
        requests: ModuleType = requests,
        _ray: Optional[ModuleType] = None,
        log: Any = _ConsoleLog(),
        _os: ModuleType = os,
        _ignore_version_check: bool = False,
        api_client: DefaultApi = None,
    ) -> None:

        # If we are running in an anyscale session, or IGNORE_VERSION_CHECK is set,
        # skip the pinned versions
        if "IGNORE_VERSION_CHECK" in os.environ or "ANYSCALE_SESSION_ID" in os.environ:
            _ignore_version_check = True

        self._use_compute_config = False
        self._enable_runtime_env = False
        enable_runtime_env = os.environ.get("ANYSCALE_ENABLE_RUNTIME_ENV")
        if enable_runtime_env is not None and enable_runtime_env != "0":
            self._enable_runtime_env = True
            from anyscale.utils.runtime_env import (
                runtime_env_setup as s3_runtime_env_setup,
            )

            s3_runtime_env_setup()
            anyscale.utils.runtime_env.logger = log
            if os.environ.get("ANYSCALE_COMPUTE_CONFIG") == "1":
                self._use_compute_config = True

        # Class dependencies.
        self._log = log
        self._anyscale_sdk: AnyscaleSDK = None
        self._credentials = None
        if anyscale_sdk:
            self._anyscale_sdk = anyscale_sdk
        else:
            self._credentials = load_credentials()
            self._log.debug("Using host {}".format(anyscale.conf.ANYSCALE_HOST))
            self._log.debug("Using credentials {}".format(self._credentials[:6]))
            self._anyscale_sdk = AnyscaleSDK(
                self._credentials, os.path.join(anyscale.conf.ANYSCALE_HOST, "ext")
            )
        if api_client is None:
            api_client = get_api_client()
        self._api_client = api_client
        if not _ray:
            try:
                import ray
            except ModuleNotFoundError:
                raise RuntimeError(
                    "Ray is not installed. Please install with: \n"
                    "pip install -U --force-reinstall `python -m anyscale.connect required_ray_version`"
                )
            _ray = ray
        self._ray: Any = _ray
        self._subprocess: Any = subprocess
        self._os: Any = _os
        self._requests: Any = requests

        self._in_shell = _is_in_shell()
        self._ignore_version_check = _ignore_version_check

        # Builder args.
        self._scratch_dir: str = scratch_dir
        self._ray_release: Optional[str] = None
        self._project_dir: Optional[str] = None
        self._project_name: Optional[str] = None
        self._cloud_name: Optional[str] = None
        self._session_name: Optional[str] = None
        self._base_docker_image: Optional[str] = None
        self._requirements: Optional[str] = None
        self._cluster_compute_name: Optional[str] = None
        self._cluster_compute_dict: Optional[CLUSTER_COMPUTE_DICT_TYPE] = None
        self._cluster_env_name: Optional[str] = None
        self._cluster_env_dict: Optional[CLUSTER_ENV_DICT_TYPE] = None
        self._cluster_env_revision: Optional[int] = None
        self._initial_scale: List[Dict[str, float]] = []
        self._autosuspend_timeout = DEFAULT_AUTOSUSPEND_TIMEOUT
        self._run_mode: Optional[str] = None
        self._build_commit: Optional[str] = None
        self._build_pr: Optional[int] = None
        self._force_rebuild: bool = False
        self._job_config = self._ray.job_config.JobConfig()
        # Override default run mode.
        if "ANYSCALE_BACKGROUND" in os.environ:
            self._run_mode = "background"
            self._log.debug(
                "Using `run_mode=background` since ANYSCALE_BACKGROUND is set"
            )
        elif "ANYSCALE_LOCAL_DOCKER" in os.environ:
            self._run_mode = "local_docker"
            self._log.debug(
                "Using `run_mode=local_docker` since ANYSCALE_LOCAL_DOCKER is set"
            )

        if self._use_compute_config and self._enable_runtime_env:
            self._log.debug(
                "Using compute_config to start session with sdk since "
                "ANYSCALE_COMPUTE_CONFIG and ANYSCALE_ENABLE_RUNTIME_ENV are set."
            )

        # Whether to update the session when connecting to a fixed session.
        self._needs_update: bool = True
        self._parse_address(address)

    def _parse_address(self, address: Optional[str]) -> None:
        """Parses the anyscale address and sets parameters on this builder.
        Eg, address="<cluster-name>?cluster_compute=my_template&autosuspend=5&cluster_env=bla:1
        """
        if address is None or not address:
            return
        parsed_result = urlparse(address)

        # Parse the cluster name. e.g., what is before the question mark in the url.
        cluster_name = parsed_result.path
        if cluster_name:
            self.session(cluster_name)

        # parse the parameters (what comes after the question mark)
        # parsed_result.query here looks like "param1=val1&param2=val2"
        # params_dict looks like:
        # {'cluster_compute': ['my_template'], 'autosuspend': ['5'], 'cluster_env': ['bla:1']}.
        params_dict: Dict[str, Any] = parse_qs(parsed_result.query)
        for key, val in params_dict.items():
            if key == "autosuspend":
                self.autosuspend(minutes=int(val[0]))
            elif key == "cluster_env":
                self.cluster_env(val[0])
            elif key == "cluster_compute":
                self.cluster_compute(val[0])
            else:
                raise ValueError(
                    "Provided parameter in the anyscale address is "
                    f"{key}. The supported parameters are: {CONNECT_URL_PARAMS}."
                )

    def env(self, runtime_env: Dict[str, Any]) -> "ClientBuilder":
        """Sets the custom user specified runtime environment dict.
        Examples:
            >> ray.client("anyscale://cluster_name").env({"pip": "./requirements.txt"}).connect()
            >> ray.client("anyscale://cluster_name").env({"pip": ["chess"]}).connect()
            >> ray.client("anyscale://cluster_name").env({"conda": "conda.yaml"}).connect()
        """

        if type(runtime_env) != dict:
            raise TypeError("runtime_env argument type should be dict.")
        self._job_config.runtime_env = copy.deepcopy(runtime_env)
        return self

    def namespace(self, namespace: str) -> "ClientBuilder":
        """
        Sets the namespace in the job config.
        Example:
            >> ray.client("anyscale://cluster_name").namespace("training_namespace").connect()
        """
        if self._enable_runtime_env:
            self._job_config.set_ray_namespace(namespace)
        return self

    def job_name(self, job_name: Optional[str] = None) -> "ClientBuilder":
        """
        Sets the job_name so the user can identify it in the UI. This is just a UI concept.
        Example:
            >>> ray.client("anyscale://cluster_name").job_name("production_job").connect()
        """
        if self._enable_runtime_env:
            current_time_str = datetime.now(timezone.utc).strftime("%m-%d-%Y-%H-%M-%S")
            job_name = (
                f"{job_name}-{current_time_str}"
                if job_name
                else f"job-{current_time_str}"
            )
            self._job_config.set_metadata("job_name", job_name)
        return self

    def _set_runtime_env_in_job_config(self, project_dir: str) -> None:
        """Configures the runtime env inside self._job_config."""
        self._log.info(
            "Runtime environment is enabled, "
            "to disable it, set ANYSCALE_ENABLE_RUNTIME_ENV=0"
        )
        if "working_dir" not in self._job_config.runtime_env:
            self._job_config.runtime_env["working_dir"] = project_dir
        if "excludes" not in self._job_config.runtime_env:
            self._job_config.runtime_env["excludes"] = []
        self._job_config.runtime_env["excludes"] = EXCLUDE_DIRS + [
            os.path.join(project_dir, path)
            for path in (self._job_config.runtime_env["excludes"] + EXCLUDE_PATHS)
        ]

        if not self._ignore_version_check:
            ray_release = "master/" + REQUIRED_RAY_COMMIT
        else:
            branch = os.environ.get("USE_RAY_BRANCH") or "master"
            ray_release = f"{branch}/{self._ray.__commit__}"
        runtime_env = self._job_config.runtime_env
        runtime_env["_ray_release"] = ray_release

        working_dir = Path(runtime_env["working_dir"])
        pip_config = runtime_env.get("pip")
        conda_config = runtime_env.get("conda")

        if pip_config is not None and conda_config is not None:
            raise ValueError(
                "The 'pip' field and 'conda' field of "
                "runtime_env cannot both be specified.  To use "
                "pip with conda, please only set the 'conda' "
                "field, and specify your pip dependencies "
                "within the conda YAML config dict: see "
                "https://conda.io/projects/conda/en/latest/"
                "user-guide/tasks/manage-environments.html"
                "#create-env-file-manually"
            )
        if pip_config is not None:
            if isinstance(pip_config, str):
                pip_file = Path(pip_config)
                if not pip_file.is_absolute():
                    pip_file = working_dir / pip_file
                if not pip_file.is_file():
                    raise ValueError(f"{pip_file} is not a valid file")
                runtime_env["pip"] = pip_file.read_text()
            elif isinstance(pip_config, list) and all(
                isinstance(dep, str) for dep in pip_config
            ):
                runtime_env["pip"] = "\n".join(pip_config) + "\n"
            else:
                raise TypeError(
                    "runtime_env['pip'] must be of type str or " "List[str]"
                )

        if conda_config is not None:
            if not isinstance(conda_config, dict):
                yaml_file = Path(conda_config)
                if yaml_file.suffix in (".yaml", ".yml"):
                    if not yaml_file.is_absolute():
                        yaml_file = working_dir / yaml_file
                    if not yaml_file.is_file():
                        raise ValueError(f"Can't find conda file {yaml_file}")
                    try:
                        runtime_env["conda"] = yaml.load(yaml_file.read_text())
                    except Exception as e:
                        raise ValueError(
                            f"Invalid conda file {yaml_file} with error {e}"
                        )
                else:
                    self._log.info(f"Using pre installed conda env: {conda_config}")
            deps = runtime_env["conda"].get("dependencies")
            if any([d.startswith("python=") for d in deps if isinstance(d, str)]):
                raise ValueError(
                    "Currently we don't support specify python verion. The python in the cluster will be used automatically"
                )
        self._job_config.set_runtime_env(runtime_env)

    def _set_metadata_in_job_config(self, project_id: str) -> None:
        """
        Specify creator_id in job config. This is needed so the job
        can correctly be created in the database. Specify default job name
        if not user provided. This will be displayed in the UI.
        """
        if self._enable_runtime_env:
            project = self._anyscale_sdk.get_project(project_id).result
            # TODO(nikita): A customer can spoof this value and pretend to be someone else.
            # Fix this once we have a plan for verification.
            self._job_config.set_metadata("creator_id", project.creator_id)
            if "job_name" not in self._job_config.metadata:
                self.job_name()

    def connect(self) -> None:  # noqa
        """Connect to Anyscale using previously specified options.

        Examples:
            >>> ray.client("anyscale://cluster_name").connect()
        """
        ray = self._ray  # noqa F841
        from ray.autoscaler import sdk as ray_autoscaler_sdk

        # TODO(ekl) check for duplicate connections
        self._log.zero_time()

        if self._ray.util.client.ray.is_connected():
            raise RuntimeError(
                "Already connected to a Ray session, please "
                "run anyscale.connect in a new Python process."
            )

        # Allow the script to be run on the head node as well.
        if "ANYSCALE_SESSION_ID" in os.environ:
            self._ray.init(address="auto")
            return

        # Re-exec in the docker container.
        if self._run_mode == "local_docker":
            self._exec_self_in_local_docker()

        # Autodetect or create a scratch project.
        if self._project_dir is None:
            self._project_dir = anyscale.project.find_project_root(os.getcwd())
        if self._project_dir:
            self._ensure_project_setup_at_dir(self._project_dir, self._project_name)
        elif self._in_shell:
            self._project_dir = self._get_or_create_scratch_project()
        else:
            raise ValueError(
                "The current working directory is not associated with an "
                "Anyscale project. Please run ``anyscale init`` to setup a "
                "new project or specify ``.project_dir()`` prior to "
                "connecting. Anyscale Connect uses the project directory "
                "to find the Python code dependencies for your script."
            )

        proj_def = anyscale.project.ProjectDefinition(self._project_dir)
        project_id = anyscale.project.get_project_id(proj_def.root)
        self._set_metadata_in_job_config(project_id)
        self._log.info("Using project dir", proj_def.root)

        # TODO(ekl): generate a serverless compute configuraton here.
        cluster_yaml = yaml.safe_load(anyscale.project.CLUSTER_YAML_TEMPLATE)

        # handles building from sources. This is very hacky. TODO(ameer/nikita/Ian): refactor!
        if self._build_pr or self._build_commit:
            self._cluster_env_name = self._build_app_config_from_source(project_id)

        # connect() in general is very hacky. TODO(ameer/nikita/Ian): refactor!
        if self._cluster_env_dict:
            self._log.info("building new docker image for the provided cluster env ...")
            # Replacing ":" with "-" because the cluster env name cannot include ":"
            self._cluster_env_name = (
                self._cluster_env_name
                or "anonymous_cluster_env-{}".format(
                    datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
                )
            )
            self._anyscale_sdk.create_app_config(
                {
                    "name": self._cluster_env_name,
                    "project_id": project_id,
                    "config_json": self._cluster_env_dict,
                }
            )
        build = (
            self._get_app_config_build(
                project_id, self._cluster_env_name, self._cluster_env_revision
            )
            if self._cluster_env_name
            else None
        )

        if self._session_name is not None:
            sess = self._get_session(project_id, self._session_name)
            if not sess or sess.state != "Running":
                # Unconditionally create the session if it isn't up.
                needs_up = True
            else:
                needs_up = self._needs_update

        else:
            needs_up = True

        cluster_yaml = self._populate_cluster_config(
            cluster_yaml,
            project_id,
            self._anyscale_sdk.get_project(project_id).result.name,
            build=build,
            needs_up=needs_up,
        )
        with tempfile.NamedTemporaryFile(mode="w+", delete=False) as tmp_file:
            tmp_file.write(yaml.dump(cluster_yaml))
            yaml_filepath = tmp_file.name

        if self._enable_runtime_env:
            self._set_runtime_env_in_job_config(self._project_dir)

            with open(yaml_filepath) as f:
                import hashlib

                hasher = hashlib.sha1()
                hasher.update(f.read().encode())
                config_hash = hasher.hexdigest().encode()
        else:
            self._log.info(
                "Runtime environment is disabled, "
                "to enable it, set ANYSCALE_ENABLE_RUNTIME_ENV=1"
            )
            self._job_config = None
            config_hash = self._fingerprint(proj_def.root, yaml_filepath).encode()

        # Locate a updated session and update it if needed.
        if needs_up:
            self._session_name = self._get_or_create_updated_session(
                config_hash,
                project_id,
                self._session_name,
                build_id=build.id if build else None,
                yaml_filepath=yaml_filepath,
            )
        else:
            # Appeases mypy, this is guaranteed based on how `needs_up` is set
            assert self._session_name
            # session name was set but doesn't need an update
            sess = self._get_session_or_die(project_id, self._session_name)
            self._acquire_session_lock(
                sess, raise_connection_error=True, connection_retries=0
            )

        # Connect Ray client.
        self._check_connection(project_id, self._session_name)

        # Issue request resources call.
        if self._initial_scale:
            self._log.debug("Calling request_resources({})".format(self._initial_scale))
            ray_autoscaler_sdk.request_resources(bundles=self._initial_scale)

        # Define ray in the notebook automatically for convenience.
        try:
            fr = _get_interactive_shell_frame()
            if self._in_shell and fr is not None and "ray" not in fr.frame.f_globals:
                self._log.debug("Auto importing Ray into the notebook.")
                fr.frame.f_globals["ray"] = self._ray
        except Exception as e:
            self._log.error("Failed to auto define `ray` in notebook", e)

        # If in background mode, execute the job in the remote session.
        if self._run_mode == "background":
            self._exec_self_in_head_node()

    def cloud(self, cloud_name: str) -> "ClientBuilder":
        """Set the name of the cloud to be used.

        This sets the name of the cloud that your connect session will be
        started in. If you do not specify it, it will use the last used cloud
        in this project.

        Args:
            cloud_name (str): Name of the cloud to start the session in.

        Examples:
            >>> ray.client("anyscale://cluster_name").cloud("aws_test_account").connect()
        """
        self._cloud_name = cloud_name
        return self

    def project_dir(
        self, local_dir: str, name: Optional[str] = None
    ) -> "ClientBuilder":
        """Set the project directory.

        This sets the project code directory that will be synced to all nodes
        in the cluster as required by Ray. If not specified, the project
        directory will be autodetected based on the current working directory.
        If no Anyscale project is found, a "scratch" project will be used.

        Args:
            local_dir (str): path to the project directory.
            name (str): optional name to use if the project doesn't exist.

        Examples:
            >>> anyscale.project_dir("~/my-proj-dir").connect()
        """
        self._project_dir = os.path.abspath(os.path.expanduser(local_dir))
        self._project_name = name
        return self

    def session(self, session_name: str, update: bool = True) -> "ClientBuilder":
        """Set a fixed session name.

        Setting a fixed session name will create a new session if a session
        with session_name does not exist. Otherwise it will reconnect to an existing
        session and update it if necessary.

        Args:
            session_name (str): fixed name of the session.
            update (bool): whether to update session configurations when
                connecting to an existing session. Note that this may restart
                the Ray runtime. By default update is set to True.

        Examples:
            >>> anyscale.session("prod_deployment", update=False).connect()
        """
        slugified_name = slugify(session_name)
        if slugified_name != session_name:
            self._log.error(
                f"Using `{slugified_name}` as the session name (instead of `{session_name}`)"
            )

        self._needs_update = update
        self._session_name = slugified_name

        return self

    def run_mode(self, run_mode: Optional[str] = None) -> "ClientBuilder":
        """Re-exec the driver program in the remote session or local docker.

        By setting ``run_mode("background")``, you can tell Anyscale connect
        to run the program driver remotely in the head node instead of executing
        locally. This allows you to e.g., close your laptop during development
        and have the program continue executing in the cluster.

        By setting ``run_mode("local_docker")``, you can tell Anyscale connect
        to re-exec the program driver in a local docker image, ensuring the
        driver environment will exactly match that of the remote session.

        You can also change the run mode by setting the ANYSCALE_BACKGROUND=1
        or ANYSCALE_LOCAL_DOCKER=1 environment variables. Changing the run mode
        is only supported for script execution. Attempting to change the run
        mode in a notebook or Python shell will raise an error.

        Args:
            run_mode (str): either None, "background", or "local_docker".

        Examples:
            >>> anyscale.run_mode("background").connect()
        """
        if run_mode not in [None, "background", "local_docker"]:
            raise ValueError("Unknown run mode {}".format(run_mode))
        if self._in_shell:
            if run_mode == "background":
                raise ValueError("Background mode is not supported in Python shells.")
            if run_mode == "local_docker":
                raise ValueError("Local docker mode is not supported in Python shells.")
        self._run_mode = run_mode
        return self

    def base_docker_image(self, image_name: str) -> "ClientBuilder":
        """Set the docker image to use for the session.

        IMPORTANT: the Python minor version of the manually specified docker
        image must match the local Python version.

        Args:
            image_name (str): docker image name.

        Examples:
            >>> anyscale.base_docker_image("anyscale/ray-ml:latest").connect()
        """
        if self._use_compute_config:
            raise ValueError(
                "Cannot specify base_docker_image when using compute configs "
                "(because ANYSCALE_COMPUTE_CONFIG=1). Please specify a build id instead."
            )
        self._base_docker_image = image_name

        return self

    def require(self, requirements: Union[str, List[str]]) -> "ClientBuilder":
        """Set the Python requirements for the session.

        Args:
            requirements: either be a list of pip library specifications, or
            the path to a requirements.txt file.

        Examples:
            >>> anyscale.require("~/proj/requirements.txt").connect()
            >>> anyscale.require(["gym", "torch>=1.4.0"]).connect()
        """
        if isinstance(requirements, str):
            with open(requirements, "r") as f:
                data = f.read()
            # Escape quotes
            self._requirements = data.replace('"', r"\"")
        else:
            assert isinstance(requirements, list)
            self._requirements = "\n".join(requirements)

        return self

    def cluster_compute(
        self, cluster_compute: Union[str, CLUSTER_COMPUTE_DICT_TYPE]
    ) -> "ClientBuilder":
        """Set the Anyscale cluster compute to use for the cluster.

        Args:
            cluster_compute: Name of the cluster compute
            or a dictionary to build a new cluster compute.
            For example "my-cluster-compute".

        Examples:
            >>> ray.client("anyscale://").cluster_compute("my_cluster_compute").connect()
            >>> ray.client("anyscale://").cluster_compute({"cloud_id": "1234", ... }).connect()
        """
        if type(cluster_compute) == str:
            self._cluster_compute_name = cluster_compute  # type: ignore
        elif type(cluster_compute) == dict:
            self._cluster_compute_dict = copy.deepcopy(cluster_compute)  # type: ignore
        else:
            raise TypeError(
                "cluster_compute should either be Dict[str, Any] or a string."
            )
        return self

    def cluster_env(
        self, cluster_env: Union[str, CLUSTER_ENV_DICT_TYPE]
    ) -> "ClientBuilder":
        """TODO(ameer): remove app_config below after a few releases.
        Set the Anyscale cluster environment to use for the cluster.

        IMPORTANT: the Python minor version of the manually specified cluster
        environment must match the local Python version, and the Ray version must
        also be compatible with the one on the client.

        Args:
            cluster_env: Name (and optionally revision) of
            the cluster environment or a dictionary to build a new cluster environment.
            For example "my_app_config:2" where the revision would be 2.
            If no revision is specified, use the latest revision.

        Examples:
            >>> ray.client("anyscale://").cluster_env("prev_created_config:2").connect()
            >>> ray.client("anyscale://").cluster_env({"base_image": "anyscale/ray-ml:1.1.0-gpu"}).connect()
        """
        self.app_config(cluster_env)
        return self

    def app_config(
        self, cluster_env: Union[str, CLUSTER_ENV_DICT_TYPE],
    ) -> "ClientBuilder":
        """Set the Anyscale app config to use for the session.

        IMPORTANT: the Python minor version of the manually specified app
        config must match the local Python version, and the Ray version must
        also be compatible with the one on the client.

        Args:
            cluster_env: Name (and optionally revision) of
            the cluster environment or a dictionary to build a new cluster environment.
            For example "my_cluster_env:2" where the revision would be 2.
            If no revision is specified, use the latest revision.

        Examples:
            >>> anyscale.app_config("prev_created_config:2").connect()
        """

        if self._build_commit or self._build_pr:
            raise ValueError("app_config() conflicts with build_from_source()")
        if type(cluster_env) == str:
            components = cluster_env.rsplit(":", 1)  # type: ignore
            self._cluster_env_name = components[0]
            if len(components) == 1:
                self._cluster_env_revision = None
            else:
                self._cluster_env_revision = int(components[1])
        elif type(cluster_env) == dict:
            cluster_env_copy: CLUSTER_ENV_DICT_TYPE = copy.deepcopy(cluster_env)  # type: ignore
            self._cluster_env_name = cluster_env_copy.pop("name", None)  # type: ignore
            self._cluster_env_dict = cluster_env_copy
        else:
            raise TypeError("The type of cluster_env must be either a str or a dict.")
        return self

    def download_results(
        self, *, remote_dir: str, local_dir: str, autosync: bool = False
    ) -> "ClientBuilder":
        """Specify a directory to sync down from the cluster head node.

        Args:
            remote_dir (str): the remote result dir on the head node.
            local_dir (str): the local path to sync results to.
            autosync (bool): whether to sync the files continuously. By
                default, results will only be synced on job completion.

        Examples:
            >>> ray.client("anyscale://cluster_name")
            ...   .download_results(
            ...       remote_dir="~/ray_results", remote_dir="~/proj_output",
            ...       autosync=True)
            ...   .connect()
        """
        raise NotImplementedError()

    def autosuspend(
        self,
        enabled: bool = True,
        *,
        hours: Optional[int] = None,
        minutes: Optional[int] = None,
    ) -> "ClientBuilder":
        """Configure or disable session autosuspend behavior.

        The session will be autosuspend after the specified time period. By
        default, sessions auto terminate after one hour of idle.

        Args:
            enabled (bool): whether autosuspend is enabled.
            hours (int): specify idle time in hours.
            minutes (int): specify idle time in minutes. This is added to the
                idle time in hours.

        Examples:
            >>> ray.client("anyscale://cluster_name").autosuspend(False).connect()
            >>> ray.client("anyscale://cluster_name?autosuspend=10").connect()  # 10 minutes
            >>> ray.client("anyscale://cluster_name").autosuspend(hours=1, minutes=30).connect()
        """
        if enabled:
            if hours is None and minutes is None:
                timeout = DEFAULT_AUTOSUSPEND_TIMEOUT
            else:
                timeout = 0
                if hours is not None:
                    timeout += hours * 60
                if minutes is not None:
                    timeout += minutes
        else:
            timeout = -1
        self._autosuspend_timeout = timeout
        return self

    def nightly_build(self, git_commit: str) -> "ClientBuilder":
        """Use the specified nightly build commit for the session runtime.

        This is an experimental feature.

        Args:
            git_commit (str): git commit of the nightly Ray release.

        Examples:
            >>> anyscale
            ...   .nightly_build("f1e293c6997d1b14d61b8ca05965af42ae59d285")
            ...   .connect()
        """
        if len(git_commit) != 40:
            raise ValueError("Ray git commit hash must be 40 chars long")
        self._ray_release = "master/{}".format(git_commit)
        url = get_wheel_url(self._ray_release)
        request = self._requests.head(url)
        if request.status_code != 200:
            raise ValueError(
                "Could not locate wheel in S3 (HTTP {}): {}".format(
                    request.status_code, url
                )
            )
        return self

    def build_from_source(
        self,
        *,
        git_commit: Optional[str] = None,
        github_pr_id: Optional[int] = None,
        force_rebuild: bool = False,
    ) -> "ClientBuilder":
        """Build Ray from source for the session runtime.

        This is an experimental feature.

        Note that the first build for a new base image might take upwards of
        half an hour. Subsequent builds will have cached compilation stages.

        Args:
            git_commit (Optional[str]): If specified, try to checkout the exact
                git commit from the Ray master branch. If pull_request_id is
                also specified, the commit may be from the PR branch as well.
            github_pr_id (Optional[int]): Specify the pull request id to use.
                If no git commit is specified, the latest commit from the pr
                will be used.
            force_rebuild (bool): Force rebuild of the app config.

        Examples:
            >>> anyscale
            ...   .build_from_source(git_commit="f1e293c", github_pr_id=12345)
            ...   .connect()
        """
        if self._cluster_env_name:
            raise ValueError("cluster_env() conflicts with build_from_source()")
        self._build_commit = git_commit
        self._build_pr = github_pr_id
        self._force_rebuild = force_rebuild
        return self

    def request_resources(
        self,
        *,
        num_cpus: Optional[int] = None,
        num_gpus: Optional[int] = None,
        bundles: Optional[List[Dict[str, float]]] = None,
    ) -> "ClientBuilder":
        """Configure the initial resources to scale to.

        This is an experimental feature.

        The session will immediately attempt to scale to accomodate the
        requested resources, bypassing normal upscaling speed constraints.
        The requested resources are pinned and exempt from downscaling.

        Args:
            num_cpus (int): number of cpus to request.
            num_gpus (int): number of gpus to request.
            bundles (List[Dict[str, float]): resource bundles to
                request. Each bundle is a dict of resource_name to quantity
                that can be allocated on a single machine. Note that the
                ``num_cpus`` and ``num_gpus`` args simply desugar into
                ``[{"CPU": 1}] * num_cpus`` and ``[{"GPU": 1}] * num_gpus``
                respectively.

        Examples:
            >>> ray.client("anyscale://cluster_name").request_resources(num_cpus=200, num_gpus=30).connect()
            >>> ray.client("anyscale://cluster_name").request_resources(
            ...     num_cpus=8,
            ...     resource_bundles=[{"GPU": 8}, {"GPU": 8}, {"GPU": 1}],
            ... ).connect()
        """
        to_request: List[Dict[str, float]] = []
        if num_cpus:
            to_request += [{"CPU": 1}] * num_cpus
        if num_gpus:
            to_request += [{"GPU": 1}] * num_gpus
        if bundles:
            to_request += bundles
        self._initial_scale = to_request
        return self

    def _get_or_create_scratch_project(self) -> str:
        """Get or create a scratch project, including the directory."""
        project_dir = os.path.expanduser(self._scratch_dir)
        project_name = os.path.basename(self._scratch_dir)
        if not os.path.exists(project_dir) and self._find_project_id(project_name):
            self._clone_project(project_dir, project_name)
        else:
            self._ensure_project_setup_at_dir(project_dir, project_name)
        return project_dir

    def _find_project_id(self, project_name: str) -> Optional[str]:
        """Return id if a project of a given name exists."""
        resp = self._anyscale_sdk.search_projects({"name": {"equals": project_name}})
        if len(resp.results) > 0:
            return resp.results[0].id  # type: ignore
        else:
            return None

    def _clone_project(self, project_dir: str, project_name: str) -> None:
        """Clone a project into the given dir by name."""
        cur_dir = os.getcwd()
        try:
            parent_dir = os.path.dirname(project_dir)
            os.makedirs(parent_dir, exist_ok=True)
            os.chdir(parent_dir)
            self._subprocess.check_call(["anyscale", "clone", project_name])
        finally:
            os.chdir(cur_dir)

    def _ensure_project_setup_at_dir(
        self, project_dir: str, project_name: Optional[str]
    ) -> None:
        """Get or create an Anyscale project rooted at the given dir."""
        os.makedirs(project_dir, exist_ok=True)
        if project_name is None:
            project_name = os.path.basename(project_dir)

        # If the project yaml exists, assume we're already setup.
        project_yaml = os.path.join(project_dir, ".anyscale.yaml")
        if os.path.exists(project_yaml):
            return

        project_id = self._find_project_id(project_name)
        if project_id is None:
            self._log.info("Creating new project for", project_dir)
            project_response = self._anyscale_sdk.create_project(
                {
                    "name": project_name,
                    "description": "Automatically created by Anyscale Connect",
                }
            )
            project_id = project_response.result.id

        if not os.path.exists(project_yaml):
            with open(project_yaml, "w+") as f:
                f.write(yaml.dump({"project_id": project_id}))

    def _start_session(
        self,
        project_id: str,
        session_name: str,
        cloud_name: str,
        build_id: Optional[str],
        yaml_filepath: str,
    ) -> None:
        """Start session from sdk. Create/update the session if required."""
        with open(yaml_filepath) as f:
            cluster_config = json.dumps(yaml.safe_load(f.read()))
        cloud_id, _ = get_cloud_id_and_name(self._api_client, cloud_name=cloud_name)

        if self._use_compute_config:
            # Start session with build id and default compute config.
            if not build_id:
                # TODO(nikita): We will support default build ids after the default app
                # configs are created for all python versions.
                raise RuntimeError(
                    "App config must be provided if ANYSCALE_COMPUTE_CONFIG=1. Please specify "
                    'it with `ray.client("anyscale://cluster_name?cluster_env=name:1").connect()`'
                )

            if self._cluster_compute_name:
                compute_template_id = self._get_cluster_compute_id_from_name(
                    project_id, self._cluster_compute_name
                )
            else:
                # If the user specifies _cluster_compute_dict use it, otherwise
                # use the default cluster compute template.
                if self._cluster_compute_dict:
                    cluster_compute_class = ComputeTemplateConfig(
                        **self._cluster_compute_dict
                    )
                    config_object = cluster_compute_class
                else:
                    config_object = self._anyscale_sdk.get_default_compute_config(
                        cloud_id
                    ).result
                compute_template_id = self._register_compute_template(
                    project_id, config_object
                )
            session = self._create_or_update_session_data(
                session_name,
                project_id,
                build_id,
                self._autosuspend_timeout,
                None,
                compute_template_id,
                None,
            )

            self._anyscale_sdk.start_session(
                session.id,
                StartSessionOptions(
                    build_id=build_id, compute_template_id=compute_template_id
                ),
            )
        else:
            # Legacy path of starting session with cluster config and cloud id.
            # Build id can be optionally specified to update the database and UI.
            session = self._create_or_update_session_data(
                session_name,
                project_id,
                build_id,
                self._autosuspend_timeout,
                cluster_config,
                None,
                cloud_id,
            )

            self._anyscale_sdk.start_session(
                session.id, StartSessionOptions(cluster_config=cluster_config),
            )

        wait_for_session_start(project_id, session_name, self._api_client)
        url = get_endpoint(f"/projects/{project_id}/sessions/{session.id}")
        self._log.debug(f"Session {session_name} finished starting. View at {url}")

    def _create_or_update_session_data(
        self,
        session_name: str,
        project_id: str,
        build_id: Optional[str],
        idle_timeout: Optional[int],
        cluster_config: Optional[str],
        compute_template_id: Optional[str],
        cloud_id: Optional[str],
    ) -> Session:
        """
        Creates new session with app configs if session with `session_name` doesn't
        already exist. Otherwise, update the `idle_timeout` of the existing
        session if provided.
        """
        legacy_path = cluster_config and cloud_id
        new_path = build_id and compute_template_id
        assert (
            legacy_path or new_path
        ), "Must provide either build_id and compute_config, or cloud_id and cluster_config."

        session_list = self._api_client.list_sessions_api_v2_sessions_get(
            project_id=project_id, active_only=False, name=session_name
        ).results

        session_exists = len(session_list) > 0
        if not session_exists:
            if legacy_path:
                # Create a new session if there is no existing session with the givens session_name
                create_session_data = CreateSession(
                    name=session_name,
                    project_id=project_id,
                    cloud_id=cloud_id,
                    cluster_config=cluster_config,
                    build_id=build_id,
                    compute_template_id=None,
                    idle_timeout=idle_timeout,
                    uses_app_config=bool(build_id),
                )
                # Using the internal API for this because we need to provide a cluster_config and build_id.
                # Once we move away from cluster configs, we should use the external API to create a session.
                session = self._api_client.create_connect_session_api_v2_sessions_create_connect_session_post(
                    create_session_data
                ).result
            else:
                # Create a new session if there is no existing session with the givens session_name
                create_session_data = CreateSession(
                    name=session_name,
                    project_id=project_id,
                    build_id=build_id,
                    compute_template_id=compute_template_id,
                    idle_timeout=idle_timeout,
                    uses_app_config=True,
                )
                session = self._anyscale_sdk.create_session(create_session_data).result
        else:
            # Get the existing session and update the idle_timeout if required
            session = session_list[0]
            if idle_timeout:
                self._anyscale_sdk.update_session(
                    session.id, UpdateSession(idle_timeout=idle_timeout)
                )

        return session

    def _up_session(
        self,
        project_id: str,
        session_name: str,
        cloud_name: str,
        cwd: Optional[str],
        dangerously_set_build_id: Optional[str],
        yaml_filepath: str,
    ) -> None:
        # Non-blocking version of check_call, see
        # https://github.com/python/cpython/blob/64abf373444944a240274a9b6d66d1cb01ecfcdd/Lib/subprocess.py#L363
        command = (
            ["anyscale", "up"]
            + (["--disable-sync"] if self._enable_runtime_env else [])
            + [
                "--idle-timeout",
                str(self._autosuspend_timeout),
                "--config",
                yaml_filepath,
                "--cloud-name",
                cloud_name,
                session_name,
            ]
            + (
                ["--dangerously-set-build-id", dangerously_set_build_id]
                if dangerously_set_build_id
                else []
            )
        )
        with tempfile.NamedTemporaryFile(delete=False) as output_log_file:
            with self._subprocess.Popen(
                command, cwd=cwd, stdout=output_log_file, stderr=subprocess.STDOUT,
            ) as p:
                # Get session URL:
                session_found = False
                retry_time = 1.0
                while not session_found and retry_time < 10:
                    results = self._list_sessions(project_id=project_id)
                    for session in results:
                        if session.name == session_name:
                            self._log.info(
                                "Updating session, see: {}".format(
                                    get_endpoint(
                                        f"/projects/{project_id}/sessions/{session.id}"
                                    )
                                )
                            )
                            session_found = True
                    time.sleep(retry_time)
                    retry_time = 2 * retry_time
                try:
                    retcode = p.wait()
                except Exception as e:
                    p.kill()
                    raise e
                # Check for errors:
                if retcode:
                    cmd = " ".join(command)
                    msg = "Executing '{}' in {} failed.".format(cmd, self._project_dir)
                    self._log.error(
                        "--------------- Start update logs ---------------\n"
                        "{}".format(open(output_log_file.name).read())
                    )
                    self._log.error("--------------- End update logs ---------------")
                    raise RuntimeError(msg)

    def _get_organization_default_cloud(self) -> Optional[str]:
        """Return default cloud name for organization if it exists and
        if user has correct permissions for it.

        Returns:
            Name of default cloud name for organization if it exists and
            if user has correct permissions for it.
        """
        user = self._api_client.get_user_info_api_v2_userinfo_get().result
        organization = user.organizations[0]  # Each user only has one org
        if organization.default_cloud_id:
            try:
                # Check permissions
                get_cloud_id_and_name(
                    self._api_client, cloud_id=organization.default_cloud_id
                )
                cloud_name = self._api_client.get_cloud_api_v2_clouds_cloud_id_get(
                    organization.default_cloud_id
                ).result.name
                return str(cloud_name)
            except Exception:
                return None
        return None

    def _get_last_used_cloud(self, project_id: str) -> str:
        """Return the name of the cloud last used in the project.

        Args:
            project_id (str): The project to get the last used cloud for.

        Returns:
            Name of the cloud last used in this project.
        """
        # TODO(pcm): Get rid of this and the below API call in the common case where
        # we can determine the cloud to use in the backend.
        cloud_id = self._anyscale_sdk.get_project(project_id).result.last_used_cloud_id

        # TODO(pcm): Replace this with an API call once the AnyscaleSDK supports it.
        p = self._subprocess.Popen(
            ["anyscale", "list", "clouds", "--json"], stdout=subprocess.PIPE
        )
        clouds = json.loads(p.communicate()[0])

        if len(clouds) == 0:
            msg = "No cloud configured, please set up a cloud with 'anyscale cloud setup'."
            self._log.error(msg)
            raise RuntimeError(msg)

        if not cloud_id:
            # Clouds are sorted in descending order, pick the oldest one as default.
            cloud_id = clouds[-1]["id"]

        cloud_name = {cloud["id"]: cloud["name"] for cloud in clouds}[cloud_id]
        self._log.debug(
            (
                f"Using last active cloud '{cloud_name}'. "
                "Call anyscale.cloud('...').connect() to overwrite."
            )
        )
        return cast(str, cloud_name)

    def _get_or_create_updated_session(  # noqa: C901
        self,
        config_hash: bytes,
        project_id: str,
        session_name: Optional[str],
        build_id: Optional[str],
        yaml_filepath: str,
    ) -> str:
        """Get or create a session updated with the given hash.

        Args:
            config_hash (bytes): The hash value of config
            project_id (str): The project to use.
            session_name (Optional[str]): If specified, the given session
                will be created or updated as needed. Otherwise the session
                name will be picked automatically.

        Returns:
            The name of the session to connect to.
        """
        session_hash = None
        ray_cli = self._ray.util.client.ray
        kv = self._ray.experimental.internal_kv
        results = self._list_sessions(project_id=project_id)

        if session_name is not None:
            for session in results:
                if session.state != "Running":
                    continue
                if session.name == session_name:
                    self._log.debug("Trying to acquire lock on", session.name)
                    self._acquire_session_lock(
                        session, raise_connection_error=False, connection_retries=0
                    )
                    if ray_cli.is_connected():
                        try:
                            session_hash = kv._internal_kv_get(ANYSCALE_CONFIG_HASH)
                        except Exception as e:
                            self._log.debug("Error getting session hash", e)
                    break

        else:
            self._log.debug("-> Starting a new session")
            used_names = [s.name for s in results]
            for i in range(MAX_SESSIONS):
                name = "session-{}".format(i)
                if name not in used_names:
                    session_name = name
                    self._log.debug("Starting session", session_name)
                    break

        # Should not happen.
        if session_name is None:
            raise RuntimeError("Could not create new session to connect to.")

        if self._cloud_name is None:
            default_cloud_name = self._get_organization_default_cloud()
            if default_cloud_name:
                self._cloud_name = default_cloud_name
            else:
                self._cloud_name = self._get_last_used_cloud(project_id)

        self._log.debug("Session hash", session_hash)
        self._log.debug("config hash", config_hash)
        if (
            session_hash != config_hash
            and "ANYSCALE_SKIP_CHECKING_HASH" not in os.environ
        ):
            self._log.debug("Updating the cluster config of", session_name)
            # TODO(ekl): race condition here since "up" breaks the lock.
            if ray_cli.is_connected():
                self._ray.util.disconnect()
            # Update session.
            if self._enable_runtime_env:
                self._log.debug("Starting session with sdk")
                self._start_session(
                    project_id=project_id,
                    session_name=session_name,
                    cloud_name=self._cloud_name,
                    build_id=build_id,
                    yaml_filepath=yaml_filepath,
                )
            else:
                self._log.debug("Starting session with `anyscale up`")
                self._up_session(
                    project_id,
                    session_name,
                    self._cloud_name,
                    self._project_dir,
                    dangerously_set_build_id=build_id,
                    yaml_filepath=yaml_filepath,
                )
            # Need to re-acquire the connection after the update.
            self._acquire_session_lock(
                self._get_session_or_die(project_id, session_name),
                raise_connection_error=True,
                connection_retries=10,
            )
            # TODO(ekl) retry this, might be race condition with another client
            if not ray_cli.is_connected():
                raise RuntimeError("Failed to acquire session we created")
            self._log.debug(
                "Updated files hash",
                config_hash,
                kv._internal_kv_get(ANYSCALE_CONFIG_HASH),
            )

        kv._internal_kv_put(ANYSCALE_CONFIG_HASH, config_hash, overwrite=True)
        return session_name

    def _acquire_session_lock(
        self,
        session_meta: Session,
        raise_connection_error: bool,
        connection_retries: int,
    ) -> None:
        """Connect to and acquire a lock on the session.

        The session lock is released by calling disconnect() on the returned
        Ray connection. This function also checks for Python version
        compatibility, it will not acquire the lock on version mismatch.

        """
        try:
            session_url, secure, metadata = self._get_connect_params(session_meta)
            if connection_retries > 0:
                self._log.debug("Beginning connection attempts")
            # Disable retries when acquiring session lock for fast failure.
            self._log.debug(
                "Info: ",
                session_url,
                secure,
                metadata,
                connection_retries,
                self._job_config,
            )
            info = self._ray.util.connect(
                session_url,
                secure=secure,
                metadata=metadata,
                connection_retries=connection_retries,
                job_config=self._job_config,
                ignore_version=True,
            )
            self._dynamic_check(info)
            self._log.debug("Connected server info: ", info)
        except Exception as e:
            if raise_connection_error:
                self._log.debug(
                    "Connection error after {} retries".format(connection_retries)
                )
                raise
            else:
                self._log.debug("Ignoring connection error", e)
                return
        if info["num_clients"] > 1:
            self._log.debug(
                "Failed to acquire lock due to too many connections: ",
                info["num_clients"],
            )
            self._ray.util.disconnect()

    def _check_connection(self, project_id: str, session_name: str,) -> None:
        """Check the connected session to make sure it's good"""
        session_found = self._get_session_or_die(project_id, session_name)

        def func() -> str:
            return "Connected!"

        f_remote = self._ray.remote(func)
        ray_ref = f_remote.remote()
        self._log.debug(self._ray.get(ray_ref))
        self._log.info(
            "Connected to {}, see: {}".format(
                session_name,
                get_endpoint(f"/projects/{project_id}/sessions/{session_found.id}"),
            )
        )

    def _get_session_or_die(self, project_id: str, session_name: str) -> Session:
        """Query Anyscale for the given session's metadata."""
        session_found = self._get_session(project_id, session_name)
        if not session_found:
            raise RuntimeError("Failed to locate session: {}".format(session_name))
        return session_found

    def _get_session(self, project_id: str, session_name: str) -> Optional[Session]:
        """Query Anyscale for the given session's metadata."""
        results = self._list_sessions(project_id=project_id)
        session_found: Session = None
        for session in results:
            if session.name == session_name:
                session_found = session
                break
        return session_found

    def _get_connect_params(self, session_meta: Session) -> Tuple[str, bool, Any]:
        """Get the params from the session needed to use Ray client."""
        connect_url = None
        metadata = [("cookie", "anyscale-token=" + session_meta.access_token)]
        if session_meta.connect_url:
            url_components = session_meta.connect_url.split("?port=")
            metadata += [("port", url_components[1])] if len(url_components) > 1 else []
            connect_url = url_components[0]
            secure = len(url_components) == 1
        else:
            # This code path can go away once all sessions use session_meta.connect_url:
            # TODO(nikita): Use the service_proxy_url once it is fixed for anyscale up with file mounts.
            full_url = session_meta.jupyter_notebook_url
            assert (
                full_url is not None
            ), f"Unable to determine URL for Session: {session_meta.name}, please retry shortly or try a different session."
            # like "session-fqsx0p3pzfna71xxxxxxx.anyscaleuserdata.com:8081"
            connect_url = full_url.split("/")[2].lower() + ":8081"
            # like "8218b528-7363-4d04-8358-57936cdxxxxx"
            metadata += [("port", "10001")]
            secure = False

        return connect_url, secure, metadata

    def _fingerprint(self, dir_path: str, yaml_filepath: str) -> str:
        """Calculate file hash for the given dir."""
        fingerprint_hasher = hashlib.blake2b()
        dir_fingerprint = fingerprint(
            dir_path,
            exclude_dirs=EXCLUDE_DIRS,  # .git does not work with absolute path.
            exclude_paths=[os.path.join(dir_path, path) for path in EXCLUDE_PATHS],
            mtime_hash=True,
        )
        fingerprint_hasher.update(dir_fingerprint.encode("utf-8"))
        if os.path.exists(yaml_filepath):
            with open(yaml_filepath) as f:
                fingerprint_hasher.update(f.read().encode("utf-8"))
        return fingerprint_hasher.hexdigest()

    def _get_cluster_compute_id_from_name(
        self, project_id: str, cluster_compute_name: str
    ) -> str:
        """gets the cluster compute id given a cluster name."""
        cluster_compute_id: Optional[str] = None
        cluster_computes = self._api_client.search_compute_templates_api_v2_compute_templates_search_post(
            ComputeTemplateQuery(project_id=project_id)
        ).results
        for template in cluster_computes:
            if template.name == cluster_compute_name:
                cluster_compute_id = template.id
        if cluster_compute_id is None:
            raise ValueError(
                f"The cluster compute template {cluster_compute_name}"
                " is not registered."
            )
        else:
            return cluster_compute_id

    def _register_compute_template(
        self, project_id: str, config_object: ComputeTemplateConfig
    ) -> str:
        """
        Register compute template with a default name and return the compute template id."""
        created_template = self._api_client.create_compute_template_api_v2_compute_templates_post(
            create_compute_template=CreateComputeTemplate(
                name="connect-autogenerated-config-{}".format(
                    datetime.now().isoformat()
                ),
                project_id=project_id,
                config=config_object,
                anonymous=True,
            )
        ).result
        compute_template_id = str(created_template.id)
        return compute_template_id

    def _populate_cluster_config(
        self,
        cluster_yaml: Dict[str, Any],
        project_id: str,
        project_name: str,
        build: Optional[Build],
        needs_up: bool = True,
    ) -> Dict[str, Any]:
        """Populate cluster config with serverless compute options."""
        cluster_yaml = copy.deepcopy(cluster_yaml)

        base_docker_image_cpu = _get_base_image("cpu")
        base_docker_image_gpu = _get_base_image("gpu")

        # Overwrite base_docker_image with application config if available.
        if build:
            base_docker_image_cpu = (
                base_docker_image_gpu
            ) = self._get_app_config_docker_image(project_id, build_to_use=build)
        elif self._base_docker_image:
            # Overwrite base_docker_image if provided by user.
            base_docker_image_cpu = self._base_docker_image
            base_docker_image_gpu = self._base_docker_image
        else:
            # We are using our pinned-nightly images, so we can version check against
            # the pinned Ray version & commit.
            if needs_up:
                self._check_required_ray_version(
                    self._ray.__version__, self._ray.__commit__
                )
        self._log.debug("Base docker image {}".format(base_docker_image_cpu))

        # Setup serverless compute template.
        cluster_yaml["available_node_types"] = {
            "anyscale.cpu.medium": {
                "node_config": {"InstanceType": "m5.4xlarge"},
                "max_workers": 20,
                "resources": {},
                "docker": {"worker_image": base_docker_image_cpu},
            },
            "anyscale.cpu.large": {
                "node_config": {"InstanceType": "m5.16xlarge"},
                "max_workers": 10,
                "resources": {},
                "docker": {"worker_image": base_docker_image_cpu},
            },
            "anyscale.gpu.medium": {
                "node_config": {"InstanceType": "g3.4xlarge"},
                "max_workers": 20,
                "resources": {},
                "docker": {"worker_image": base_docker_image_gpu},
            },
            "anyscale.gpu.large": {
                "node_config": {"InstanceType": "g3.16xlarge"},
                "max_workers": 10,
                "resources": {},
                "docker": {"worker_image": base_docker_image_gpu},
            },
        }
        cluster_yaml["max_workers"] = 50
        cluster_yaml["head_node_type"] = "anyscale.cpu.medium"
        cluster_yaml["docker"]["image"] = base_docker_image_cpu

        # Install Ray runtime if specified.
        if self._ray_release:
            cluster_yaml["setup_commands"] = [
                "pip install -U {}".format(get_wheel_url(self._ray_release))
            ]

        # Install requirements:
        if self._requirements:
            cluster_yaml["setup_commands"].append(
                f'echo "{self._requirements}" | pip install -r /dev/stdin'
            )

        cluster_yaml["head_start_ray_commands"] = [
            "ray stop",
            "ulimit -n 65536; ray start --head --port=6379 "
            "--object-manager-port=8076  --ray-client-server-port=10001",
        ]

        return cluster_yaml

    def _wait_for_app_build(self, project_id: str, build_id: str) -> Build:
        has_logged = False
        while True:
            build = self._anyscale_sdk.get_build(build_id).result
            if build.status in ["pending", "in_progress"]:
                if not has_logged:
                    url = get_endpoint(
                        f"projects/{project_id}/app-config-details/{build_id}"
                    )
                    self._log.info(
                        f"Waiting for app config to be built (see {url} for progress)..."
                    )
                    has_logged = True
                time.sleep(10.0)
            elif build.status in ["failed", "pending_cancellation", "canceled"]:
                raise RuntimeError(
                    "Build status is '{}', please select another revision!".format(
                        build.status
                    )
                )
            else:
                assert build.status == "succeeded"
                return build

    def _get_app_config_build(
        self, project_id: str, app_config_name: str, app_config_revision: Optional[int]
    ) -> Build:
        app_template_id = None
        app_templates = self._list_app_configs(project_id)
        for app_template in app_templates:
            if app_template.name == app_config_name:
                app_template_id = app_template.id
        if not app_template_id:
            raise RuntimeError(
                "Application config '{}' not found. ".format(app_config_name)
                + "Available app configs: {}".format(
                    ", ".join(a.name for a in app_templates)
                )
            )
        builds = self._list_builds(app_template_id)

        build_to_use = None
        if app_config_revision:
            for build in builds:
                if build.revision == app_config_revision:
                    build_to_use = build

            if not build_to_use:
                raise RuntimeError(
                    "Revision {} of app config '{}' not found.".format(
                        app_config_revision, app_config_name
                    )
                )
        else:
            latest_build_revision = -1
            for build in builds:
                if build.revision > latest_build_revision:
                    latest_build_revision = build.revision
                    build_to_use = build
            self._log.debug(
                "Using latest revision {} of {}".format(
                    latest_build_revision, app_config_name
                )
            )
        assert build_to_use  # for mypy
        return build_to_use

    def _build_app_config_from_source(self, project_id: str) -> str:
        config_name = "ray-build-{}-{}".format(self._build_pr, self._build_commit)
        # Force creation of a unique app config.
        if self._force_rebuild:
            config_name += "-{}".format(int(time.time()))
        app_templates = self._list_app_configs(project_id)
        found = any([a.name == config_name for a in app_templates])
        if not found:
            build_steps = BUILD_STEPS.copy()
            # Add a unique command to bust the Makisu cache if needed.
            # Otherwise we could end up caching a previous fetch.
            build_steps.append("echo UNIQUE_ID={}".format(config_name))
            if self._build_pr:
                build_steps.append(
                    "cd ray && git fetch origin pull/{}/head:target && "
                    "git checkout target".format(self._build_pr)
                )
            if self._build_commit:
                build_steps.append(
                    "cd ray && git checkout {}".format(self._build_commit)
                )
            build_steps.append(
                'cd ray/python && sudo env "PATH=$PATH" python setup.py develop'
            )
            self._anyscale_sdk.create_app_config(
                {
                    "name": config_name,
                    "project_id": project_id,
                    "config_json": {
                        "base_image": self._base_docker_image or "anyscale/ray:nightly",
                        "debian_packages": ["curl", "unzip", "zip", "gnupg"],
                        "post_build_cmds": build_steps,
                    },
                }
            )
        return config_name

    def _get_app_config_docker_image(self, project_id: str, build_to_use: Build) -> str:
        # Wait for build to complete:
        build_to_use = self._wait_for_app_build(project_id, build_to_use.id)
        return "localhost:5555/{}".format(build_to_use.docker_image_name)

    def _exec_self_in_head_node(self) -> None:
        """Run the current main file in the head node."""
        cur_file = os.path.abspath(sys.argv[0])
        # TODO(ekl) it would be nice to support keeping the original file name,
        # but "anyscale push" isn't escaping e.g., spaces correctly.
        tmp_file = "/tmp/anyscale-connect-{}.py".format(uuid.uuid4().hex)
        cur_dir = os.getcwd()
        try:
            assert self._project_dir is not None
            os.chdir(self._project_dir)
            command = [
                "anyscale",
                "push",
                self._session_name,
                "-s",
                cur_file,
                "-t",
                tmp_file,
            ]
            self._log.debug("Running", command)
            self._subprocess.check_output(
                command, stderr=subprocess.STDOUT,
            )
            command = (
                [
                    "anyscale",
                    "exec",
                    "--session-name",
                    self._session_name,
                    "python",
                    tmp_file,
                ]
                + sys.argv[1:]  # type: ignore
            )
            self._log.debug("Running", command)
            self._subprocess.check_call(command)
        finally:
            os.chdir(cur_dir)
        self._os._exit(0)

    def _exec_self_in_local_docker(self) -> None:
        """Run the current main file in a local docker image."""
        cur_file = os.path.abspath(sys.argv[0])
        docker_image = self._base_docker_image or _get_base_image("cpu")
        command = [
            "docker",
            "run",
            "--env",
            "ANYSCALE_HOST={}".format(anyscale.conf.ANYSCALE_HOST),
            "--env",
            "ANYSCALE_CLI_TOKEN={}".format(self._credentials),
            "-v",
            "{}:/user_main.py".format(cur_file),
            "--entrypoint=/bin/bash",
            docker_image,
            "-c",
            "python /user_main.py {}".format(
                " ".join([shlex.quote(x) for x in sys.argv[1:]])
            ),
        ]
        self._log.debug("Running", command)
        self._subprocess.check_call(command)
        self._os._exit(0)

    def _get_project_name(self, project_id: str) -> str:
        return str(self._anyscale_sdk.get_project(project_id).result.name)

    def _list_entities(
        self, list_function: Callable[..., Any], container_id: str
    ) -> List[Any]:
        entities = []
        has_more = True
        paging_token = None
        while has_more:
            resp = list_function(container_id, count=50, paging_token=paging_token)
            entities.extend(resp.results)
            paging_token = resp.metadata.next_paging_token
            has_more = paging_token is not None
        return entities

    def _list_sessions(self, project_id: str) -> List[Session]:
        return self._list_entities(self._anyscale_sdk.list_sessions, project_id)

    def _list_app_configs(self, project_id: str) -> List[AppConfig]:
        return self._list_entities(self._anyscale_sdk.list_app_configs, project_id)

    def _list_builds(self, application_template_id: str) -> List[Build]:
        return self._list_entities(
            self._anyscale_sdk.list_builds, application_template_id
        )

    def _check_required_ray_version(
        self,
        ray_version: str,
        ray_commit: str,
        required_ray_version: str = REQUIRED_RAY_VERSION,
        required_ray_commit: str = REQUIRED_RAY_COMMIT,
    ) -> None:
        if ray_version != required_ray_version or ray_commit != required_ray_commit:
            if ray_version != required_ray_version:
                msg = "The local ray installation has version {}, but {} is required.".format(
                    ray_version, required_ray_version
                )
            else:
                msg = "The local ray installation has commit {}, but {} is required.".format(
                    ray_commit[:7], required_ray_commit[:7]
                )
            msg = (
                "{}\nPlease install the required "
                "Ray version by running:\n\t`pip uninstall ray -y && pip install -U {}`\nTo unsafely "
                "ignore this check, set IGNORE_VERSION_CHECK=1.".format(
                    msg, get_wheel_url("master/{}".format(required_ray_commit)),
                )
            )

            if self._ignore_version_check:
                self._log.debug(msg)
            else:
                raise ValueError(msg)

    def _dynamic_check(self, info: Dict[str, str]) -> None:
        self._check_required_ray_version(
            self._ray.__version__,
            self._ray.__commit__,
            info["ray_version"],
            info["ray_commit"],
        )

        # NOTE: This check should not be gated with IGNORE_VERSION_CHECK, because this is
        # replacing Ray Client's internal check.
        local_major_minor = f"{sys.version_info[0]}.{sys.version_info[1]}"
        client_version = f"{local_major_minor}.{sys.version_info[2]}"
        server_version = info["python_version"]
        assert server_version.startswith(
            local_major_minor
        ), f"Python minor versions differ between client ({client_version}) and server ({server_version}). Please ensure that they match."


# This implements the following utility function for users:
# $ pip install -U `python -m anyscale.connect required_ray_version`
if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "required_ray_version":
        print(get_wheel_url("master/{}".format(REQUIRED_RAY_COMMIT)))
    else:
        raise ValueError("Unsupported argument.")
