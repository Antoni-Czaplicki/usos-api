from ..connection import USOSAPIConnection
from ..models import StudentProgramme


class ProgrammeService:
    """
    A service for programme-related operations.
    """

    def __init__(self, connection: USOSAPIConnection):
        """
        Initialize the programme service.

        :param connection: The connection to use.
        """
        self.connection = connection

    async def get_student_programmes(
        self,
        user_id: int | None = None,
        fields: list[str] | None = None,
        active_only: bool = True,
    ) -> list[StudentProgramme]:
        """
        Get the programmes of a student.

        :param user_id: The ID of the student. If None, the currently authorized user is used.
        :param fields: The fields to include in the response. Whole list of fields can be found `here <https://apps.usos.pwr.edu.pl/developers/api/services/progs/#student_programme>`_.
        :param active_only: Whether to get only programmes with the status `active` or `graduated_before_diploma`.
        :return: The student programmes.
        """
        if fields is None:
            fields = [
                "id",
                "status",
                "admission_date",
                "is_primary",
                "stages",
                "programme[id|name|faculty[id|name]]",
            ]  # Default fields
        response = await self.connection.post(
            "services/progs/student",
            user_id=user_id,
            fields="|".join(fields),
            active_only="true" if active_only else "false",
        )
        return [StudentProgramme(**programme) for programme in response]
