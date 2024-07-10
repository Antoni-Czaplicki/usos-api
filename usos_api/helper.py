from typing import TYPE_CHECKING, List

from usos_api.models import CourseEdition, Grade

if TYPE_CHECKING:
    from usos_api import USOSClient


class APIHelper:
    def __init__(self, client: "USOSClient"):
        self.client = client

    async def get_user_end_grades_with_weights(
        self, current_term_only: bool = False
    ) -> List[Grade]:
        """
        Get user end grades with weights.

        :param current_term_only: If True, only consider the current term.
        :return: A list of user end grades with weights.
        """
        ects_by_term = await self.client.course_service.get_user_courses_ects()
        terms = await self.client.term_service.get_terms(list(ects_by_term.keys()))
        term_ids = [
            term.id for term in terms if not current_term_only or term.is_current
        ]
        course_ids = [
            course_id
            for term_id in term_ids
            for course_id in ects_by_term[term_id].keys()
        ]

        courses = {
            course.id: course
            for course in await self.client.course_service.get_courses(course_ids)
        }
        grades_by_term = await self.client.grade_service.get_grades_by_terms(term_ids)

        user_grades = []
        for term in terms:
            if term.id not in term_ids:
                continue
            for course_id, ects in ects_by_term[term.id].items():
                grades = (
                    grades_by_term[term.id].get(course_id, {}).get("course_grades", [])
                )
                for grade in grades:
                    grade.weight = ects
                    grade.course_edition = CourseEdition(
                        course=courses[course_id], term=term
                    )
                    user_grades.append(grade)

        return user_grades
