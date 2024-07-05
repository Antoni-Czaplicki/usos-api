import urllib

import aiohttp
from oauthlib.oauth1 import Client

from .exceptions import USOSAPIException
from .logger import get_logger

_LOGGER = get_logger("AuthManager")


class AuthManager:
    REQUEST_TOKEN_SUFFIX = "services/oauth/request_token"
    AUTHORIZE_SUFFIX = "services/oauth/authorize"
    ACCESS_TOKEN_SUFFIX = "services/oauth/access_token"
    REVOKE_TOKEN_SUFFIX = "services/oauth/revoke_token"
    SCOPES = "|".join(["offline_access", "studies"])

    def __init__(self, api_base_address: str, consumer_key: str, consumer_secret: str):
        self.base_address = api_base_address.rstrip("/") + "/"
        self.consumer_key = consumer_key
        self.consumer_secret = consumer_secret
        self.access_token = None
        self.access_token_secret = None
        self._session = None
        self._oauth_client = Client(consumer_key, consumer_secret)

    async def __aenter__(self) -> "AuthManager":
        await self.open()
        return self

    async def __aexit__(self, exc_type, exc_value, traceback):
        await self.close()

    async def open(self):
        self._session = aiohttp.ClientSession()

    async def close(self):
        if self._session:
            await self._session.close()

    async def _generate_request_token(self, callback_url: str) -> None:
        url = f"{self.base_address}{self.REQUEST_TOKEN_SUFFIX}"
        params = {
            "oauth_callback": callback_url,
            "scopes": self.SCOPES,
        }
        headers = {"Content-Type": "application/x-www-form-urlencoded"}
        url, headers, body = self._oauth_client.sign(
            url, http_method="POST", body=params, headers=headers
        )
        async with self._session.post(url, data=body, headers=headers) as response:
            await self._handle_response_errors(response)
            data = dict(urllib.parse.parse_qsl(await response.text()))
            self._request_token = data["oauth_token"]
            self._request_token_secret = data["oauth_token_secret"]
            self._oauth_client.resource_owner_key = self._request_token
            self._oauth_client.resource_owner_secret = self._request_token_secret
            _LOGGER.info(f"New request token generated: {self._request_token}")

    async def get_authorization_url(self, callback_url: str) -> str:
        await self._generate_request_token(callback_url)
        return f"{self.base_address}{self.AUTHORIZE_SUFFIX}?oauth_token={self._request_token}"

    async def authorize_with_token(self, token: str):
        self._oauth_client.verifier = token
        url = f"{self.base_address}{self.ACCESS_TOKEN_SUFFIX}"
        url, headers, body = self._oauth_client.sign(url, http_method="POST")
        async with self._session.post(url, data=body, headers=headers) as response:
            await self._handle_response_errors(response)
            data = dict(urllib.parse.parse_qsl(await response.text()))
            self.access_token = data["oauth_token"]
            self.access_token_secret = data["oauth_token_secret"]
            self._oauth_client = Client(
                self.consumer_key,
                client_secret=self.consumer_secret,
                resource_owner_key=self.access_token,
                resource_owner_secret=self.access_token_secret,
            )
            _LOGGER.info(
                f"Authorization successful, received access token: {self.access_token}"
            )
            return self.access_token, self.access_token_secret

    async def load_access_token(self, access_token: str, access_token_secret: str):
        self.access_token = access_token
        self.access_token_secret = access_token_secret
        self._oauth_client = Client(
            self.consumer_key,
            client_secret=self.consumer_secret,
            resource_owner_key=self.access_token,
            resource_owner_secret=self.access_token_secret,
        )

    async def sign_request(self, url: str, http_method: str = "GET", **kwargs):
        if not self.access_token:
            raise USOSAPIException("Access token not set. Did you forget to authorize?")
        url, headers, body = self._oauth_client.sign(
            url, http_method=http_method, **kwargs
        )
        return url, headers, body

    async def _handle_response_errors(self, response: aiohttp.ClientResponse):
        if response.status != 200:
            text = await response.text()
            if response.status == 401:
                _LOGGER.error(
                    f"HTTP 401: Unauthorized. Your access key probably expired. Response: {text}"
                )
                raise USOSAPIException(
                    "HTTP 401: Unauthorized. Your access key probably expired."
                )
            elif response.status == 400:
                raise USOSAPIException(f"HTTP 400: Bad request: {text}")
            else:
                raise USOSAPIException(f"HTTP {response.status}: {text}")

    async def _revoke_token(self):
        url = f"{self.base_address}{self.REVOKE_TOKEN_SUFFIX}"
        url, headers, body = self._oauth_client.sign(url, http_method="POST")
        async with self._session.post(url, data=body, headers=headers) as response:
            await self._handle_response_errors(response)
            _LOGGER.info("Token revoked successfully.")

    async def logout(self):
        if not self.access_token:
            return
        await self._revoke_token()
        self.access_token = None
