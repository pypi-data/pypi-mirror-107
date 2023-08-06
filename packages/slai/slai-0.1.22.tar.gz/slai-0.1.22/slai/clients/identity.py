from slai.exceptions import NoCredentialsFound
import requests

from requests.auth import HTTPBasicAuth
from importlib import import_module

from slai.modules.parameters import from_config
from slai.modules.runtime import detect_runtime, detect_credentials

REQUESTS_TIMEOUT = 15


def get_identity_client(*, client_id=None, client_secret=None):
    import_path = from_config(
        "IDENTITY_CLIENT",
        "slai.clients.identity.IdentityClient",
    )
    class_ = import_path.split(".")[-1]
    path = ".".join(import_path.split(".")[:-1])
    return getattr(import_module(path), class_)(
        client_id=client_id, client_secret=client_secret
    )


class IdentityClient:
    STAGE = from_config(
        key="STAGE",
        default="staging",
    )

    BASE_URL = from_config(
        key="BASE_URL",
        default=f"https://api.slai.io/{STAGE}",
    )

    def __init__(self, client_id=None, client_secret=None):
        self.runtime = detect_runtime()
        self.credentials_loaded = False

        if not client_id or not client_secret:
            try:
                self.credentials = detect_credentials(runtime=self.runtime)
                self.client_id = self.credentials["client_id"]
                self.client_secret = self.credentials["client_secret"]
                self.credentials_loaded = True
            except NoCredentialsFound:
                pass

        else:
            self.client_id = client_id
            self.client_secret = client_secret

            self.credentials_loaded = True

    def validate_notebook_auth_token(self, *, token):
        body = {"action": "retrieve", "token": token}

        res = requests.post(
            f"{self.BASE_URL}/app/notebook-auth",
            auth=None,
            headers={},
            json=body,
            timeout=REQUESTS_TIMEOUT,
        )
        res.raise_for_status()
        return res.json()

    def get_user(self):
        if not self.credentials_loaded:
            raise NoCredentialsFound("no_credentials_loaded")

        body = {"action": "retrieve"}

        res = requests.post(
            f"{self.BASE_URL}/cli/user",
            auth=HTTPBasicAuth(self.client_id, self.client_secret),
            headers={},
            json=body,
            timeout=REQUESTS_TIMEOUT,
        )
        res.raise_for_status()
        return res.json()
