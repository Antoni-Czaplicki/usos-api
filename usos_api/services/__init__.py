from .api_documentation import APIDocumentationService
from .api_server import APIServerService
from .courses import CourseService
from .exam_reports import ExamReportService
from .grades import GradeService
from .groups import GroupService
from .programmes import ProgrammeService
from .registrations import RegistrationService
from .terms import TermService
from .users import UserService

__all__ = [
    "APIDocumentationService",
    "APIServerService",
    "CourseService",
    "ExamReportService",
    "GradeService",
    "GroupService",
    "ProgrammeService",
    "TermService",
    "UserService",
    "RegistrationService",
]
