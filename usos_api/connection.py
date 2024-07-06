from urllib.parse import urlencode, urlparse

import aiohttp

from .auth import AuthManager
from .exceptions import USOSAPIException
from .logger import get_logger

_LOGGER = get_logger("usos-api")
_DOWNLOAD_LOGGER = get_logger("usos-api-download")


class USOSAPIConnection:
    """
    A connection to the USOS API.
    """

    def __init__(self, api_base_address: str, consumer_key: str, consumer_secret: str):
        """
        Initialize the USOS API connection.

        :param api_base_address: The base address of the USOS API.
        :param consumer_key: Consumer key obtained from the USOS API.
        :param consumer_secret: Consumer secret obtained from the USOS API.
        """
        self.base_address = api_base_address.rstrip("/") + "/"
        self.auth_manager = AuthManager(
            self.base_address, consumer_key, consumer_secret
        )
        self._session = None

    async def __aenter__(self) -> "USOSAPIConnection":
        """
        Enter the connection.

        :return: The connection.
        """
        await self.open()
        return self

    async def __aexit__(self, exc_type, exc_value, traceback):
        """
        Exit the connection.

        :param exc_type: The exception type.
        :param exc_value: The exception value.
        :param traceback: The traceback.
        """
        await self.close()

    async def open(self):
        """
        Open the connection.
        """
        self._session = aiohttp.ClientSession()
        await self.auth_manager.open()

    async def close(self):
        """
        Close the connection.
        """
        if self._session:
            await self._session.close()
        await self.auth_manager.close()

    async def test_connection(self) -> bool:
        """
        Test the connection to the USOS API.
        :return: True if the connection is successful, False otherwise.
        """
        url = f"{self.base_address}services/apisrv/now"
        async with self._session.get(url) as response:
            return response.status == 200

    async def get(self, service: str, **kwargs) -> dict:
        """
        Perform a GET request to the USOS API.

        From the USOS API documentation:
        You may call all the services with GET or POST methods (POST preferred).

        :param service: The service to call.
        :param kwargs: The parameters to pass.
        :return: The response data.
        """
        kwargs = {k: str(v) for k, v in kwargs.items() if v is not None}
        headers = {}
        url_parts = [f"{self.base_address}{service}"]
        query_string = urlparse(url_parts[0]).query
        url_parts.append("&" if query_string else "?")
        url_parts.append(urlencode(kwargs))
        url, headers, body = self.auth_manager.sign_request(
            "".join(url_parts), headers=headers
        )
        print(url, headers, body)
        async with self._session.get(url, params=kwargs, headers=headers) as response:
            await self._handle_response_errors(response)
            return await response.json()

    async def post(self, service: str, **kwargs) -> dict:
        """
        Perform a POST request to the USOS API.

        From the USOS API documentation:
        You may call all the services with GET or POST methods (POST preferred).

        :param service: The service to call.
        :param kwargs: The parameters to pass.
        :return: The response data.
        """
        kwargs = {k: str(v) for k, v in kwargs.items() if v is not None}
        headers = {"Content-Type": "application/x-www-form-urlencoded"}
        url = f"{self.base_address}{service}"
        url, headers, body = self.auth_manager.sign_request(
            url, http_method="POST", body=kwargs, headers=headers
        )
        async with self._session.post(url, data=body, headers=headers) as response:
            await self._handle_response_errors(response)
            return await response.json()

    async def _handle_response_errors(self, response: aiohttp.ClientResponse):
        """
        Handle errors in the response.

        :param response: The response to handle.
        :raises USOSAPIException: If an error occurred.
        """
        if response.status != 200:
            text = await response.text()
            if response.status == 401:
                raise USOSAPIException(
                    f"HTTP 401: Unauthorized. Your access key probably expired. {text}"
                )
            elif response.status == 400:
                raise USOSAPIException(f"HTTP 400: Bad request: {text}")
            else:
                raise USOSAPIException(f"HTTP {response.status}: {text}")
