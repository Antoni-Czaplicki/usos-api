import json

from .connection import USOSAPIConnection
from .logger import get_logger
from .services import UserService

_LOGGER = get_logger("USOSClient")


class USOSClient:
    def __init__(self, api_base_address: str, consumer_key: str, consumer_secret: str):
        self.connection = USOSAPIConnection(
            api_base_address, consumer_key, consumer_secret
        )
        self.user_service = UserService(self.connection)

    async def __aenter__(self) -> "USOSClient":
        await self.connection.__aenter__()
        return self

    async def __aexit__(self, exc_type, exc_value, traceback):
        await self.close()

    async def close(self):
        await self.connection.close()

    async def authorize(self, token: str):
        return await self.connection.auth_manager.authorize_with_token(token)

    async def get_authorization_url(self, callback_url: str = "oob"):
        """
        Get the URL to authorize the client.

        :param callback_url: The URL to redirect to after authorization, leave as "oob" for pin-based authorization.
        :return:
        """
        return await self.connection.auth_manager.get_authorization_url(callback_url)

    async def load_access_token(self, access_token: str, access_token_secret: str):
        await self.connection.auth_manager.load_access_token(
            access_token, access_token_secret
        )

    async def load_access_token_from_json(self, json_data: dict):
        try:
            access_token = json_data["access_token"]
            access_token_secret = json_data["access_token_secret"]
        except KeyError:
            raise ValueError("Invalid JSON data.")
        await self.load_access_token(access_token, access_token_secret)

    async def load_access_token_from_file(
        self, file_path: str = "usos_api_access_token.json"
    ):
        if not file_path.endswith(".json"):
            raise ValueError("File must be a JSON file.")
        with open(file_path, "r") as file:
            json_data = json.load(file)
        await self.load_access_token_from_json(json_data)

    async def save_access_token_to_file(
        self, file_path: str = "usos_api_access_token.json"
    ):
        if not file_path.endswith(".json"):
            raise ValueError("File must be a JSON file.")
        json_data = {
            "access_token": self.connection.auth_manager.access_token,
            "access_token_secret": self.connection.auth_manager.access_token_secret,
        }
        with open(file_path, "w") as file:
            json.dump(json_data, file)

    async def get_user(self, user_id: int | None = None):
        return await self.user_service.get_user(user_id)

    async def test_connection(self) -> bool:
        return await self.connection.test_connection()
