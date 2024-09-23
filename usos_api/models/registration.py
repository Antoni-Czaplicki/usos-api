from datetime import datetime

from pydantic import BaseModel

from usos_api.models import LangDict
from usos_api.models.course import Course
from usos_api.models.programme import Programme
from usos_api.models.term import Term


class Registration(BaseModel):
    id: str | None = None
    description: LangDict | None = None
    message: LangDict | None = None
    type: str | None = None
    status: str | None = None
    faculty: str | None = None
    is_linkage_required: bool | None = None
    www_instance: str | None = None

    rounds: list["RegistrationRound"] | None = None
    related_courses: list["RegistrationCourse"] | None = None


class RegistrationRound(BaseModel):
    id: str | None = None
    name: LangDict | None = None
    status: str | None = None
    registration_mode: str | None = None
    start_date: datetime | None = None
    end_date: datetime | None = None
    selection_limit: int | None = None
    is_dedicated: bool | None = None
    is_overflow_allowed: bool | None = None
    is_exchange: bool | None = None
    is_only_entitled: bool | None = None
    rank_code: str | None = None
    ranking: dict | None = None
    is_processed: bool | None = None
    registration: Registration | None = None


class RegistrationCourse(BaseModel):
    registration_id: str | None = None
    course_id: str | None = None
    term_id: str | None = None
    status: str | None = None
    limits: dict | None = None
    www_instance: str | None = None


class Stage(BaseModel):
    id: str | None = None
    name: LangDict | None = None


class Link(BaseModel):
    programme: Programme | None = None
    stage: Stage | None = None


class CoursesCart(BaseModel):
    links: list[Link] | None = None
    course: Course | None = None
    term: Term | None = None
    user_registration_status: str | None = None
    is_registration_valid: bool | None = None
    choice_number: int | None = None
    limits: int | None = None
    is_linkage_required: bool | None = None
    registrations_count: int | None = None
    registration_status: str | None = None
    active_registration_round_id: str | None = None
