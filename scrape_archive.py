from typing import Any, List, Dict, Callable
from typing_extensions import Self
import requests
from bs4 import BeautifulSoup
from selenium.webdriver.chrome.webdriver import WebDriver

from utils import Utils
from website.global_constants.file_name_consts import FileNameConsts

# This script is new and untested and not in use as of 11/07/2024

class CourseArchive:
    def __init__(self) -> None:
        self.page_source: str = self._fetch()
        self.year_ranges: List[str] = self._parse()
        self.academic_years: Dict[str, AcademicYear] = {}
        self._populate_academic_years()

    def save_courses(self) -> None:
        archive_dictionary = {}
        for year_range in self.year_ranges:
            academic_year = self.academic_years[year_range]
            archive_dictionary[academic_year.year_range] = academic_year.courses
        file_name = FileNameConsts.archived_courses_json
        Utils.save_dct_as_json(file_name, archive_dictionary)

    def _fetch(self) -> str:
        url = "https://kurser.dtu.dk/archive/volumes"
        response = requests.get(url, timeout=10)
        return response.text

    def _parse(self) -> List[str]:
        years = []
        soup = BeautifulSoup(self.page_source, 'html.parser')
        archive_list = soup.find_all('a', href=True)
        for a in archive_list:
            if '/archive/' in a['href']:
                year = a.text.strip()
                years.append(year.replace('/', '-'))
        return years

    def _populate_academic_years(self) -> None:
        print('Course archive main page scraped...')
        for year_range in self.year_ranges:
            print(f'Scraping {year_range}...')
            academic_year = AcademicYear(year_range)
            self.academic_years[year_range] = academic_year
            print(f'Finished scraping {year_range} ({len(academic_year.courses)} courses found)')


class AcademicYear:
    def __init__(self, year_range: str) -> None:
        self._validate(year_range)
        self.year_range: str = year_range
        self.name: str = self.year_range
        self.start_year: int = int(self.name[:4])
        self.end_year: int = self.start_year + 1
        self.page_source: str = self._fetch_main_page()
        self.departments: Dict[str, str] = self._parse_departments()
        self.course_codes: List[str] = self._parse_course_codes()
        self.course_code_page_sources: List[str] = self._fetch_course_subpages()
        self.courses: Dict[str, str] = self._parse_course_code_subpage()
        self.fall_term: Term = Term.create_fall_term(self)
        self.spring_term: Term = Term.create_spring_term(self)
        self.terms: List[Term] = [self.fall_term, self.spring_term]

    @staticmethod
    def _validate(year_range: str) -> None:
        if len(year_range) != 9:
            raise ValueError("Year range must be 9 characters long")
        if year_range[4] != '-':
            raise ValueError("Year range must have a hyphen as the 5th character")
        start_year = int(year_range[0:4])
        end_year = int(year_range[5:9])
        if not 2000 <= start_year <= 2098:
            raise ValueError("Start year must be between 2000 and 2098")
        if not 2001 <= end_year <= 2099:
            raise ValueError("End year must be between 2001 and 2099")
        if end_year != start_year + 1:
            raise ValueError("End year must be exactly one year after start year")

    def _fetch_main_page(self) -> str:
        url = f"https://kurser.dtu.dk/archive/{self.year_range}"
        response = requests.get(url, timeout=10)
        response.raise_for_status()  # Check if the request was successful
        return response.text

    def _parse_departments(self) -> Dict[str, str]:
        soup = BeautifulSoup(self.page_source, 'html.parser')
        departments = {}

        department_list = soup.find('ul', style='border-top:1px solid #ddd')
        if department_list:
            for li in department_list.find_all('li'):
                a_tag = li.find('a')
                if a_tag:
                    text = a_tag.text.strip()
                    number, name = text.split(' ', 1)
                    departments[number] = name

        return departments

    def _parse_course_codes(self) -> List[str]:
        split_at = "</strong>"
        last_page_source_table = self.page_source.split(split_at)[-1]
        soup = BeautifulSoup(last_page_source_table, 'html.parser')
        course_codes = []

        table = soup.find('table', class_='table')
        if table:
            for a_tag in table.find_all('a'):
                code = a_tag.text.strip()
                course_codes.append(code)

        return course_codes

    def _fetch_course_subpages(self) -> List[str]:
        subpage_page_sources = []
        for code in self.course_codes:
            url = f"https://kurser.dtu.dk/archive/{self.year_range}/coursecode/{code}"
            response = requests.get(url, timeout=10)
            subpage_page_sources.append(response.text)
        return subpage_page_sources

    def _parse_course_code_subpage(self) -> Dict[str, str]:
        courses = {}
        for page_source in self.course_code_page_sources:
            soup = BeautifulSoup(page_source, 'html.parser')
            table = soup.find('table', class_='table')
            rows = table.find_all('tr')[1:]
            for row in rows:
                columns = row.find_all('td')
                if len(columns) == 2:
                    course_number = columns[0].text.strip()
                    course_name = columns[1].text.strip()
                    courses[course_number] = course_name
        return courses

class Term:
    FALL_TERM_CODE = 'E'
    SPRING_TERM_CODE = 'F'
    VALID_TERM_CODES = [FALL_TERM_CODE, SPRING_TERM_CODE]

    def __init__(self, name: str) -> None:
        self._validate(name)
        self.name = name

    @staticmethod
    def _validate(name: str) -> None:
        if len(name) != 3:
            raise ValueError("Term name must be 3 characters long")
        if name[0] not in Term.VALID_TERM_CODES:
            raise ValueError(f"Term code must be in {Term.VALID_TERM_CODES}")
        try:
            year = int(name[1:3])
            if not 0 <= year <= 99:
                raise ValueError("Year must be between 00 and 99")
        except ValueError as exc:
            raise ValueError("Last two characters must be numeric") from exc

    @classmethod
    def create_fall_term(cls, academic_year: AcademicYear) -> Self:
        return cls._create_term(Term.FALL_TERM_CODE, academic_year.start_year)

    @classmethod
    def create_spring_term(cls, academic_year: AcademicYear) -> Self:
        return cls._create_term(Term.SPRING_TERM_CODE, academic_year.end_year)

    @classmethod
    def _create_term(cls, term_code: str, year: int) -> Self:
        two_digit_year = year - 2000
        return cls(f"{term_code}{two_digit_year:02d}")

class ScrapeManager:
    def __init__(self) -> None:
        self.driver: WebDriver = Utils.launch_selenium()

    def scrape(self, url: str, use_selenium: bool, parser: Callable[[str], Any]):
        page_source = ""
        if use_selenium:
            page_source = Utils.access_url_via_selenium(url, self.driver)
        else:
            page_source = Utils.access_url_via_requests_get(url)
        return parser(page_source)

#%%
if __name__ == "__main__":

    course_archive = CourseArchive()
    course_archive.save_courses()