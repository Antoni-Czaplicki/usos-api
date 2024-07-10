from ..connection import USOSAPIConnection
from ..models import Grade


class GradeService:
    """
    A service for grade-related operations.
    """

    def __init__(self, connection: USOSAPIConnection):
        """
        Initialize the grade service.

        :param connection: The connection to use.
        """
        self.connection = connection

    async def get_grades_by_terms(
        self, term_ids: list[str] | str, fields: list[str] = None
    ) -> dict[str, dict[str, dict[str, dict[str, Grade] | list[Grade]]]]:
        """
        Get grades by terms.

        :param term_ids: The IDs of the terms to get grades for, or a single term ID.
        :param fields: The fields to include in the response.
        :return: The grades.
        """
        term_ids = [term_ids] if isinstance(term_ids, str) else term_ids
        fields = fields or [
            "value_symbol",
            "passes",
            "value_description",
            "exam_id",
            "exam_session_number",
            "counts_into_average",
        ]

        response = await self.connection.post(
            "services/grades/terms2",
            term_ids="|".join(term_ids),
            fields="|".join(fields),
        )

        new_response = {}
        term_id: str
        for term_id, courses in response.items():
            new_response[term_id] = self._process_courses(courses)

        return new_response

    def _process_courses(
        self, courses: dict
    ) -> dict[str, dict[str, dict[str, Grade] | list[Grade]]]:
        """
        Process courses to extract grades.

        :param courses: The courses to process.
        :return: The processed courses with grades.
        """
        processed_courses = {}
        for course_id, grades in courses.items():
            course_units_grades = self._process_course_units_grades(
                grades["course_units_grades"]
            )
            course_grades = self._process_course_grades(grades["course_grades"])
            processed_courses[course_id] = {
                "course_units_grades": course_units_grades,
                "course_grades": course_grades,
            }
        return processed_courses

    def _process_course_units_grades(
        self, course_units_grades: dict
    ) -> dict[str, dict[str, Grade]]:
        """
        Process course units grades.

        :param course_units_grades: The course units grades to process.
        :return: The processed course units grades.
        """
        processed_units_grades = {}
        for unit_id, units in course_units_grades.items():
            processed_units_grades[unit_id] = {
                exam_session_number: Grade(**grade)
                for unit in units
                for exam_session_number, grade in unit.items()
            }
        return processed_units_grades

    def _process_course_grades(self, course_grades: list) -> list[Grade]:
        """
        Process course grades.

        :param course_grades: The course grades to process.
        :return: The processed course grades.
        """
        return [
            Grade(**grade) for session in course_grades for grade in session.values()
        ]
