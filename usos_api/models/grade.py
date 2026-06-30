from datetime import datetime
from typing import TYPE_CHECKING, Any, Optional

from pydantic import BaseModel, field_validator

from . import CourseEdition
from .course import CourseUnit
from .usos_bool import USOSBool

if TYPE_CHECKING:
    from .user import User

from .lang_dict import LangDict


class Grade(BaseModel):
    value: float | None = None
    value_symbol: str | None = None
    passes: USOSBool | None = None
    value_description: LangDict | None = None
    exam_id: int | None = None
    exam_session_number: int | None = None
    counts_into_average: USOSBool | None = None
    comment: str | None = None
    private_comment: str | None = None
    grade_type_id: str | None = None
    date_modified: datetime | None = None
    date_acquisition: datetime | None = None
    modification_author: Optional["User"] = None
    course_edition: CourseEdition | None = None
    unit: CourseUnit | None = None
    exam_report: dict[str, Any] | None = None
    user: Optional["User"] = None
    weight: float | None = (
        None  # Not returned by USOS API but is here to make it easier to work with grades
    )

    def __init__(self, **data: Any):
        super().__init__(**data)
        if self.value_symbol:
            try:
                self.value = float(self.value_symbol.replace(",", "."))
            except ValueError:
                pass  # Invalid value, ignore it

    @field_validator("modification_author", mode="before")
    @classmethod
    def _parse_modification_author(cls, value: Any) -> Optional["User"]:
        from .user import User

        if value is None or isinstance(value, User):
            return value
        if isinstance(value, dict):
            return User.model_validate(value)
        if isinstance(value, str | int):
            return User(id=value)
        raise ValueError("Expected user object, user id or None.")
