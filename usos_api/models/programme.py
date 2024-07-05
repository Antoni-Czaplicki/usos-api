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

    # def __init__(
    #     self,
    #     id: str,
    #     name: dict,
    #     description: dict,
    #     faculty: dict,
    #     all_faculties: list,
    #     mode_of_studies: dict,
    #     level_of_studies: dict,
    #     duration: dict,
    #     professional_status: dict,
    #     level: str,
    # ):
    #     """
    #     Initialize a new Programme instance.
    #
    #     :param id: The ID of the programme.
    #     :param name: The name of the programme.
    #     :param description: The description of the programme.
    #     :param faculty: The faculty which administers this study programme.
    #     :param all_faculties: List of faculties related to programme.
    #     :param mode_of_studies: The studies-mode provided by the programme.
    #     :param level_of_studies: The level of the programme.
    #     :param duration: The duration of the programme.
    #     :param professional_status: The qualifications that will be acquired after graduation from this programme.
    #     :param level: The level of the programme.
    #     """
    #     self.id = id
    #     self.name = name
    #     self.description = description
    #     self.faculty = faculty
    #     self.all_faculties = all_faculties
    #     self.mode_of_studies = mode_of_studies
    #     self.level_of_studies = level_of_studies
    #     self.duration = duration
    #     self.professional_status = professional_status
    #     self.level = level

    def __repr__(self):
        """
        Return a string representation of the Programme.
        """
        return f"<Programme {self.name}>"


class StudentProgramme(BaseModel):
    """
    Class representing a student programme a user is enrolled in.
    """

    id: str | None = None
    user: dict | None = None
    programme: Programme | None = None
    status: str | None = None
    admission_date: str | None = None
    stages: list = []
    is_primary: bool | None = None

    # def __init__(
    #     self,
    #     id: str,
    #     user: dict,
    #     programme: dict,
    #     status: str,
    #     admission_date: str,
    #     stages: list,
    #     is_primary: bool,
    # ):
    #     """
    #     Initialize a new StudentProgramme instance.
    #
    #     :param id: The ID of the student programme.
    #     :param user: The user of this student_programme.
    #     :param programme: The programme.
    #     :param status: The status of the student programme.
    #     :param admission_date: The date of admission of a student on this programme.
    #     :param stages: List of stages for acquired programmes.
    #     :param is_primary: True if this programme is marked as his/her primary programme.
    #     """
    #     self.id = id
    #     self.user = user
    #     self.programme = programme
    #     self.status = status
    #     self.admission_date = admission_date
    #     self.stages = stages
    #     self.is_primary = is_primary

    def __repr__(self):
        """
        Return a string representation of the StudentProgramme.
        """
        return f"<StudentProgramme {self.id}>"
