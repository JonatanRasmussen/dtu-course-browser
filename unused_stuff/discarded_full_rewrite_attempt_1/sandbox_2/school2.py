from typing import Dict, Tuple
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from __main__ import Grades



class Persistence:

    @staticmethod
    def load_school_object() -> 'School':
        pass

    @staticmethod
    def save_school_object() -> 'School':
        pass




class School():

    def __init__(self, name: str) -> None:
        self.school_name: str = name
        self.years: Dict[str,'Year'] = {}

    @classmethod
    def load_from_database(cls) -> None:
        return Persistence.load_school_object()

    def save_from_database(self) -> None:
        Persistence.save_school_object(self)


class DTU(School):

    # ACADEMIC YEARS
    YEAR_START: int = 2017
    YEAR_END: int = 2024

    @staticmethod
    def initialize_years(year_range: Tuple[int, int]) -> None:
        years: Dict[str,Year] = {}
        for _ in range(year_range):
            year_name: str = Year._generate_year_key(year_range)
            year_object: Year = Year(year_name)

            years[year_name] = year_object
        return years

    def _initialize_year(year_name: str) -> 'Year':
        year: Year = Year(year_name)
        year.initialize_all_courses()
        return year

    @staticmethod
    def _generate_year_key(year: int) -> str:
        return f"{str(year)}'-'{str(1+year)}"


class Year:
    def __init__(self, school: 'School', name: str) -> None:
        self.school_name: str = school.get_school_name()
        self.year_name: str = name
        self.courses: Dict[str,'Course'] = {}

    @staticmethod
    def initialize_years(year_range: Tuple[int, int]) -> None:
        years: Dict[str,Year] = {}
        for _ in range(year_range):
            year_name: str = Year._generate_year_key(year_range)
            year_object: Year = Year(year_name)

            years[year_name] = year_object
        return years

    def _initialize_year(self, year_name: str) -> 'Year':
        year: Year = Year(self, year_name)
        year.initialize_all_courses()
        return year

    @staticmethod
    def _generate_year_key(year: int) -> str:
        return f"{str(year)}'-'{str(1+year)}"



    def initialize_all_courses(self) -> None:
        for course in self.courses:
            pass


    def initialize_course(self, key: str) -> 'Year':
        return Year(self, key)



class Course:
    def __init__(self, name: str) -> None:
        self.name = name
        self.instances: Dict[str,'CourseInstance'] = {}
        self.info: 'InfoPage' = InfoPage()

    def get_name(self) -> str:
        return self.name

    def get_instance(self, term_name: str) -> Dict[str,'Course']:
        return self.instances[term_name]

    def get_all_instances(self) -> Dict[str,'Course']:
        return self.instances


class CourseInstance:
    def __init__(self, name: str) -> None:
        self.name = name
        self.term: str = ""
        self.evals: 'Evaluation' = Evaluation()
        self.grades: 'GradeSheet' = GradeSheet()

    def get_name(self) -> str:
        return self.name

    def get_evals(self) -> 'Evaluation':
        return self.evals

    def get_grades(self) -> 'GradeSheet':
        return self.grades


class Evaluation:
    def __init__(self, term: str) -> None:
        self.term: 'CourseInstance' = term
        self.my_var: str = ""

    def get_my_var(self) -> str:
        return self.my_var


class GradeSheet:
    def __init__(self, term: str) -> None:
        self.term: 'CourseInstance' = term
        self.my_var: str = ""

    def get_my_var(self) -> str:
        return self.my_var


class InfoPage:
    def __init__(self, course: 'Course') -> None:
        self.course: 'Course' = course
        self.my_var: str = ""

    def get_my_var(self) -> str:
        return self.my_var


if __name__ == "__main__":
    dtu = DTU()
