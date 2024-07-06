from datetime import date

from pydantic import BaseModel

from .lang_dict import LangDict


class Term(BaseModel):
    id: str | None = None
    name: LangDict | None = None
    start_date: date | None = None
    end_date: date | None = None
    finish_date: date | None = None
    is_active: bool | None = None
