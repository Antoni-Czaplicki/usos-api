from typing import TYPE_CHECKING, Any, Dict, Optional

from pydantic import BaseModel

if TYPE_CHECKING:
    from .user import User

from .lang_dict import LangDict


class Grade(BaseModel):
    value_symbol: str | None = None
    passes: bool | None = None
    value_description: LangDict | None = None
    exam_id: str | None = None
    exam_session_number: str | None = None
    counts_into_average: bool | None = None
    comment: str | None = None
    private_comment: str | None = None
    grade_type_id: str | None = None
    date_modified: str | None = None
    date_acquisition: str | None = None
    modification_author: str | None = None
    course_edition: Dict[str, Any] | None = None
    unit: Dict[str, Any] | None = None
    exam_report: Dict[str, Any] | None = None
    user: Optional["User"] = None
