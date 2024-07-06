from datetime import date
from enum import Enum

from pydantic import BaseModel

from .course import CourseEditionConducted
from .lang_dict import LangDict
from .programme import StudentProgramme


class PreviousName(BaseModel):
    """
    Class representing a user's previous name along with the date until which it was used.
    """

    first_name: str | None = None
    last_name: str | None = None
    until: date | None = None


class Title(BaseModel):
    """
    Class representing a user's academic titles.
    """

    before: str | None = None
    after: str | None = None


class EmailAccess(Enum):
    """
    Enum representing the access level to a user's email.
    """

    NO_EMAIL = "no_email"
    NO_ACCESS = "no_access"
    REQUIRE_CAPTCHA = "require_captcha"
    PLAINTEXT = "plaintext"


class EmploymentFunction(BaseModel):
    """
    Class representing an employment function of a user.
    """

    function: LangDict | None = None
    faculty: dict | None = None
    is_official: bool | None = None


class Position(BaseModel):
    """
    Class representing an employment position.
    """

    id: str | None = None
    name: LangDict | None = None
    employment_group: dict | None = None


class EmploymentPosition(BaseModel):
    """
    Class representing an employment position of a user.
    """

    position: Position | None = None
    faculty: LangDict | None = None


class PostalAddress(BaseModel):
    """
    Class representing a postal address of a user.
    """

    type: str | None = None
    type_name: str | None = None
    address: str | None = None


class ExternalIds(BaseModel):
    """
    Class representing external IDs of a user.
    """

    orcid: str | None = None
    pbn_id: str | None = None


class StaffStatus(Enum):
    """
    Enum representing the staff status of a user.
    """

    NOT_STAFF = 0
    NON_ACADEMIC_STAFF = 1
    ACADEMIC_TEACHER = 2


class StudentStatus(Enum):
    """
    Enum representing the student status of a user.
    """

    NOT_STUDENT = 0
    INACTIVE_STUDENT = 1
    ACTIVE_STUDENT = 2


class Sex(Enum):
    """
    Enum representing the gender of a user.
    """

    MALE = "M"
    FEMALE = "F"


class User(BaseModel):
    """
    Class representing a User with various attributes.
    """

    id: int | None = None
    first_name: str | None = None
    middle_names: str | None = None
    last_name: str | None = None
    previous_names: list[PreviousName] = []
    sex: Sex | None = None
    titles: Title | None = None
    student_status: StudentStatus | None = None
    staff_status: StaffStatus | None = None
    email_access: EmailAccess | None = None
    email: str | None = None
    email_url: str | None = None
    has_email: bool | None = None
    homepage_url: str | None = None
    profile_url: str | None = None
    phone_numbers: list[str] = []
    mobile_numbers: list[str] = []
    office_hours: LangDict | None = None
    interests: LangDict | None = None
    has_photo: bool | None = None
    photo_urls: dict[str, str] = {}
    student_number: str | None = None
    pesel: str | None = None
    birth_date: date | None = None
    revenue_office_id: str | None = None
    citizenship: str | None = None
    room: str | None = None
    student_programmes: list[StudentProgramme] = []
    employment_functions: list[EmploymentFunction] = []
    employment_positions: list[EmploymentPosition] = []
    course_editions_conducted: list[CourseEditionConducted] = []
    postal_addresses: list[PostalAddress] = []
    alt_email: str | None = None
    can_i_debug: bool = False
    external_ids: ExternalIds | None = None
    phd_student_status: int | None = None
    library_card_id: str | None = None
