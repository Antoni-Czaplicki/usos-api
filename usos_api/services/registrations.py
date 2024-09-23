from ..connection import USOSAPIConnection
from ..models import CoursesCart, Registration


class RegistrationService:
    """
    A service for registration-related operations.
    """

    def __init__(self, connection: USOSAPIConnection):
        """
        Initialize the registration service.

        :param connection: The connection to use.
        """
        self.connection = connection

    async def get_user_registrations(
        self, active_only: bool = True, fields: list[str] = None
    ) -> list[Registration]:
        """
        Get user registrations.

        :param active_only: Whether to return only active registrations.
        :param fields: Selector of result fields you are interested in (optional, default is specified fields).
        :return: The user registrations.
        """
        fields = "|".join(fields) if fields else None

        response = await self.connection.post(
            "services/registrations/user_registrations",
            fields=fields,
            active_only=active_only,
        )
        return [Registration(**registration) for registration in response]

    async def get_registration(
        self, registration_id: str, fields: list[str] = None
    ) -> Registration:
        """
        Get a registration.

        :param registration_id: The ID of the registration.
        :param fields: Selector of result fields you are interested in (optional, default is specified fields).
        :return: The registration.
        """

        fields = "|".join(fields) if fields else None

        response = await self.connection.post(
            "services/registrations/registration", id=registration_id, fields=fields
        )
        return Registration(**response)

    async def register_to_course(
        self,
        round_id: str,
        course_id: str,
        term_id: str,
        user_programme_id: str = None,
        user_stage_id: str = None,
    ) -> dict:
        """
        Register to a course.

        :param round_id: Registration round ID.
        :param course_id: Course code.
        :param term_id: Cycle code.
        :param user_programme_id: User program ID (optional).
        :param user_stage_id: User stage ID (optional).
        :return: Empty dict on success.
        """
        data = {
            "round_id": round_id,
            "course_id": course_id,
            "term_id": term_id,
        }
        if user_programme_id:
            data["user_programme_id"] = user_programme_id
        if user_stage_id:
            data["user_stage_id"] = user_stage_id

        response = await self.connection.post("services/registrations/register", **data)
        return response

    async def get_courses_cart(self, fields: list[str] = None) -> list[CoursesCart]:
        """
        Get user courses cart with registrations information.

        :param fields: Selector of result fields you are interested in (optional, default is specified fields).
        :return: A CoursesCartResponse object.
        """
        if fields is None:
            fields = [
                "links",
                "course",
                "term",
                "user_registration_status",
                "is_registration_valid",
                "choice_number",
                "limits",
                "is_linkage_required",
                "registrations_count",
                "registration_status",
                "active_registration_round_id",
            ]
        fields = "|".join(fields)

        response = await self.connection.post(
            "services/registrations/courses_cart", fields=fields
        )
        return [CoursesCart(**course) for course in response]
