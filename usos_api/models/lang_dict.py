from pydantic import BaseModel


class LangDict(BaseModel):
    """
    Class representing a dictionary with translations.
    """

    pl: str | None = None
    en: str | None = None

    def __repr__(self):
        """
        Return a string representation of the LangDict.
        """
        return f"LangDict(pl={self.pl}, en={self.en})"
