from typing import TYPE_CHECKING, List

from usos_api.models import CourseEdition, Grade
from usos_api.services.courses import CourseEctsByTerm
from usos_api.services.exam_reports import UserExamReportsByTerm

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
            term.id for term in terms if not current_term_only or term.is_ongoing
        ]

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
                        course_id=course_id, term_id=term.id
                    )
                    user_grades.append(grade)

        return user_grades

    async def get_user_exam_reports_with_ects(
        self,
        term_ids: list[str] | str | None = None,
        fields: list[str] | str | None = None,
    ) -> tuple[CourseEctsByTerm, UserExamReportsByTerm]:
        """
        Fetch raw user exam reports together with course ECTS weights.

        This helper intentionally does not shape grades for a specific app. It only
        coordinates the USOS calls that are usually needed together.

        :param term_ids: Academic term IDs. If omitted, terms from ECTS data are used.
        :param fields: Selector of exam report fields you are interested in.
        :return: ``(ects_by_term, reports_by_term)`` for the selected terms.
        """
        all_ects_by_term = await self.client.course_service.get_user_courses_ects()
        selected_term_ids = _term_ids(term_ids) or list(all_ects_by_term.keys())
        if not selected_term_ids:
            return {}, {}

        reports_by_term = await self.client.exam_report_service.get_user_exam_reports(
            term_ids=selected_term_ids,
            fields=fields,
        )
        ects_by_term = {
            term_id: all_ects_by_term.get(term_id, {}) for term_id in selected_term_ids
        }
        return ects_by_term, reports_by_term


def _term_ids(term_ids: list[str] | str | None) -> list[str]:
    if term_ids is None:
        return []
    if isinstance(term_ids, str):
        return [term_ids]
    return term_ids
