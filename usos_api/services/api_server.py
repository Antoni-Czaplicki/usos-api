from typing import List

from usos_api.models.consumer import Consumer


class APIServerService:
    """
    A service for APIServer-related operations.
    """

    def __init__(self, connection):
        """
        Initialize the APIServerService.

        :param connection: The connection to use.
        """
        self.connection = connection

    async def get_consumer_info(self, fields: List[str] | None = None) -> Consumer:
        """
        Get information on the Consumer.

        :param fields: The fields to include in the response.
        :return: A dictionary of fields you have asked for.
        """
        if not fields:
            fields = [
                "name",
                "url",
                "email",
                "date_registered",
                "administrative_methods",
                "token_scopes",
            ]
        fields = "|".join(fields)
        response = await self.connection.post("services/apisrv/consumer", fields=fields)
        return self._deserialize_consumer(response)

    def _deserialize_consumer(self, data: dict) -> Consumer:
        return Consumer(**data)
