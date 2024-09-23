from .api_documentation import APIDocumentationService
from .api_server import APIServerService
from .courses import CourseService
from .grades import GradeService
from .groups import GroupService
from .registrations import RegistrationService
from .terms import TermService
from .users import UserService

__all__ = [
    "APIDocumentationService",
    "APIServerService",
    "CourseService",
    "GradeService",
    "GroupService",
    "TermService",
    "UserService",
    "RegistrationService",
]
