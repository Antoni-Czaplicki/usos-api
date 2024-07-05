import aiohttp

from .auth import AuthManager
from .exceptions import USOSAPIException
from .logger import get_logger

_LOGGER = get_logger("usos-api")
_DOWNLOAD_LOGGER = get_logger("usos-api-download")


class USOSAPIConnection:
    def __init__(self, api_base_address: str, consumer_key: str, consumer_secret: str):
        self.base_address = api_base_address.rstrip("/") + "/"
        self.auth_manager = AuthManager(
            self.base_address, consumer_key, consumer_secret
        )
        self._session = None

    async def __aenter__(self) -> "USOSAPIConnection":
        await self.open()
        return self

    async def __aexit__(self, exc_type, exc_value, traceback):
        await self.close()

    async def open(self):
        self._session = aiohttp.ClientSession()
        await self.auth_manager.open()

    async def close(self):
        if self._session:
            await self._session.close()
        await self.auth_manager.close()

    async def test_connection(self) -> bool:
        url = f"{self.base_address}services/apisrv/now"
        async with self._session.get(url) as response:
            return response.status == 200

    async def get(self, service: str, **kwargs) -> dict:
        kwargs = {k: str(v) for k, v in kwargs.items() if v is not None}
        headers = {"Content-Type": "application/x-www-form-urlencoded"}
        url = f"{self.base_address}{service}"
        url, headers, body = await self.auth_manager.sign_request(
            url, http_method="POST", body=kwargs, headers=headers
        )
        async with self._session.post(url, data=body, headers=headers) as response:
            await self._handle_response_errors(response)
            return await response.json()

    async def _handle_response_errors(self, response: aiohttp.ClientResponse):
        if response.status != 200:
            text = await response.text()
            if response.status == 401:
                raise USOSAPIException(
                    "HTTP 401: Unauthorized. Your access key probably expired."
                )
            elif response.status == 400:
                raise USOSAPIException(f"HTTP 400: Bad request: {text}")
            else:
                raise USOSAPIException(f"HTTP {response.status}: {text}")
