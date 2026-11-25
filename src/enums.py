from enum import Enum


class UserRole(str, Enum):
    SYSTEM_ADMIN = "system_admin"
    STUDENT = "student"
    SECRETARY = "secretary"
    EVALUATOR = "evaluator"
    PROGRAM_DIRECTOR = "program_director"
    QUALITY_TEAM = "quality_team"
    COORDINATOR = "coordinator"
    FACULTY_REVIEWER = "faculty_reviewer"
