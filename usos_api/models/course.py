from typing import TYPE_CHECKING, List

from pydantic import BaseModel

from .group import Group
from .term import Term

if TYPE_CHECKING:
    from .user import User

from .grade import Grade
from .lang_dict import LangDict


class CourseAttribute(BaseModel):
    """
    Class representing a course attribute.
    """

    name: LangDict | None = None
    values: List[LangDict] | None = None


class Course(BaseModel):
    """
    Class representing a course.
    """

    id: str | None = None
    name: LangDict | None = None
    homepage_url: str | None = None
    profile_url: str | None = None
    is_currently_conducted: bool | None = None
    terms: List[Term] | None = None
    fac_id: str | None = None
    lang_id: str | None = None
    ects_credits_simplified: float | None = None
    description: LangDict | None = None
    bibliography: LangDict | None = None
    learning_outcomes: LangDict | None = None
    assessment_criteria: LangDict | None = None
    practical_placement: LangDict | None = None
    attributes: List[CourseAttribute] | None = None
    attributes2: List[CourseAttribute] | None = None


class CourseEdition(BaseModel):
    """
    Class representing a course edition.
    """

    course_id: str | None = None
    course_name: LangDict | None = None
    term_id: str | None = None
    homepage_url: str | None = None
    profile_url: str | None = None
    coordinators: List["User"] | None = None
    lecturers: List["User"] | None = None
    passing_status: str | None = None
    user_groups: List[Group] | None = None
    description: LangDict | None = None
    bibliography: LangDict | None = None
    notes: LangDict | None = None
    course_units_ids: List[str] | None = None
    participants: List["User"] | None = None
    grades: List[Grade] | None = None
    attributes: List[CourseAttribute] | None = None


class CourseEditionConducted(BaseModel):
    """
    Class representing a conducted course edition.
    """

    id: str | None = None
    course: Course | None = None
    term: Term | None = None
