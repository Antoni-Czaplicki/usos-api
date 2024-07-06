from typing import TYPE_CHECKING, List

from pydantic import BaseModel

from .lang_dict import LangDict

if TYPE_CHECKING:
    from .user import User


class Group(BaseModel):
    course_unit_id: str | None = None
    group_number: int | None = None
    class_type: LangDict | None = None
    class_type_id: str | None = None
    group_url: str | None = None
    course_id: str | None = None
    course_name: LangDict | None = None
    course_homepage_url: str | None = None
    course_profile_url: str | None = None
    course_is_currently_conducted: bool | None = None
    course_fac_id: str | None = None
    course_lang_id: str | None = None
    term_id: str | None = None
    lecturers: List["User"] | None = None
    participants: List["User"] | None = None
    group_description: LangDict | None = None
    group_literature: LangDict | None = None
    course_learning_outcomes: LangDict | None = None
    course_description: LangDict | None = None
    course_bibliography: LangDict | None = None
    course_assessment_criteria: LangDict | None = None
    course_practical_placement: LangDict | None = None
