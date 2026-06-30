from datetime import datetime
from typing import Any, Mapping, TypeAlias

from pydantic import BaseModel, ConfigDict, field_validator

from .lang_dict import LangDict
from .usos_bool import USOSBool
from .user import User


class ExternalObject(BaseModel):
    model_config = ConfigDict(extra="allow")

    id: str | int | None = None
    name: LangDict | str | None = None


class GradeValue(BaseModel):
    grade_type: ExternalObject | None = None
    order_key: str | int | None = None
    symbol: str | None = None
    passes: USOSBool | None = None
    decimal_value: float | None = None
    name: LangDict | None = None


class GradeType(BaseModel):
    id: str | None = None
    name: LangDict | None = None
    values: list[GradeValue] | None = None


class ExamReportType(BaseModel):
    id: str | None = None
    name: LangDict | None = None
    grade_type: GradeType | None = None


class ExamReport2StudentGrade(BaseModel):
    grade_value: GradeValue | None = None
    comment: str | None = None
    private_comment: str | None = None
    user: ExternalObject | None = None
    grader: ExternalObject | None = None
    last_updated: datetime | None = None
    is_editable: USOSBool | None = None
    resignation: USOSBool | None = None
    inactive_links: USOSBool | None = None
    why_cannot_edit: str | None = None
    date_acquisition: datetime | None = None
    examrep_session: ExternalObject | None = None


class ExamReport2UserGrade(BaseModel):
    grade_value: GradeValue | None = None
    comment: str | None = None
    user: ExternalObject | None = None
    grader: ExternalObject | None = None
    last_updated: datetime | None = None


def grades_by_user(value: Any) -> dict[str, ExamReport2StudentGrade] | None:
    if value is None or isinstance(value, dict):
        return value
    if isinstance(value, list):
        parsed_grades: dict[str, ExamReport2StudentGrade] = {}
        for index, raw_grade in enumerate(value):
            grade = ExamReport2StudentGrade.model_validate(raw_grade)
            user_id = grade.user.id if grade.user is not None else None
            parsed_grades[str(user_id if user_id is not None else index)] = grade
        return parsed_grades
    raise ValueError("Expected grade dictionary, grade list or None.")


class ExamReport2Session(BaseModel):
    examrep_id: str | int | None = None
    number: int | None = None
    status: str | None = None
    description: LangDict | None = None
    deadline: datetime | None = None
    is_open: USOSBool | None = None
    is_acquisition_date_required: USOSBool | None = None
    all_grades: dict[str, ExamReport2StudentGrade] | None = None
    issuer_grade: ExamReport2UserGrade | None = None
    read_access: list[ExternalObject] | None = None
    write_access: list[ExternalObject] | None = None

    @field_validator("all_grades", mode="before")
    @classmethod
    def _parse_all_grades(
        cls, value: Any
    ) -> dict[str, ExamReport2StudentGrade] | None:
        return grades_by_user(value)


class ExamReport2(BaseModel):
    id: str | int | None = None
    description: LangDict | None = None
    counts_into_average: USOSBool | None = None
    grade_type: GradeType | None = None
    is_general_report: USOSBool | None = None
    sessions: list[ExamReport2Session] | None = None
    edit_access: list[ExternalObject] | None = None
    course_edition: ExternalObject | None = None
    course_unit: ExternalObject | None = None
    active_sessions: list[ExamReport2Session] | None = None


class ExamReportSessionAccess(BaseModel):
    cause: str | None = None
    groups: list[ExternalObject] | None = None
    exam_groups: list[ExternalObject] | None = None
    unassigned: USOSBool | None = None


class ExamReport2ClassGroup(BaseModel):
    class_group: ExternalObject | None = None
    grades: dict[str, ExamReport2StudentGrade] | None = None

    @field_validator("grades", mode="before")
    @classmethod
    def _parse_grades(cls, value: Any) -> dict[str, ExamReport2StudentGrade] | None:
        return grades_by_user(value)


class ExamReportCourse(BaseModel):
    id: str | None = None
    name: LangDict | None = None


class ExamReportCourseUnit(BaseModel):
    id: str | None = None
    course_id: str | None = None
    course_name: LangDict | None = None
    classtype_id: str | None = None
    term_id: str | None = None


class ExamReportGradeDistributionItem(BaseModel):
    grade_symbol: str | None = None
    percentage: float | None = None


class ExamReportIssuerGrade(BaseModel):
    value_symbol: str | None = None
    passes: USOSBool | None = None
    value_description: LangDict | None = None
    exam_id: str | int | None = None
    exam_session_number: int | None = None
    counts_into_average: USOSBool | None = None
    comment: str | None = None
    private_comment: str | None = None
    grade_type_id: str | None = None
    date_modified: datetime | None = None
    date_acquisition: datetime | None = None
    modification_author: User | None = None

    @field_validator("modification_author", mode="before")
    @classmethod
    def _parse_modification_author(cls, value: Any) -> User | None:
        if value is None or isinstance(value, User):
            return value
        if isinstance(value, dict):
            return User.model_validate(value)
        if isinstance(value, str | int):
            return User(id=value)
        raise ValueError("Expected user object, user id or None.")


class ExamReportSession(BaseModel):
    number: int | None = None
    examrep_id: str | int | None = None
    status: str | None = None
    description: LangDict | None = None
    deadline: datetime | None = None
    is_editable: USOSBool | None = None
    issuer_grades: list[ExamReportIssuerGrade] | None = None

    @field_validator("issuer_grades", mode="before")
    @classmethod
    def _parse_issuer_grades(cls, value: Any) -> list[Any] | None:
        if value is None or isinstance(value, list):
            return value
        if isinstance(value, dict):
            return [value]
        raise ValueError("Expected issuer grade object, issuer grade list or None.")


class ExamReport(BaseModel):
    id: str | int | None = None
    description: LangDict | None = None
    type_id: str | None = None
    type_description: LangDict | None = None
    counts_into_average: USOSBool | None = None
    term_id: str | None = None
    is_editable: USOSBool | None = None
    course_unit: ExamReportCourseUnit | None = None
    course: ExamReportCourse | None = None
    sessions: list[ExamReportSession] | None = None
    grades_distribution: list[ExamReportGradeDistributionItem] | None = None


UserExamReportsByTerm: TypeAlias = dict[str, dict[str, list[ExamReport]]]
RawUserExamReportsByTerm: TypeAlias = dict[str, dict[str, list[dict[str, Any]]]]
LegacyUserExamReportsByTerm: TypeAlias = dict[
    str, dict[str, dict[str, list[ExamReport]]]
]
LegacyCourseEditionExamReport: TypeAlias = dict[
    str, ExamReport | list[ExamReport] | dict[str, list[ExamReport]] | None
]


def parse_user_exam_reports(
    reports_by_term: Mapping[str, Mapping[str, list[Mapping[str, Any]]]],
) -> UserExamReportsByTerm:
    return {
        term_id: {
            course_id: [ExamReport.model_validate(report) for report in reports]
            for course_id, reports in courses.items()
        }
        for term_id, courses in reports_by_term.items()
    }


def parse_legacy_user_exam_reports(
    reports_by_term: Mapping[
        str, Mapping[str, Mapping[str, list[Mapping[str, Any]]]]
    ],
) -> LegacyUserExamReportsByTerm:
    return {
        term_id: {
            course_id: {
                group_id: [ExamReport.model_validate(report) for report in reports]
                for group_id, reports in groups.items()
            }
            for course_id, groups in courses.items()
        }
        for term_id, courses in reports_by_term.items()
    }


def parse_legacy_course_edition_exam_report(
    exam_report_data: Mapping[str, Any],
) -> LegacyCourseEditionExamReport:
    return {
        key: _parse_legacy_course_edition_value(value)
        for key, value in exam_report_data.items()
    }


def _parse_legacy_course_edition_value(
    value: Any,
) -> ExamReport | list[ExamReport] | dict[str, list[ExamReport]] | None:
    if value is None:
        return None
    if isinstance(value, list):
        return [ExamReport.model_validate(report) for report in value]
    if isinstance(value, dict):
        if all(isinstance(reports, list) for reports in value.values()):
            return {
                group_id: [ExamReport.model_validate(report) for report in reports]
                for group_id, reports in value.items()
            }
        return ExamReport.model_validate(value)
    raise ValueError("Expected exam report object, exam report list, mapping or None.")
