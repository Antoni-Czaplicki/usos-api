from ..connection import USOSAPIConnection
from ..models.user import User


class UserService:
    """
    A service for user-related operations.
    """

    def __init__(self, connection: USOSAPIConnection):
        """
        Initialize the user service.

        :param connection: The connection to use.
        """
        self.connection = connection

    async def get_user(
        self, user_id: int | None = None, fields: list[str] | None = None
    ) -> User:
        """
        Get a user by their ID or the currently authorized user.

        :param user_id: The ID of the user to get. If None, the currently authorized user will be returned.
        :param fields: The fields to include in the response. Whole list of fields can be found `here <https://apps.usos.pwr.edu.pl/developers/api/services/users/#user>`_.
        :return: The user.
        """

        if fields is None:
            fields = [
                "id",
                "first_name",
                "last_name",
                "email",
                "student_number",
                "student_programmes",
                "student_status",
                "staff_status",
                "has_photo",
                "photo_urls[original]",
            ]  # Default fields
        fields = "|".join(fields)
        response = await self.connection.post(
            "services/users/user", user_id=user_id, fields=fields
        )
        return self._deserialize_user(response)

    def _deserialize_user(self, data: dict) -> User:
        return User(**data)
