from datetime import date

from pydantic import BaseModel


class Programme(BaseModel):
    """
    Class representing a study programme.
    """

    id: str | None = None
    name: dict | None = None
    description: dict | None = None
    faculty: dict | None = None
    all_faculties: list | None = None
    mode_of_studies: dict | None = None
    level_of_studies: dict | None = None
    duration: dict | None = None
    professional_status: dict | None = None
    level: str | None = None


class StudentProgramme(BaseModel):
    """
    Class representing a student programme a user is enrolled in.
    """

    id: str | None = None
    user: dict | None = None
    programme: Programme | None = None
    status: str | None = None
    admission_date: date | None = None
    stages: list = []
    is_primary: bool | None = None
