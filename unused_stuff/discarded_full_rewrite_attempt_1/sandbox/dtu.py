from grade import Grade
from school import School
from dtu_grades import DtuGrades

class Dtu(School):
    """ Grade distribution across DTU's different types of grades """

    def instantiate_grades(self) -> dict[str:'Grade']:
        return DtuGrades.generate_grades()