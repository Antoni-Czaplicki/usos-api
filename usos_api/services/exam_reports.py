from datetime import date, datetime
from typing import TypeAlias

from ..connection import USOSAPIConnection
from ..models.exam_report import (
    ExamReport,
    ExamReport2,
    ExamReport2ClassGroup,
    ExamReport2Session,
    ExamReport2StudentGrade,
    ExamReport2UserGrade,
    ExamReportSession,
    ExamReportSessionAccess,
    ExamReportType,
    GradeType,
    GradeValue,
    LegacyCourseEditionExamReport,
    LegacyUserExamReportsByTerm,
    RawUserExamReportsByTerm,
    UserExamReportsByTerm,
    parse_legacy_course_edition_exam_report,
    parse_legacy_user_exam_reports,
    parse_user_exam_reports,
)

EmptyResponse: TypeAlias = dict[str, object]


def _join_fields(fields: list[str] | str | None) -> str | None:
    if isinstance(fields, list):
        return "|".join(fields)
    return fields


def _bool_param(value: bool) -> str:
    return str(value).lower()


class ExamReportService:
    """
    A service for exam report-related operations.
    """

    def __init__(self, connection: USOSAPIConnection):
        """
        Initialize the exam report service.

        :param connection: The connection to use.
        """
        self.connection = connection

    async def get_class_group(
            self,
            examrep_id: str | int,
            course_unit_id: str,
            group_number: str | int,
            fields: list[str] | str,
    ) -> ExamReport2ClassGroup:
        """
        Get class group and grades in given group for given exam report.

        :param examrep_id: ID of exam report.
        :param course_unit_id: ID of course unit.
        :param group_number: Group number.
        :param fields: Selector of result fields you are interested in.
        :return: A dictionary of selected fields and their values.
        """
        response = await self.connection.post(
            "services/examrep2/class_group",
            examrep_id=examrep_id,
            course_unit_id=course_unit_id,
            group_number=group_number,
            fields=_join_fields(fields),
        )
        return ExamReport2ClassGroup.model_validate(response)

    async def get_examinee_exam_reports(
            self,
            user_id: str | int,
            fields: list[str] | str | None = None,
    ) -> list[ExamReport2]:
        """
        Get exam reports that allow the access token issuer to update a student's grades.

        :param user_id: ID of the student.
        :param fields: Selector of result fields you are interested in.
        :return: List of exam report objects.
        """
        response = await self.connection.post(
            "services/examrep2/examinee",
            user_id=user_id,
            fields=_join_fields(fields),
        )
        return [ExamReport2.model_validate(report) for report in response]

    async def get_exam_report(
            self,
            examrep_id: str | int,
            fields: list[str] | str | None = None,
    ) -> ExamReport2:
        """
        Get information about an exam report.

        :param examrep_id: ID of exam report.
        :param fields: Selector of result fields you are interested in.
        :return: A dictionary of selected fields and their values.
        """
        response = await self.connection.post(
            "services/examrep2/examrep",
            examrep_id=examrep_id,
            fields=_join_fields(fields),
        )
        return ExamReport2.model_validate(response)

    async def get_exam_report_session(
            self,
            examrep_id: str | int,
            examrep_session_number: str | int,
            fields: list[str] | str | None = None,
    ) -> ExamReport2Session:
        """
        Get information about an exam report session.

        :param examrep_id: ID of exam report.
        :param examrep_session_number: Exam report session number.
        :param fields: Selector of result fields you are interested in.
        :return: A dictionary of selected fields and their values.
        """
        response = await self.connection.post(
            "services/examrep2/examrep_session",
            examrep_id=examrep_id,
            examrep_session_number=examrep_session_number,
            fields=_join_fields(fields),
        )
        return ExamReport2Session.model_validate(response)

    async def get_exam_report_session_access(
            self,
            examrep_id: str | int,
            examrep_session_number: str | int,
            access_type: str,
            fields: list[str] | str | None = None,
    ) -> list[ExamReportSessionAccess]:
        """
        Get access information for an exam report session.

        :param examrep_id: ID of exam report.
        :param examrep_session_number: Exam report session number.
        :param access_type: Access type requested by the API parameter named ``type``.
        :param fields: Selector of result fields you are interested in.
        :return: A dictionary of selected fields and their values.
        """
        response = await self.connection.post(
            "services/examrep2/examrep_session_access",
            examrep_id=examrep_id,
            examrep_session_number=examrep_session_number,
            type=access_type,
            fields=_join_fields(fields),
        )
        return [ExamReportSessionAccess.model_validate(access) for access in response]

    async def get_exam_report_type(
            self,
            examrep_type_id: str | int,
            fields: list[str] | str | None = None,
    ) -> ExamReportType:
        """
        Get information about an exam report type.

        :param examrep_type_id: ID of exam report type.
        :param fields: Selector of result fields you are interested in.
        :return: A dictionary of selected fields and their values.
        """
        response = await self.connection.post(
            "services/examrep2/examrep_type",
            examrep_type_id=examrep_type_id,
            fields=_join_fields(fields),
        )
        return ExamReportType.model_validate(response)

    async def get_grade_type(
            self,
            grade_type_id: str | int,
            fields: list[str] | str | None = None,
    ) -> GradeType:
        """
        Get information about a grade type.

        :param grade_type_id: ID of grade type.
        :param fields: Selector of result fields you are interested in.
        :return: A dictionary of selected fields and their values.
        """
        response = await self.connection.post(
            "services/examrep2/grade_type",
            grade_type_id=grade_type_id,
            fields=_join_fields(fields),
        )
        return GradeType.model_validate(response)

    async def get_grade_value(
            self,
            grade_type_id: str | int,
            order_key: str | int,
            fields: list[str] | str | None = None,
    ) -> GradeValue:
        """
        Get information about a grade value.

        :param grade_type_id: ID of grade type.
        :param order_key: Grade value order key.
        :param fields: Selector of result fields you are interested in.
        :return: A dictionary of selected fields and their values.
        """
        response = await self.connection.post(
            "services/examrep2/grade_value",
            grade_type_id=grade_type_id,
            order_key=order_key,
            fields=_join_fields(fields),
        )
        return GradeValue.model_validate(response)

    async def get_grader_exam_reports(
            self,
            only_writable: bool = False,
            active_terms_only: bool = True,
            fields: list[str] | str | None = None,
    ) -> list[ExamReport2]:
        """
        Get exam reports that the access token issuer can access.

        :param only_writable: Whether to return only writable exam reports.
        :param active_terms_only: Whether to return only exam reports from active terms.
        :param fields: Selector of result fields you are interested in.
        :return: List of exam report objects.
        """
        response = await self.connection.post(
            "services/examrep2/grader",
            only_writable=_bool_param(only_writable),
            active_terms_only=_bool_param(active_terms_only),
            fields=_join_fields(fields),
        )
        return [ExamReport2.model_validate(report) for report in response]

    async def get_student_grade(
            self,
            examrep_id: str | int,
            examrep_session_number: str | int,
            student_id: str | int,
            fields: list[str] | str | None = None,
    ) -> ExamReport2StudentGrade:
        """
        Get information about a student's grade in an exam report session.

        :param examrep_id: ID of exam report.
        :param examrep_session_number: Exam report session number.
        :param student_id: ID of student.
        :param fields: Selector of result fields you are interested in.
        :return: A dictionary of selected fields and their values.
        """
        response = await self.connection.post(
            "services/examrep2/student_grade",
            examrep_id=examrep_id,
            examrep_session_number=examrep_session_number,
            student_id=student_id,
            fields=_join_fields(fields),
        )
        return ExamReport2StudentGrade.model_validate(response)

    async def get_student_grades(
            self,
            examrep_id: str | int,
            student_id: str | int,
            fields: list[str] | str | None = None,
    ) -> list[ExamReport2StudentGrade]:
        """
        Get information about all of a student's grades from a single exam report.

        :param examrep_id: ID of exam report.
        :param student_id: ID of student.
        :param fields: Selector of result fields you are interested in.
        :return: List of student grade objects.
        """
        response = await self.connection.post(
            "services/examrep2/student_grades",
            examrep_id=examrep_id,
            student_id=student_id,
            fields=_join_fields(fields),
        )
        return [ExamReport2StudentGrade.model_validate(grade) for grade in response]

    async def update_student_grade(
            self,
            student_id: str | int,
            examrep_id: str | int,
            examrep_session_number: str | int,
            value_symbol: str | None = None,
            comment: str | None = None,
            private_comment: str | None = None,
            date_modified: date | datetime | str | None = None,
            date_acquisition: date | datetime | str | None = None,
    ) -> EmptyResponse:
        """
        Update a student's grade in an exam report session.

        :param student_id: ID of student.
        :param examrep_id: ID of exam report.
        :param examrep_session_number: Exam report session number.
        :param value_symbol: Grade value symbol.
        :param comment: Comment visible to the student.
        :param private_comment: Comment visible to graders only.
        :param date_modified: Grade modification date.
        :param date_acquisition: Grade acquisition date.
        :return: Empty dictionary on success.
        """
        return await self.connection.post(
            "services/examrep2/update_student_grade",
            student_id=student_id,
            examrep_id=examrep_id,
            examrep_session_number=examrep_session_number,
            value_symbol=value_symbol,
            comment=comment,
            private_comment=private_comment,
            date_modified=date_modified,
            date_acquisition=date_acquisition,
        )

    async def get_user_grade(
            self,
            examrep_id: str | int,
            examrep_session_number: str | int,
            fields: list[str] | str | None = None,
    ) -> ExamReport2UserGrade:
        """
        Get the access token issuer's grade in an exam report session.

        :param examrep_id: ID of exam report.
        :param examrep_session_number: Exam report session number.
        :param fields: Selector of result fields you are interested in.
        :return: A dictionary of selected fields and their values.
        """
        response = await self.connection.post(
            "services/examrep2/user_grade",
            examrep_id=examrep_id,
            examrep_session_number=examrep_session_number,
            fields=_join_fields(fields),
        )
        return ExamReport2UserGrade.model_validate(response)

    async def get_course_edition_exam_report(
            self,
            course_id: str,
            term_id: str,
            fields: list[str] | str | None = None,
    ) -> LegacyCourseEditionExamReport:
        """
        Get legacy exam report information related to a course edition.

        This wraps ``services/examrep/course_edition``.

        :param course_id: Course ID.
        :param term_id: Academic term ID.
        :param fields: Selector of result fields you are interested in.
        :return: A dictionary of selected fields and their values.
        """
        response = await self.connection.post(
            "services/examrep/course_edition",
            course_id=course_id,
            term_id=term_id,
            fields=_join_fields(fields),
        )
        return parse_legacy_course_edition_exam_report(response)

    async def get_course_edition_exam_reports(
            self,
            course_id: str,
            term_id: str,
            fields: list[str] | str | None = None,
    ) -> LegacyCourseEditionExamReport:
        """
        Get legacy exam reports related to a course edition.

        This wraps ``services/examrep/course_edition2``.

        :param course_id: Course ID.
        :param term_id: Academic term ID.
        :param fields: Selector of result fields you are interested in.
        :return: A dictionary of selected fields and their values.
        """
        response = await self.connection.post(
            "services/examrep/course_edition2",
            course_id=course_id,
            term_id=term_id,
            fields=_join_fields(fields),
        )
        return parse_legacy_course_edition_exam_report(response)

    async def get_legacy_exam_report(
            self,
            exam_id: str | int,
            fields: list[str] | str | None = None,
    ) -> ExamReport:
        """
        Get legacy exam report information.

        This wraps ``services/examrep/exam``.

        :param exam_id: Exam report ID.
        :param fields: Selector of result fields you are interested in.
        :return: A dictionary of selected fields and their values.
        """
        response = await self.connection.post(
            "services/examrep/exam",
            id=exam_id,
            fields=_join_fields(fields),
        )
        return ExamReport.model_validate(response)

    async def get_legacy_exam_session(
        self,
        exam_id: str | int,
        number: str | int,
        fields: list[str] | str | None = None,
    ) -> ExamReportSession:
        """
        Get legacy exam report session information.

        This wraps ``services/examrep/exam_session``.

        :param exam_id: Exam report ID.
        :param number: Exam session number.
        :param fields: Selector of result fields you are interested in.
        :return: A dictionary of selected fields and their values.
        """
        response = await self.connection.post(
            "services/examrep/exam_session",
            exam_id=exam_id,
            number=number,
            fields=_join_fields(fields),
        )
        return ExamReportSession.model_validate(response)

    async def get_legacy_user_exam_reports(
        self,
        term_ids: list[str] | str,
        fields: list[str] | str | None = None,
    ) -> LegacyUserExamReportsByTerm:
        """
        Get the current user's legacy exam reports for selected terms.

        This wraps ``services/examrep/user``.

        :param term_ids: Academic term IDs.
        :param fields: Selector of result fields you are interested in.
        :return: A dictionary mapping term IDs to course IDs to exam report groups.
        """
        response = await self.connection.post(
            "services/examrep/user",
            term_ids=_join_fields(term_ids),
            fields=_join_fields(fields),
        )
        return parse_legacy_user_exam_reports(response)

    async def get_raw_user_exam_reports(
        self,
        term_ids: list[str] | str | None = None,
        fields: list[str] | str | None = None,
    ) -> RawUserExamReportsByTerm:
        """
        Get the current user's legacy exam reports as raw API dictionaries.

        This wraps ``services/examrep/user2``.

        :param term_ids: Academic term IDs. If omitted, the API default is used.
        :param fields: Selector of result fields you are interested in.
        :return: Raw dictionary mapping term IDs to course IDs to exam report lists.
        """
        return await self.connection.post(
            "services/examrep/user2",
            term_ids=_join_fields(term_ids),
            fields=_join_fields(fields),
        )

    async def get_user_exam_reports(
        self,
        term_ids: list[str] | str | None = None,
        fields: list[str] | str | None = None,
    ) -> UserExamReportsByTerm:
        """
        Get the current user's legacy exam reports for selected terms.

        This wraps ``services/examrep/user2`` and parses the response into
        Pydantic models.

        :param term_ids: Academic term IDs. If omitted, the API default is used.
        :param fields: Selector of exam report fields you are interested in.
        :return: A dictionary mapping term IDs to course IDs to exam report models.
        """
        return parse_user_exam_reports(
            await self.get_raw_user_exam_reports(term_ids=term_ids, fields=fields)
        )
