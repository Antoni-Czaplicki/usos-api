from datetime import date

from pydantic import BaseModel

from .lang_dict import LangDict


class Faculty(BaseModel):
    """
    Class representing a faculty.
    """

    id: str | None = None
    name: LangDict | None = None
    profile_url: str | None = None
    homepage_url: str | None = None
    postal_address: str | None = None
    email: str | None = None
    is_public: bool | None = None


class Programme(BaseModel):
    """
    Class representing a study programme.
    """

    id: str | None = None
    name: LangDict | None = None
    description: LangDict | None = None
    faculty: Faculty | None = None
    all_faculties: list[Faculty] | None = None
    mode_of_studies: LangDict | None = None
    level_of_studies: LangDict | None = None
    duration: LangDict | None = None
    professional_status: LangDict | None = None
    level: str | None = None


class ProgrammeStage(BaseModel):
    """
    Class representing a stage of a programme a student is enrolled in.
    """

    id: str | None = None
    name: LangDict | None = None
    code: str | None = None
    description: LangDict | None = None


class StudentProgramme(BaseModel):
    """
    Class representing a student programme a user is enrolled in.
    """

    id: str | None = None
    user: dict | None = None
    programme: Programme | None = None
    status: str | None = None
    admission_date: date | None = None
    stages: list[ProgrammeStage] | None = []
    is_primary: bool | None = None
