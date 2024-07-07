import json

from .connection import USOSAPIConnection
from .logger import get_logger
from .services import UserService
from .services.api_server import APIServerService
from .services.groups import GroupService

_LOGGER = get_logger("USOSClient")


class USOSClient:
    """
    A client for the USOS API.

    :var UserService user_service: The user service.
    :var GroupService group_service: The group service.
    :var APIServerService api_server_service: The API server service.

    :ivar USOSAPIConnection connection: The connection to the USOS API, used for making requests.
    """

    def __init__(
        self, api_base_address: str, consumer_key: str, consumer_secret: str
    ) -> None:
        """
        Initialize the USOS API client.

        :param api_base_address: The base address of the USOS API.
        :param consumer_key: Consumer key obtained from the USOS API.
        :param consumer_secret: Consumer secret obtained from the USOS API.
        """
        self.connection = USOSAPIConnection(
            api_base_address, consumer_key, consumer_secret
        )
        self.user_service = UserService(self.connection)
        self.group_service = GroupService(self.connection)
        self.api_server_service = APIServerService(self.connection)

    async def __aenter__(self) -> "USOSClient":
        """
        Enter the client.

        :return: The client.
        """
        await self.open()
        return self

    async def __aexit__(self, exc_type, exc_value, traceback):
        """
        Exit the client.

        :param exc_type: The exception type.
        :param exc_value: The exception value.
        :param traceback: The traceback.
        """
        await self.close()

    async def close(self) -> None:
        """
        Close the client.
        """
        await self.connection.close()

    async def open(self) -> None:
        """
        Open the client.
        """
        await self.connection.open()

    def set_scopes(self, scopes: list[str]) -> None:
        """
        Set the scopes for the client.

        :param scopes: The scopes to set.
        """
        self.connection.auth_manager.SCOPES = "|".join(scopes)

    def add_scope(self, scope: str) -> None:
        """
        Add a scope to the client.

        :param scope: The scope to add.
        """
        self.connection.auth_manager.SCOPES += f"|{scope}"

    def remove_scope(self, scope: str) -> None:
        """
        Remove a scope from the client.

        :param scope: The scope to remove.
        """
        self.connection.auth_manager.SCOPES = "|".join(
            [s for s in self.connection.auth_manager.SCOPES.split("|") if s != scope]
        )

    async def authorize(self, verifier: str, request_token: str = None, request_token_secret: str = None) -> tuple[str, str]:
        """
        Authorize the client with verifier and optionally token and token secret.

        Parameters `token` and `token_secret` can be useful when you create a new client instance and want to authorize it with the token and secret obtained from another client instance.

        :param verifier: The verifier to authorize the client with.
        :param request_token: The OAuth token obtained from the previous step.
        :param request_token_secret: The OAuth token secret obtained from the previous step.
        :return: The access token and secret.
        """
        return await self.connection.auth_manager.authorize(verifier, request_token, request_token_secret)

    async def get_authorization_url(self, callback_url: str = "oob"):
        """
        Get the URL to authorize the client.

        :param callback_url: The URL to redirect to after authorization, leave as "oob" for pin-based authorization.
        :return: The URL to authorize the client.
        """
        return await self.connection.auth_manager.get_authorization_url(callback_url)

    def load_access_token(self, access_token: str, access_token_secret: str):
        """
        Load the access token and secret into the client.

        :param access_token: The access token.
        :param access_token_secret: The access token secret.
        """
        self.connection.auth_manager.load_access_token(
            access_token, access_token_secret
        )

    def load_access_token_from_json(self, json_data: dict):
        """
        Load the access token and secret from a JSON object.

        :param json_data: The JSON object containing the access token and secret.
        """
        try:
            access_token = json_data["access_token"]
            access_token_secret = json_data["access_token_secret"]
        except KeyError:
            raise ValueError("Invalid JSON data.")
        self.load_access_token(access_token, access_token_secret)

    async def load_access_token_from_file(
        self, file_path: str = "usos_api_access_token.json"
    ) -> None:
        """
        Load the access token and secret from a JSON file.

        :param file_path: The path to the JSON file.
        """
        if not file_path.endswith(".json"):
            raise ValueError("File must be a JSON file.")
        with open(file_path, "r") as file:
            json_data = json.load(file)
        self.load_access_token_from_json(json_data)

    async def save_access_token_to_file(
        self, file_path: str = "usos_api_access_token.json"
    ) -> None:
        """
        Save the access token and secret to a JSON file.

        :param file_path: The path to the JSON file.
        """
        if not file_path.endswith(".json"):
            raise ValueError("File must be a JSON file.")
        access_token, access_token_secret = self.connection.auth_manager.get_access_token()
        json_data = {
            "access_token": access_token,
            "access_token_secret": access_token_secret,
        }
        with open(file_path, "w") as file:
            json.dump(json_data, file)

    async def test_connection(self) -> bool:
        """
        Test the connection to the USOS API.

        :return: True if the connection is successful, False otherwise.
        """
        return await self.connection.test_connection()
