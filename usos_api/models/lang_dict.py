from pydantic import BaseModel


class LangDict(BaseModel):
    """
    Class representing a dictionary with translations.
    """

    pl: str | None = None
    en: str | None = None
