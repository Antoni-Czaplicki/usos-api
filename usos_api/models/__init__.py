from .api_documentation import (
    APIMethodIndexItem,
    APIMethodInfo,
    APIModuleInfo,
    Argument,
    AuthOptions,
    DeprecatedInfo,
    ResultField,
    ScopeInfo,
)
from .consumer import Consumer
from .course import (
    Course,
    CourseAttribute,
    CourseEdition,
    CourseEditionConducted,
    CourseUnit,
)
from .grade import Grade
from .group import Group
from .lang_dict import LangDict
from .programme import Programme, StudentProgramme
from .term import Term
from .user import (
    EmailAccess,
    EmploymentFunction,
    EmploymentPosition,
    ExternalIds,
    Position,
    PostalAddress,
    PreviousName,
    Sex,
    StaffStatus,
    StudentStatus,
    Title,
    User,
)

# Fix for circular imports
CourseAttribute.model_rebuild()
CourseEdition.model_rebuild()
Grade.model_rebuild()
Group.model_rebuild()

__all__ = [
    "User",
    "PreviousName",
    "Title",
    "Position",
    "EmploymentPosition",
    "EmailAccess",
    "StaffStatus",
    "StudentStatus",
    "EmploymentFunction",
    "PostalAddress",
    "ExternalIds",
    "StudentProgramme",
    "Programme",
    "Sex",
    "LangDict",
    "CourseAttribute",
    "CourseEdition",
    "Group",
    "Grade",
    "Course",
    "CourseEditionConducted",
    "Term",
    "Consumer",
    "CourseUnit",
    "AuthOptions",
    "Argument",
    "ResultField",
    "DeprecatedInfo",
    "APIMethodInfo",
    "APIMethodIndexItem",
    "APIModuleInfo",
    "ScopeInfo",
]
