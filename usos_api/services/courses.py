from typing import Optional

from ..connection import USOSAPIConnection
from ..models import Course, CourseEdition, Term


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

    async def get_user_course_editions(
        self,
        active_terms_only: bool = False,
        ongoing_terms_only: bool = False,
    ) -> list[CourseEdition]:
        """
        Get information on user's courses.

        This is a BETA method. We're looking for beta-testers. Until we find them, there's a substantial probability it won't stay backwards-compatible!
        If you are planning on using this method, please let us know. Then, we will work with you and move it out of beta as soon as we can.

        :param active_terms_only: Return only these course editions which are related to the currently active academic terms. Apparently, this parameter does not always work as expected, so you can use `ongoing_terms_only` instead.
        :param ongoing_terms_only: Return only these course editions which are related to the currently ongoing academic terms (filtered locally based on start and finish dates).
        :return: A dictionary of selected fields and their values.
        """
        params = {
            "fields": "course_editions[course_id|course_name|term_id|homepage_url|profile_url|coordinators|lecturers|passing_status|user_groups|grades|attributes]|terms",
            "active_terms_only": str(active_terms_only).lower(),
        }

        response = await self.connection.post("services/courses/user", **params)

        terms = {term["id"]: Term(**term) for term in response["terms"]}
        ongoing_terms = {term_id for term_id, term in terms.items() if term.is_ongoing}

        return [
            CourseEdition(**course_edition)
            for term_id, course_editions in response["course_editions"].items()
            if not ongoing_terms_only or term_id in ongoing_terms
            for course_edition in course_editions
        ]
