from pydantic import BaseModel

from .lang_dict import LangDict


class Term(BaseModel):
    id: str | None = None
    name: LangDict | None = None
    start_date: str | None = None
    end_date: str | None = None
    finish_date: str | None = None
    is_active: bool | None = None
