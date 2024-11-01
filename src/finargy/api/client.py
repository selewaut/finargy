from email.mime import base
import token
import requests
import datetime
from dotenv import load_dotenv
import os


BASE_URL = "https://api.invertironline.com/api/v2"
TOKEN_URL = "https://api.invertironline.com/token"


class InvertirOnlineAPI:
    def __init__(self, base_url=BASE_URL, token_url=TOKEN_URL):
        # load environment variables
        load_dotenv()
        self.username = os.getenv("USER")
        self.password = os.getenv("PASSWORD")
        self.base_url = base_url
        self.token_url = token_url
        self.access_token = None
        self.token_expiry = None
        # get auth tokens.
        self._authenticate()

    def _authenticate(self):
        """Authenticate and obtain access token."""
        data = {
            "grant_type": "password",
            "username": self.username,
            "password": self.password,
        }
        response = requests.post(self.token_url, data=data)
        response.raise_for_status()
        # get authentication token
        token_info = response.json()
        self.access_token = token_info["access_token"]
        expires_in = token_info["expires_in"]
        self.token_expiry = datetime.datetime.now() + datetime.timedelta(
            seconds=expires_in
        )
        print(f"Authenticated. Token expires at {self.token_expiry}")

    def _check_token_expiry(self):
        """Check if the token has expired and re-authenticate if necessary."""
        if datetime.datetime.now() >= self.token_expiry:
            self._authenticate()

    def _request(self, method, endpoint, params=None, data=None):
        """Make an API request."""
        self._check_token_expiry()
        url = f"{self.base_url}/{endpoint}"
        headers = {
            "Authorization": f"Bearer {self.access_token}",
        }
        response = requests.request(
            method, url, headers=headers, params=params, json=data
        )
        response.raise_for_status()
        return response.json()
