import urllib

import aiohttp
from oauthlib.oauth1 import Client

from .exceptions import USOSAPIException
from .logger import get_logger

_LOGGER = get_logger("AuthManager")


class AuthManager:
    """
    A manager for the USOS API authentication.
    """

    REQUEST_TOKEN_SUFFIX = "services/oauth/request_token"
    AUTHORIZE_SUFFIX = "services/oauth/authorize"
    ACCESS_TOKEN_SUFFIX = "services/oauth/access_token"
    REVOKE_TOKEN_SUFFIX = "services/oauth/revoke_token"
    # List of available scopes can be found at https://apps.usos.edu.pl/developers/api/authorization/#scopes
    SCOPES = "|".join(["offline_access", "studies"])

    def __init__(self, api_base_address: str, consumer_key: str, consumer_secret: str):
        """
        Initialize the authentication manager.

        :param api_base_address: The base address of the USOS API.
        :param consumer_key: Consumer key obtained from the USOS API.
        :param consumer_secret: Consumer secret obtained from the USOS API.
        """
        self.base_address = api_base_address.rstrip("/") + "/"
        self.consumer_key = consumer_key
        self.consumer_secret = consumer_secret
        self.access_token = None
        self.access_token_secret = None
        self._session = None
        self._oauth_client = Client(consumer_key, consumer_secret)

    async def __aenter__(self) -> "AuthManager":
        """
        Enter the manager.

        :return: The manager.
        """
        await self.open()
        return self

    async def __aexit__(self, exc_type, exc_value, traceback):
        """
        Exit the manager.

        :param exc_type: The exception type.
        :param exc_value: The exception value.
        :param traceback: The traceback.
        """
        await self.close()

    async def open(self):
        """
        Open the manager.
        """
        self._session = aiohttp.ClientSession()

    async def close(self):
        """
        Close the manager.
        """
        if self._session:
            await self._session.close()

    async def _generate_request_token(self, callback_url: str) -> None:
        """
        Generate a new request token.

        :param callback_url:
        """
        url = f"{self.base_address}{self.REQUEST_TOKEN_SUFFIX}"
        params = {
            "oauth_callback": callback_url,
            "scopes": self.SCOPES,
        }
        headers = {"Content-Type": "application/x-www-form-urlencoded"}
        url, headers, body = Client(
            self.consumer_key, client_secret=self.consumer_secret
        ).sign(
            url, http_method="POST", body=params, headers=headers
        )  # Use a new client to avoid using the access token if it's set
        async with self._session.post(url, data=body, headers=headers) as response:
            await self._handle_response_errors(response)
            data = dict(urllib.parse.parse_qsl(await response.text()))
            self._request_token = data["oauth_token"]
            self._request_token_secret = data["oauth_token_secret"]
            self._oauth_client.resource_owner_key = self._request_token
            self._oauth_client.resource_owner_secret = self._request_token_secret
            _LOGGER.info(f"New request token generated: {self._request_token}")

    async def get_authorization_url(
        self, callback_url: str, confirm_user: bool = False
    ) -> str:
        """
        Get the authorization URL.

        :param callback_url: The callback URL.
        :param confirm_user: Whether to confirm the user.
        :return: The authorization URL.
        """
        await self._generate_request_token(callback_url)
        if confirm_user:
            return f"{self.base_address}{self.AUTHORIZE_SUFFIX}?oauth_token={self._request_token}&interactivity=confirm_user"
        return f"{self.base_address}{self.AUTHORIZE_SUFFIX}?oauth_token={self._request_token}"

    async def authorize(self, verifier: str, request_token, request_token_secret):
        """
        Authorize the client with verifier and optionally token and token secret.

        :param verifier: The verifier to authorize the client with.
        :param token: The OAuth token obtained from the previous step.
        :param token_secret: The OAuth token secret obtained from the previous step.
        :return: The access token and secret.
        """
        self._oauth_client.verifier = verifier
        if request_token:
            self._oauth_client.resource_owner_key = request_token
        if request_token_secret:
            self._oauth_client.resource_owner_secret = request_token_secret
        url = f"{self.base_address}{self.ACCESS_TOKEN_SUFFIX}"
        url, headers, body = self._oauth_client.sign(url, http_method="POST")
        try:
            async with self._session.post(url, data=body, headers=headers) as response:
                await self._handle_response_errors(response)
                data = dict(urllib.parse.parse_qsl(await response.text()))
                self.load_access_token(data["oauth_token"], data["oauth_token_secret"])
                _LOGGER.info(
                    f"Authorization successful, received access token: {self.access_token}"
                )
                return self.access_token, self.access_token_secret
        except AttributeError as e:
            if e.args[0] == "'NoneType' object has no attribute 'post'":
                raise USOSAPIException(
                    "Authorization failed. Did you forget to open the manager?"
                )
            raise

    def load_access_token(self, access_token: str, access_token_secret: str):
        """
        Load the access token and secret into the manager.

        :param access_token: The access token.
        :param access_token_secret: The access token secret.
        """
        self.access_token = access_token
        self.access_token_secret = access_token_secret
        self._oauth_client = Client(
            self.consumer_key,
            client_secret=self.consumer_secret,
            resource_owner_key=self.access_token,
            resource_owner_secret=self.access_token_secret,
        )

    def get_access_token(self):
        return self.access_token, self.access_token_secret

    def get_request_token(self):
        return self._request_token, self._request_token_secret

    def sign_request(
        self, url: str, http_method: str = "GET", **kwargs
    ) -> tuple[str, dict, dict]:
        """
        Sign a request with the OAuth client.

        :param url: The URL to sign.
        :param http_method: The HTTP method to use.
        :param kwargs: Additional parameters to pass.
        :return: The signed URL, headers, and body.
        """
        if not self.access_token:
            raise USOSAPIException("Access token not set. Did you forget to authorize?")
        url, headers, body = self._oauth_client.sign(
            url, http_method=http_method, **kwargs
        )
        return url, headers, body

    async def _handle_response_errors(self, response: aiohttp.ClientResponse):
        """
        Handle errors in the response.

        :param response: The response to handle.
        :raises USOSAPIException: If an error occurred.
        """
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
        """
        Revoke the current access token.
        """
        url = f"{self.base_address}{self.REVOKE_TOKEN_SUFFIX}"
        url, headers, body = self._oauth_client.sign(url, http_method="POST")
        async with self._session.post(url, data=body, headers=headers) as response:
            await self._handle_response_errors(response)
            _LOGGER.info("Token revoked successfully.")

    async def logout(self):
        """
        Log out the user.
        """
        if not self.access_token:
            return
        await self._revoke_token()
        self.access_token = None
