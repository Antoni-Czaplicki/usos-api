from datetime import date, datetime
from typing import TypeAlias, TypedDict

from ..connection import USOSAPIConnection

ExternalObject: TypeAlias = dict[str, object]
EmptyResponse: TypeAlias = dict[str, object]


class LangDictData(TypedDict, total=False):
    pl: str | None
    en: str | None


class GradeValue(TypedDict, total=False):
    grade_type: ExternalObject
    order_key: str | int
    symbol: str
    passes: bool
    decimal_value: float | None
    name: LangDictData


class GradeType(TypedDict, total=False):
    id: str
    name: LangDictData
    values: list[GradeValue]


class ExamReportType(TypedDict, total=False):
    id: str
    name: LangDictData
    grade_type: GradeType


class ExamReport2StudentGrade(TypedDict, total=False):
    grade_value: GradeValue | None
    comment: str | None
    private_comment: str | None
    user: ExternalObject
    grader: ExternalObject
    last_updated: str | None
    is_editable: bool
    resignation: bool
    inactive_links: bool
    why_cannot_edit: str | None
    date_acquisition: str | None
    examrep_session: ExternalObject


class ExamReport2UserGrade(TypedDict, total=False):
    grade_value: GradeValue | None
    comment: str | None
    user: ExternalObject
    grader: ExternalObject
    last_updated: str | None


class ExamReport2Session(TypedDict, total=False):
    examrep_id: str | int
    number: int
    status: str
    description: LangDictData
    deadline: str | None
    is_open: bool
    is_acquisition_date_required: bool
    all_grades: dict[str, ExamReport2StudentGrade]
    issuer_grade: ExamReport2UserGrade
    read_access: list[ExternalObject]
    write_access: list[ExternalObject]


class ExamReport2(TypedDict, total=False):
    id: str | int
    description: LangDictData
    counts_into_average: bool
    grade_type: GradeType
    is_general_report: bool
    sessions: list[ExamReport2Session]
    edit_access: list[ExternalObject]
    course_edition: ExternalObject
    course_unit: ExternalObject
    active_sessions: list[ExamReport2Session]


class ExamReportSessionAccess(TypedDict, total=False):
    cause: str | None
    groups: list[ExternalObject]
    exam_groups: list[ExternalObject]
    unassigned: list[ExternalObject]


class ExamReport2ClassGroup(TypedDict, total=False):
    class_group: ExternalObject
    grades: dict[str, ExamReport2StudentGrade]


class ExamReportCourse(TypedDict, total=False):
    id: str
    name: LangDictData


class ExamReportCourseUnit(TypedDict, total=False):
    id: str
    course_id: str
    course_name: LangDictData
    classtype_id: str | None
    term_id: str


class ExamReportGradeDistributionItem(TypedDict, total=False):
    grade_symbol: str
    percentage: float


class ExamReportIssuerGrade(TypedDict, total=False):
    value_symbol: str | None
    passes: bool
    value_description: LangDictData
    exam_id: str | int
    exam_session_number: int
    counts_into_average: bool
    comment: str | None
    private_comment: str | None
    grade_type_id: str
    date_modified: str | None
    date_acquisition: str | None
    modification_author: str | int | None


class ExamReportSession(TypedDict, total=False):
    number: int
    examrep_id: str | int
    status: str
    description: LangDictData
    deadline: str | None
    is_editable: bool
    issuer_grades: ExamReportIssuerGrade | list[ExamReportIssuerGrade]


class ExamReport(TypedDict, total=False):
    id: str | int
    description: LangDictData
    type_id: str
    type_description: LangDictData
    counts_into_average: bool
    term_id: str
    is_editable: bool
    course_unit: ExamReportCourseUnit | None
    course: ExamReportCourse
    sessions: list[ExamReportSession]
    grades_distribution: list[ExamReportGradeDistributionItem]


UserExamReportsByTerm: TypeAlias = dict[str, dict[str, list[ExamReport]]]
LegacyUserExamReportsByTerm: TypeAlias = dict[
    str, dict[str, dict[str, list[ExamReport]]]
]
LegacyCourseEditionExamReport: TypeAlias = dict[
    str, ExamReport | list[ExamReport] | dict[str, list[ExamReport]] | None
]


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
        return await self.connection.post(
            "services/examrep2/class_group",
            examrep_id=examrep_id,
            course_unit_id=course_unit_id,
            group_number=group_number,
            fields=_join_fields(fields),
        )

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
        return await self.connection.post(
            "services/examrep2/examinee",
            user_id=user_id,
            fields=_join_fields(fields),
        )

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
        return await self.connection.post(
            "services/examrep2/examrep",
            examrep_id=examrep_id,
            fields=_join_fields(fields),
        )

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
        return await self.connection.post(
            "services/examrep2/examrep_session",
            examrep_id=examrep_id,
            examrep_session_number=examrep_session_number,
            fields=_join_fields(fields),
        )

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
        return await self.connection.post(
            "services/examrep2/examrep_session_access",
            examrep_id=examrep_id,
            examrep_session_number=examrep_session_number,
            type=access_type,
            fields=_join_fields(fields),
        )

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
        return await self.connection.post(
            "services/examrep2/examrep_type",
            examrep_type_id=examrep_type_id,
            fields=_join_fields(fields),
        )

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
        return await self.connection.post(
            "services/examrep2/grade_type",
            grade_type_id=grade_type_id,
            fields=_join_fields(fields),
        )

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
        return await self.connection.post(
            "services/examrep2/grade_value",
            grade_type_id=grade_type_id,
            order_key=order_key,
            fields=_join_fields(fields),
        )

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
        return await self.connection.post(
            "services/examrep2/grader",
            only_writable=_bool_param(only_writable),
            active_terms_only=_bool_param(active_terms_only),
            fields=_join_fields(fields),
        )

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
        return await self.connection.post(
            "services/examrep2/student_grade",
            examrep_id=examrep_id,
            examrep_session_number=examrep_session_number,
            student_id=student_id,
            fields=_join_fields(fields),
        )

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
        return await self.connection.post(
            "services/examrep2/student_grades",
            examrep_id=examrep_id,
            student_id=student_id,
            fields=_join_fields(fields),
        )

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
        return await self.connection.post(
            "services/examrep2/user_grade",
            examrep_id=examrep_id,
            examrep_session_number=examrep_session_number,
            fields=_join_fields(fields),
        )

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
        return await self.connection.post(
            "services/examrep/course_edition",
            course_id=course_id,
            term_id=term_id,
            fields=_join_fields(fields),
        )

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
        return await self.connection.post(
            "services/examrep/course_edition2",
            course_id=course_id,
            term_id=term_id,
            fields=_join_fields(fields),
        )

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
        return await self.connection.post(
            "services/examrep/exam",
            id=exam_id,
            fields=_join_fields(fields),
        )

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
        return await self.connection.post(
            "services/examrep/exam_session",
            exam_id=exam_id,
            number=number,
            fields=_join_fields(fields),
        )

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
        return await self.connection.post(
            "services/examrep/user",
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

        This wraps ``services/examrep/user2``.

        :param term_ids: Academic term IDs. If omitted, the API default is used.
        :param fields: Selector of result fields you are interested in.
        :return: A dictionary mapping term IDs to course IDs to exam report lists.
        """
        return await self.connection.post(
            "services/examrep/user2",
            term_ids=_join_fields(term_ids),
            fields=_join_fields(fields),
        )
