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

    # def __init__(self, first_name: str, last_name: str, until: date):
    #     """
    #     Initialize a new PreviousName instance.
    #
    #     :param first_name: The first name of the user.
    #     :param last_name: The last name of the user.
    #     :param until: The date until which the name was used.
    #     """
    #     self.first_name = first_name
    #     self.last_name = last_name
    #     self.until = until

    def __repr__(self):
        """
        Return a string representation of the PreviousName.
        """
        return f"<PreviousName {self.first_name} {self.last_name} ({self.until})>"


class Title(BaseModel):
    """
    Class representing a user's academic titles.
    """

    before: str | None = None
    after: str | None = None

    # def __init__(self, before: Optional[str], after: Optional[str]):
    #     """
    #     Initialize a new Title instance.
    #
    #     :param before: The title to be displayed before the user's name.
    #     :param after: The title to be displayed after the user's name.
    #     """
    #     self.before = before
    #     self.after = after

    def __repr__(self):
        """
        Return a string representation of the Title.
        """
        return f"<Title {self.before} {self.after}>"


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

    # def __init__(self, function: dict, faculty: dict, is_official: bool):
    #     """
    #     Initialize a new EmploymentFunction instance.
    #
    #     :param function: The function of the employment.
    #     :param faculty: The faculty related to the user and this function.
    #     :param is_official: True if the function is "official".
    #     """
    #     self.function = function
    #     self.faculty = faculty
    #     self.is_official = is_official

    def __repr__(self):
        """
        Return a string representation of the EmploymentFunction.
        """
        return f"<EmploymentFunction {self.function}>"


class Position(BaseModel):
    """
    Class representing an employment position.
    """

    id: str | None = None
    name: LangDict | None = None
    employment_group: dict | None = None

    # def __init__(self, id: str, name: str, employment_group: dict):
    #     """
    #     Initialize a new Position instance.
    #
    #     :param id: The ID of the position.
    #     :param name: The name of the position.
    #     :param employment_group: The employment group that position belongs to.
    #     """
    #     self.id = id
    #     self.name = name
    #     self.employment_group = employment_group

    def __repr__(self):
        """
        Return a string representation of the Position.
        """
        return f"<Position {self.name}>"


class EmploymentPosition(BaseModel):
    """
    Class representing an employment position of a user.
    """

    position: Position | None = None
    faculty: LangDict | None = None

    # def __init__(self, position: Position, faculty: dict):
    #     """
    #     Initialize a new EmploymentPosition instance.
    #
    #     :param position: The position of the employment.
    #     :param faculty: The faculty related to the user and this position.
    #     """
    #     self.position = position
    #     self.faculty = faculty

    def __repr__(self):
        """
        Return a string representation of the EmploymentPosition.
        """
        return f"<EmploymentPosition {self.position}>"


class PostalAddress(BaseModel):
    """
    Class representing a postal address of a user.
    """

    type: str | None = None
    type_name: str | None = None
    address: str | None = None

    # def __init__(self, type: str, type_name: str, address: str):
    #     """
    #     Initialize a new PostalAddress instance.
    #
    #     :param type: The type of the postal address.
    #     :param type_name: The name of the type of the postal address.
    #     :param address: The postal address.
    #     """
    #     self.type = type
    #     self.type_name = type_name
    #     self.address = address

    def __repr__(self):
        """
        Return a string representation of the PostalAddress.
        """
        return f"<PostalAddress {self.address}>"


class ExternalIds(BaseModel):
    """
    Class representing external IDs of a user.
    """

    orcid: str | None = None
    pbn_id: str | None = None

    # def __init__(self, orcid: Optional[str], pbn_id: Optional[str]):
    #     """
    #     Initialize a new ExternalIds instance.
    #
    #     :param orcid: The ORCID identifier of the user.
    #     :param pbn_id: The PBN ID of the user.
    #     """
    #     self.orcid = orcid
    #     self.pbn_id = pbn_id

    def __repr__(self):
        """
        Return a string representation of the ExternalIds.
        """
        return f"<ExternalIds {self.orcid} {self.pbn_id}>"


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

    # def __init__(
    #     self,
    #     id: int | None = None,
    #     first_name: str | None = None,
    #     middle_names: str | None = None,
    #     last_name: str | None = None,
    #     previous_names: list[PreviousName] | None = None,
    #     sex: Sex | None = None,
    #     titles: Title | None = None,
    #     student_status: StudentStatus | None = None,
    #     staff_status: StaffStatus | None = None,
    #     email_access: EmailAccess | None = None,
    #     email: str | None = None,
    #     email_url: str | None = None,
    #     has_email: bool = None,
    #     homepage_url: str | None = None,
    #     profile_url: str | None = None,
    #     phone_numbers: list[str] | None = None,
    #     mobile_numbers: list[str] | None = None,
    #     office_hours: str | None = None,
    #     interests: str | None = None,
    #     has_photo: bool = None,
    #     photo_urls: dict[str, str] | None = None,
    #     student_number: str | None = None,
    #     pesel: str | None = None,
    #     birth_date: date | None = None,
    #     revenue_office_id: str | None = None,
    #     citizenship: str | None = None,
    #     room: str | None = None,
    #     student_programmes: list[StudentProgramme] | None = None,
    #     employment_functions: list[EmploymentFunction] | None = None,
    #     employment_positions: list[EmploymentPosition] | None = None,
    #     course_editions_conducted: list[str] | None = None,
    #     postal_addresses: list[PostalAddress] | None = None,
    #     alt_email: str | None = None,
    #     can_i_debug: bool = None,
    #     external_ids: ExternalIds | None = None,
    #     phd_student_status: int | None = None,
    #     library_card_id: str | None = None,
    #     **kwargs,
    # ):
    #     """
    #     Initialize a new User instance.
    #
    #     :param id: The USOS ID of the user.
    #     :param first_name: The first name of the user.
    #     :param middle_names: The middle name(s) of the user.
    #     :param last_name: The last name of the user.
    #     :param previous_names: A list of the user's previous names.
    #     :param sex: The sex of the user.
    #     :param titles: The academic titles of the user.
    #     :param student_status: The student status of the user.
    #     :param staff_status: The staff status of the user.
    #     :param email_access: The access level to the user's email.
    #     :param email: The email of the user.
    #     :param email_url: The URL of the user's email.
    #     :param has_email: A boolean indicating whether the user has an email.
    #     :param homepage_url: The URL of the user's homepage.
    #     :param profile_url: The URL of the user's profile.
    #     :param phone_numbers: A list of the user's phone numbers.
    #     :param mobile_numbers: A list of the user's mobile numbers.
    #     :param office_hours: The office hours of the user.
    #     :param interests: The interests of the user.
    #     :param has_photo: A boolean indicating whether the user has a photo.
    #     :param photo_urls: A dictionary of the user's photo URLs. Each field contains an URL pointing to an image scaled to different dimensions.
    #     :param student_number: The student number of the user.
    #     :param pesel: The PESEL number of the user.
    #     :param birth_date: The birth date of the user.
    #     :param revenue_office_id: The ID of the user's revenue office.
    #     :param citizenship: The citizenship of the user.
    #     :param room: The room of the user.
    #     :param student_programmes: A list of the student programmes the user is enrolled in.
    #     :param employment_functions: A list of the user's employment functions.
    #     :param employment_positions: A list of the user's employment positions.
    #     :param course_editions_conducted: A list of the course editions conducted by the user.
    #     :param postal_addresses: A list of the user's postal addresses.
    #     :param alt_email: The alternative email of the user.
    #     :param can_i_debug: A boolean indicating whether the user can debug.
    #     :param external_ids: The external IDs of the user.
    #     :param phd_student_status: The PhD student status of the user.
    #     :param library_card_id: The library card ID of the user.
    #     """
    #     self.id = id
    #     self.first_name = first_name
    #     self.middle_names = middle_names
    #     self.last_name = last_name
    #     self.previous_names = previous_names
    #     self.sex = sex
    #     self.titles = titles
    #     self.student_status = student_status
    #     self.staff_status = staff_status
    #     self.email_access = email_access
    #     self.email = email
    #     self.email_url = email_url
    #     self.has_email = has_email
    #     self.homepage_url = homepage_url
    #     self.profile_url = profile_url
    #     self.phone_numbers = phone_numbers
    #     self.mobile_numbers = mobile_numbers
    #     self.office_hours = office_hours
    #     self.interests = interests
    #     self.has_photo = has_photo
    #     self.photo_urls = photo_urls
    #     self.student_number = student_number
    #     self.pesel = pesel
    #     self.birth_date = birth_date
    #     self.revenue_office_id = revenue_office_id
    #     self.citizenship = citizenship
    #     self.room = room
    #     self.student_programmes = student_programmes
    #     self.employment_functions = employment_functions
    #     self.employment_positions = employment_positions
    #     self.course_editions_conducted = course_editions_conducted
    #     self.postal_addresses = postal_addresses
    #     self.alt_email = alt_email
    #     self.can_i_debug = can_i_debug
    #     self.external_ids = external_ids
    #     self.phd_student_status = phd_student_status
    #     self.library_card_id = library_card_id

    def __repr__(self):
        """
        Return a string representation of the User.
        """
        return f"<User {self.first_name} {self.last_name}>"
