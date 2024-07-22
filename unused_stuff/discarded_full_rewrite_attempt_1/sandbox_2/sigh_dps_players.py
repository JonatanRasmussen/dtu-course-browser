# External modules
from typing import Dict, List
from abc import ABC, abstractmethod
from bs4 import BeautifulSoup

# Custom imports
from web_scraping_tool import WebScrapingTool


#https://refactoring.guru/design-patterns/bridge

class Persistence:

    @staticmethod
    def exists_in_cache(scrape_key: str) -> bool:
        pass

    @staticmethod
    def exists_in_database(parse_key: str) -> bool:
        pass

    @staticmethod
    def exists_in_memory(deserialize_key: str) -> bool:
        pass

    @staticmethod
    def read_from_cache(scrape_key: str) -> str:
        pass

    @staticmethod
    def read_from_database(parse_key: str) -> dict[str:str]:
        pass

    @staticmethod
    def read_from_memory(deserialize_key: str) -> 'BaseDataObject':
        pass

    @staticmethod
    def write_to_cache(scrape_key: str, scraped_data: str) -> None:
        pass

    @staticmethod
    def write_to_database(parse_key: str, parsed_data: dict[str:str]) -> None:
        pass

    @staticmethod
    def write_to_memory(deserialize_key: str, deserialized_data: 'BaseDataObject') -> None:
        pass

class DataStrategy(ABC):

    WEBDRIVER = WebScrapingTool()

    def __init__(self) -> None:
        self._custom_object: BaseDataObject | None = None
        self._scraped_data: str = ""
        self._parsed_data: dict[str:str] = {}
        self._deserialized_data: BaseDataObject | None = None
        self._scrape_key: str = self._generate_scrape_name()
        self._parse_key: str = self._generate_parse_name()
        self._deserialize_key: str = self._generate_deserialize_name()

    def get_deserialized_data(self) -> 'BaseDataObject':
        return self._deserialized_data
    def set_deserialized_data(self, data_object: 'BaseDataObject') -> None:
        self._deserialized_data = data_object

    def access_data(self, custom_object: 'BaseDataObject'):
        self._custom_object = custom_object
        if self._deserialized_data_exists():
            self._deserialized_data = self._load_deserialized_data()
        elif self._parsed_data_exists():
            self._parsed_data = self._load_parsed_data()
            self._deserialized_data = self._deserialize_data()
        elif self._scraped_data_exists():
            self._scraped_data = self._load_scraped_data()
            self._parsed_data = self._parse_data(self._scraped_data)
            self._deserialized_data = self._deserialize_data()
        else:
            self._scraped_data = self._scrape_data(custom_object)
            self._parsed_data = self._parse_data(self._scraped_data)
            self._deserialized_data = self._deserialize_data()
        self._store_data()
        return self.get_deserialized_data()

    def _store_data(self):
        if len(self._scraped_data) != 0:
            self._store_scraped_data()
        if len(self._parsed_data) != 0:
            self._store_parsed_data()
        if self._deserialized_data is not None:
            self._store_deserialized_data()

    def _scraped_data_exists(self) -> bool:
        return Persistence.exists_in_cache(self._scrape_key)
    def _parsed_data_exists(self) -> bool:
        return Persistence.exists_in_database(self._parse_key)
    def _deserialized_data_exists(self) -> bool:
        return Persistence.exists_in_memory(self._deserialize_key)

    def _load_scraped_data(self) -> str:
        return Persistence.read_from_cache(self._scrape_key)
    def _load_parsed_data(self) -> dict[str:str]:
        return Persistence.read_from_database(self._parse_key)
    def _load_deserialized_data(self) -> 'BaseDataObject' | None:
        return Persistence.read_from_memory(self._deserialize_key)

    def _store_scraped_data(self) -> None:
        Persistence.write_to_cache(self._scraped_data, self._scrape_key)
    def _store_parsed_data(self) -> None:
        Persistence.write_to_database(self._parsed_data, self._parse_key)
    def _store_deserialized_data(self) -> None:
        Persistence.write_to_memory(self._deserialized_data, self._deserialize_key)

    def _generate_scrape_name(self) -> str:
        SCRAPE_IDENTIFIER: str = "raw"
        return f"{self._generate_data_name()}_{SCRAPE_IDENTIFIER}"

    def _generate_parse_name(self) -> str:
        PARSE_IDENTIFIER: str = "map"
        return f"{self._generate_data_name()}_{PARSE_IDENTIFIER}"

    def _generate_deserialize_name(self) -> str:
        DESERIALIZE_IDENTIFIER: str = "obj"
        return f"{self._generate_data_name()}_{DESERIALIZE_IDENTIFIER}"

    @staticmethod
    @abstractmethod
    def _scrape_data(data_object: 'BaseDataObject') -> str:
        pass

    @staticmethod
    @abstractmethod
    def _parse_data(scraped_data: str) -> dict[str:str]:
        pass

    @abstractmethod
    def _deserialize_data(self) -> 'BaseDataObject':
        pass

    @abstractmethod
    def _generate_data_name(self) -> str:
        pass

    @abstractmethod
    def _returns_list(self) -> bool:
        pass

class CourseStrategy(DataStrategy):

    @staticmethod
    def _scrape_data(course_object: 'Course') -> str:

        year: str = course_object.get_year().name()
        return CourseStrategy.scrape_course(year)

    @staticmethod
    def _parse_data(scraped_data: str) -> dict[str:str]:
        return CourseStrategy.parse_course(scraped_data)

    @staticmethod
    @abstractmethod
    def scrape_course(course_object) -> str:
        pass

    @staticmethod
    @abstractmethod
    def parse_course(scraped_data) -> dict[str:str]:
        pass

class DtuCourses(DataStrategy):

    @staticmethod
    def _scrape_data(academic_year) -> str:
        """ Deterministically generate a list of urls that covers the
            full course archive for a given academic year. The course
            list is split across several urls, one per starting letter
            https://kurser.dtu.dk/archive/2022-2023/letter/A
            https://kurser.dtu.dk/archive/2022-2023/letter/B
            ...
            https://kurser.dtu.dk/archive/2022-2023/letter/Z.
            Obtained the complete list by accessing each letter """
        URL_HOSTNAME: str = "https://kurser.dtu.dk"
        ALPHABET: list[str] = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J',
                                'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T',
                                'U', 'V', 'W', 'X', 'Y', 'Z', 'Æ', 'Ø', 'Å']
        concatenated_html: str = ""
        for char in ALPHABET:
            url_path: str = f'/archive/{academic_year}/letter/{char}'
            url = URL_HOSTNAME + url_path
            concatenated_html += DtuCourses.WEBDRIVER.get_page_source(url)
        return concatenated_html

    @staticmethod
    def _parse_data(scraped_data) -> any:
        soup = BeautifulSoup(scraped_data, 'html.parser')
        all_tables: any = soup.find_all('table', {'class': 'table'})
        dct: dict[str,str] = {}
        for table in all_tables:
            rows: any = table.find_all('tr')[1:]
            for row in rows:
                course_id: str = row.find('td').text
                course_name: str = row.find_all('td')[1].text
                if course_id in dct:
                    print(f"ID {course_id} {course_name} already exists in dct: {dct[course_id]}")
                dct[course_id] = course_name
        sorted_dct: dict[str,str] = {key: dct[key] for key in sorted(dct)}
        return sorted_dct

class EvaluationStrategy(DataStrategy):

    @staticmethod
    def _scrape_data(evaluation_object: 'Evaluation') -> str:
        year: str = evaluation_object.get_year().name()
        course: str = evaluation_object.get_course().name()
        term: str = evaluation_object.get_term().name()
        return EvaluationStrategy.scrape_evaluation(year, course, term)

    @staticmethod
    def _parse_data(scraped_data: str) -> dict[str:str]:
        return EvaluationStrategy.parse_evaluation(scraped_data)

    @staticmethod
    @abstractmethod
    def scrape_evaluation(year: str, course: str, term: str) -> str:
        pass

    @staticmethod
    @abstractmethod
    def parse_evaluation(scraped_data: str) -> dict[str:str]:
        pass

class DtuEvaluation(DataStrategy):

    @staticmethod
    def scrape_evaluation(year: str, course: str, term: str) -> str:
        pass

    @staticmethod
    def parse_evaluation(scraped_data: str) -> dict[str:str]:
        pass

class GradeSheetStrategy(DataStrategy):

    @staticmethod
    def _scrape_data(grade_sheet_object: 'GradeSheet') -> str:
        year: str = grade_sheet_object.get_year().name()
        course: str = grade_sheet_object.get_course().name()
        term: str = grade_sheet_object.get_term().name()
        return GradeSheetStrategy.scrape_grade_sheet(year, course, term)

    @staticmethod
    def _parse_data(scraped_data: str) -> dict[str:str]:
        return GradeSheetStrategy.parse_grade_sheet(scraped_data)

    @staticmethod
    @abstractmethod
    def scrape_grade_sheet(year: str, course: str, term: str) -> str:
        pass

    @staticmethod
    @abstractmethod
    def parse_grade_sheet(scraped_data: str) -> dict[str:str]:
        pass

class DtuGradeSheet(DataStrategy):

    @staticmethod
    def scrape_grade_sheet(year: str, course: str, term: str) -> str:
        pass

    @staticmethod
    def parse_grade_sheet(scraped_data: str) -> dict[str:str]:
        pass

class InfoPageStrategy(DataStrategy):

    @staticmethod
    def _scrape_data(info_page_object: 'InfoPage') -> str:
        year: str = info_page_object.get_year().name()
        course: str = info_page_object.get_course().name()
        return InfoPageStrategy.scrape_info_page(year, course)

    @staticmethod
    def _parse_data(scraped_data: str) -> dict[str:str]:
        return InfoPageStrategy.parse_info_page(scraped_data)

    @staticmethod
    @abstractmethod
    def scrape_info_page(year: str, course: str) -> str:
        pass

    @staticmethod
    @abstractmethod
    def parse_info_page(scraped_data: str) -> dict[str:str]:
        pass

class DtuInfoPage(DataStrategy):

    @staticmethod
    def scrape_info_page(year: str, course: str) -> str:
        pass

    @staticmethod
    def parse_info_page(scraped_data: str) -> dict[str:str]:
        pass

class StudyLineStrategy(DataStrategy):

    @staticmethod
    def _scrape_data(study_line_object: 'StudyLine') -> str:
        year: str = study_line_object.get_year().name()
        course: str = study_line_object.get_course().name()
        return StudyLineStrategy.scrape_study_line(year, course)

    @staticmethod
    def _parse_data(scraped_data: str) -> dict[str:str]:
        return StudyLineStrategy.parse_study_line(scraped_data)

    @staticmethod
    @abstractmethod
    def scrape_study_line(year: str, course: str) -> str:
        pass

    @staticmethod
    @abstractmethod
    def parse_study_line(scraped_data: str) -> dict[str:str]:
        pass

class DtuStudyLine(DataStrategy):

    @staticmethod
    def scrape_study_line(year: str, course: str) -> str:
        pass

    @staticmethod
    def parse_study_line(scraped_data: str) -> dict[str:str]:
        pass

class TeacherStrategy(DataStrategy):

    @staticmethod
    def _scrape_data(teacher_object: 'Teacher') -> str:
        year: str = teacher_object.get_year().name()
        return TeacherStrategy.scrape_teacher(year)

    @staticmethod
    def _parse_data(scraped_data: str) -> dict[str:str]:
        return TeacherStrategy.parse_teacher(scraped_data)

    @staticmethod
    @abstractmethod
    def scrape_teacher(year: str) -> str:
        pass

    @staticmethod
    @abstractmethod
    def parse_teacher(scraped_data: str) -> dict[str:str]:
        pass

class DtuTeacher(DataStrategy):

    @staticmethod
    def scrape_teacher(year: str) -> str:
        pass

    @staticmethod
    def parse_teacher(scraped_data: str) -> dict[str:str]:
        pass

class TermStrategy(DataStrategy):

    @staticmethod
    def _scrape_data(term_object: 'Term') -> str:
        year: str = term_object.get_year().name()
        course: str = term_object.get_course().name()
        return TermStrategy.scrape_term(year, course)

    @staticmethod
    def _parse_data(scraped_data: str) -> dict[str:str]:
        return TermStrategy.parse_term(scraped_data)

    @staticmethod
    @abstractmethod
    def scrape_term(year: str, course: str) -> str:
        pass

    @staticmethod
    @abstractmethod
    def parse_term(scraped_data: str) -> dict[str:str]:
        pass

class DtuTerm(DataStrategy):

    @staticmethod
    def scrape_term(year: str, course: str) -> str:
        pass

    @staticmethod
    def parse_term(scraped_data: str) -> dict[str:str]:
        pass

class YearStrategy(DataStrategy):

    @staticmethod
    def _scrape_data(year_object: 'Year') -> str:
        year: str = year_object.get_year().name()
        return YearStrategy.scrape_year(year)

    @staticmethod
    def _parse_data(scraped_data: str) -> dict[str:str]:
        return YearStrategy.parse_year(scraped_data)

    @staticmethod
    @abstractmethod
    def scrape_year(year: str) -> str:
        pass

    @staticmethod
    @abstractmethod
    def parse_year(scraped_data: str) -> dict[str:str]:
        pass

class DtuYear(DataStrategy):

    @staticmethod
    def scrape_year() -> str:
        pass

    @staticmethod
    def parse_year(scraped_data: str) -> dict[str:str]:
        pass

class DataOrigin(ABC):

    @staticmethod
    def get_data_retrieval_strategy(custom_object: any) -> DataStrategy:
        if isinstance(custom_object, Course):
            return DataOrigin.course_strategy()
        elif isinstance(custom_object, Evaluation):
            return DataOrigin.evaluation_strategy()
        elif isinstance(custom_object, GradeSheet):
            return DataOrigin.grade_sheet_strategy()
        elif isinstance(custom_object, InfoPage):
            return DataOrigin.info_page_strategy()
        elif isinstance(custom_object, StudyLine):
            return DataOrigin.study_line_strategy()
        elif isinstance(custom_object, Teacher):
            return DataOrigin.teacher_strategy()
        else:
            raise ValueError("Custom_object is of an unsupported type")

    @staticmethod
    @abstractmethod
    def get_domain_name() -> str:
        return DataOrigin.__name__

    @staticmethod
    @abstractmethod
    def course_strategy():
        pass

    @staticmethod
    @abstractmethod
    def evaluation_strategy():
        pass

    @staticmethod
    @abstractmethod
    def grade_sheet_strategy():
        pass

    @staticmethod
    @abstractmethod
    def info_page_strategy():
        pass

    @staticmethod
    @abstractmethod
    def study_line_strategy():
        pass

    @staticmethod
    @abstractmethod
    def teacher_strategy():
        pass

    @staticmethod
    @abstractmethod
    def year_strategy():
        pass


class DtuData(DataOrigin):

    @staticmethod
    def course_strategy():
        return DtuCourses

    @staticmethod
    def evaluation_strategy():
        return DtuEvaluation

    @staticmethod
    def grade_sheet_strategy():
        return DtuGradeSheet

    @staticmethod
    def info_page_strategy():
        return DtuInfoPage

    @staticmethod
    def study_line_strategy():
        return DtuStudyLine

    @staticmethod
    def teacher_strategy():
        return DtuTeacher

    @staticmethod
    def term_strategy():
        return DtuTerm

    @staticmethod
    def year_strategy():
        return DtuYear


class BaseDataObject(ABC):

    def __init__(self) -> None:
        self.name: str = ""
        self.parent: BaseDataObject | None = None
        self.data_origin: DataOrigin | None = None

    @staticmethod
    def get_data_strategy() -> DataStrategy | None:
        return None

    def get_class_name(self) -> str:
        return self.__class__.__name__

    def get_name(self) -> str:
        return self.name
    def set_name(self, name: str) -> None:
        self.name = name

    def get_parent(self) -> 'BaseDataObject':
        return self.parent
    def set_parent(self, parent: 'BaseDataObject') -> None:
        self.parent = parent

    def get_data_origin(self) -> DataOrigin:
        return self.data_origin
    def set_data_origin(self, data_origin: DataOrigin) -> None:
        self.data_origin = data_origin

    @staticmethod
    @abstractmethod
    def get_child_classes() -> list[type['BaseDataObject']]:
        pass

    @abstractmethod
    def cascade_build(self):
        pass

class AbstractContainer(BaseDataObject):

    def __init__(self) -> None:
        super().__init__()
        self.data_container: Dict[str, Dict[str, BaseDataObject]] = {}

    def cascade_build(self):
        for child_class in self.get_child_classes():
            key: str = child_class.get_class_name()
            self.add_new_dictionary(key)
            strategy: DataStrategy = child_class.data_origin.get_data_strategy()
            for item in strategy.access_data(self):
                child_object = child_class()
                child_object.name = item
                child_object.parent = self
                child_object.data_origin = self.data_origin
                child_object.cascade_build()
                self.add_dictionary_element(key, item, child_object)

    def get_full_dictionary(self, dct_key: str) -> Dict[str, 'BaseDataObject']:
        return self.data_container[dct_key]
    def get_dictionary_element(self, outer_key: str, inner_key: str) -> any:
        return self.data_container[outer_key][inner_key]

    def add_new_dictionary(self, dct_key: str) -> None:
        self.data_container[dct_key] = {}
    def add_dictionary_element(self, outer_key: str, inner_key: str, element: 'BaseDataObject') -> None:
        self.data_container[outer_key][inner_key] = element


class DataPoint(BaseDataObject):

    def __init__(self) -> None:
        super().__init__()
        self.term: str = ""
        self.data_point: DataPoint | None = None

    def cascade_build(self):
        strategy: DataStrategy = self.data_origin.get_data_strategy()
        data_object: BaseDataObject = strategy.access_data(self)
        self.data_point = data_object

class School(AbstractContainer):

    @staticmethod
    def get_child_classes() -> list[type['BaseDataObject']]:
        return [Year, Teacher]

    def initialize_data_strategy(self) -> DataStrategy:
        return None

class Year(AbstractContainer):

    @staticmethod
    def get_child_classes() -> list[type['BaseDataObject']]:
        return [Course, StudyLine]

    def initialize_data_strategy(self) -> DataStrategy:
        return self.data_origin.year_strategy()

class Course(AbstractContainer):

    @staticmethod
    def get_child_classes() -> list[type['BaseDataObject']]:
        return [Term, InfoPage]

    def initialize_data_strategy(self) -> DataStrategy:
        return self.data_origin.course_strategy()

class Term(AbstractContainer):

    @staticmethod
    def get_child_classes() -> list[type['BaseDataObject']]:
        return [Evaluation, GradeSheet]

    def initialize_data_strategy(self) -> DataStrategy:
        return self.data_origin.term_strategy()

class Teacher(AbstractContainer):

    @staticmethod
    def get_child_classes() -> list[type['BaseDataObject']]:
        return [Course]

    def initialize_data_strategy(self) -> DataStrategy:
        return self.data_origin.teacher_strategy()

class StudyLine(AbstractContainer):

    @staticmethod
    def get_child_classes() -> list[type['BaseDataObject']]:
        return [Course]

    def initialize_data_strategy(self) -> DataStrategy:
        return self.data_origin.study_line_strategy()

class Evaluation(DataPoint):

    def initialize_data_strategy(self) -> DataStrategy:
        return self.data_origin.evaluation_strategy()


class GradeSheet(DataPoint):

    def initialize_data_strategy(self) -> DataStrategy:
        return self.data_origin.grades_sheet_strategy()

class InfoPage(DataPoint):

    def initialize_data_strategy(self) -> DataStrategy:
        return self.data_origin.info_page_strategy()