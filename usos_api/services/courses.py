from typing import Optional

from ..connection import USOSAPIConnection
from ..models import Course


class CourseService:
    """
    A service for course-related operations.
    """

    def __init__(self, connection: USOSAPIConnection):
        """
        Initialize the course service.

        :param connection: The connection to use.
        """
        self.connection = connection

    async def get_user_courses_ects(self) -> dict[str, dict[str, float]]:
        """
        Get user courses ECTS.

        :return: The user courses ECTS.
        """
        response = await self.connection.post("services/courses/user_ects_points")
        return {
            term: {course: float(points) for course, points in courses.items()}
            for term, courses in response.items()
        }

    async def get_courses(
        self, course_ids: list[str], fields: Optional[list[str]] = None
    ) -> list[Course]:
        """
        Get courses by their IDs.

        :param course_ids: The IDs of the courses to get.
        :param fields: The fields to include in the response.
        :return: A list of courses.
        """
        if not course_ids:
            return []

        course_ids_str = "|".join(course_ids)
        fields_str = "|".join(fields) if fields else "id|name"

        response = await self.connection.post(
            "services/courses/courses", course_ids=course_ids_str, fields=fields_str
        )

        return [Course(**course_data) for course_data in response.values()]
