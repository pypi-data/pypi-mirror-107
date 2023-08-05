import requests
import sys

from slai.clients.identity import get_identity_client
from slai.modules.parameters import from_config
from slai.exceptions import (
    InvalidNotebookAuthToken,
    InvalidCredentials,
    NoCredentialsFound,
)

from getpass import getpass


class Login:
    APP_BASE_URL = from_config(
        key="APP_BASE_URL",
        default="https://app.slai.io",
    )

    def __init__(self, *, client_id=None, client_secret=None):
        self.identity_client = get_identity_client(
            client_id=client_id, client_secret=client_secret
        )

        if client_id is None or client_secret is None:
            self._notebook_auth_flow()
        else:
            self.client_id = client_id
            self.client_secret = client_secret

        self._validate_credentials()

    def _validate_credentials(self):
        try:
            _ = self.identity_client.get_user()
        except requests.exceptions.HTTPError:
            self.authenticated = False
            raise InvalidCredentials("invalid_credentials")

        # cache credentials on slai module
        setattr(
            sys.modules["slai"],
            "credentials",
            {"client_id": self.client_id, "client_secret": self.client_secret},
        )

        setattr(
            sys.modules["slai"],
            "authenticated",
            True,
        )

        print("logged in successfully.")

    def _notebook_auth_flow(self):
        token = getpass(
            f"navigate to {self.APP_BASE_URL}/notebook-auth for a temporary login token: "
        )

        try:
            response = self.identity_client.validate_notebook_auth_token(token=token)
        except requests.exceptions.HTTPError:
            raise InvalidNotebookAuthToken("invalid_token")

        self.client_id = response["client_id"]
        self.client_secret = response["client_secret"]

        self.identity_client.client_id = self.client_id
        self.identity_client.client_secret = self.client_secret
        self.identity_client.credentials_loaded = True


if __name__ == "__main__":
    login = Login()
    # login = Login(
    #     client_id="c86509848a8efcaf2b50bb791995ce57",
    #     client_secret="aa887a13fbadef87d23612c6c95913c3",
    # )
