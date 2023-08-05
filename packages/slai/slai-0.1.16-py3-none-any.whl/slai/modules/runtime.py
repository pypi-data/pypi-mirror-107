import os
import yaml
import sys

from pathlib import Path
from slai.exceptions import NoCredentialsFound

LOCAL_CREDENTIALS_PATHS = {
    "project": ".slai/credentials.yml",
    "global": f"{Path.home()}/.slai/credentials.yml",
}


class ValidRuntimes:
    Local = "local"
    Project = "project"
    Collab = "collab"


def detect_runtime():
    try:
        import google.colab  # noqa

        return ValidRuntimes.Collab
    except ImportError:
        cwd = os.getcwd()
        project_config_path = f"{cwd}/.slai/config.yml"

        if os.path.exists(project_config_path):
            return ValidRuntimes.Project
        else:
            return ValidRuntimes.Local


def detect_credentials(*, runtime, profile_name="default"):
    credentials = None

    if runtime == ValidRuntimes.Local:
        credentials = getattr(sys.modules["slai"], "credentials", None)

        if credentials:
            return credentials

        if os.path.exists(LOCAL_CREDENTIALS_PATHS["global"]):
            credentials = _load_credentials(
                path=LOCAL_CREDENTIALS_PATHS["global"], credentials_type="global"
            )
            credentials = credentials.get(profile_name)
        else:
            raise NoCredentialsFound("no_credentials_found")

    elif runtime == ValidRuntimes.Project:
        if os.path.exists(LOCAL_CREDENTIALS_PATHS["project"]):
            credentials = _load_credentials(
                path=LOCAL_CREDENTIALS_PATHS["project"], credentials_type="project"
            )
        else:
            raise NoCredentialsFound("no_credentials_found")

    elif runtime == ValidRuntimes.Collab:
        credentials = getattr(sys.modules["slai"], "credentials", None)

        if not credentials:
            raise NoCredentialsFound("no_credentials_found")

    return credentials


def _load_credentials(*, path, credentials_type="global"):
    credentials = {}

    with open(path, "r") as f_in:
        try:
            credentials = yaml.safe_load(f_in)
        except yaml.YAMLError:
            raise NoCredentialsFound("slai_invalid_config")

    if credentials_type == "global":
        return credentials
    elif credentials_type == "project":
        return {
            "client_id": credentials["client_id"],
            "client_secret": credentials["client_secret"],
        }

    return credentials
