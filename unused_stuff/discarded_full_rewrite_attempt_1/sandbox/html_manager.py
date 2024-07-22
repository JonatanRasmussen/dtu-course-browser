from web_scraping_tool_legacy import WebScrapingTool
from html_locator import HtmlLocator
from html_parser import HtmlParser
from html_slicer import HtmlSlicer
from html_persistence import HtmlPersistence

class HtmlManager:
    """ A top-level class for scraping and storing all data
        associated with a given term. It instantiates the
        html-scraper class and organizes its output into dicts.
        The dicts contain raw html strings (page source), and the
        dicts can be saved as files or passed on to other classes """

    def __init__(self: 'HtmlManager', term: str) -> None:
        """ Instantiate a single manager per term, as a single
            HtmlManager can't manage data from multiple terms """
        self._term: str = term
        self._scrape_tool: 'WebScrapingTool' = WebScrapingTool()
        self._course_dct: dict[str:str] = {}
        self._evaluation_dct: dict[str:str] = {}
        self._grades_dct: dict[str:str] = {}
        self._information_dct: dict[str:str] = {}
        self._study_line_dct: dict[str:str] = {}

    @classmethod
    def custom_courses(cls: 'HtmlManager', term: str, course_dct: dict[str:str]) -> 'HtmlManager':
        manager: 'HtmlManager' = cls(term)
        manager._course_dct = course_dct
        return manager

    def scrape_study_lines(self: 'HtmlManager') -> None:
        """ todo """

    def scrape_course_data(self: 'HtmlManager') -> None:
        """ Iterate over each course for a given term and scrape all
            course-related data (evaluations, grades and information) """
        course_list: list[str] = self.get_course_list()
        self._fix_weird_timeout_bug(course_list)
        for course in course_list:
            self.scrape_evaluations(course)
            self.scrape_grades(course)
            self.scrape_information(course)

    def get_course_list(self) -> list[str]:
        """ Convert _course_dct to a list of the term's course IDs """
        if len(self._course_dct) == 0:
            self._scrape_course_archive()
        course_list: list[str] = list(self._course_dct.keys())
        return course_list

    def scrape_evaluations(self: 'HtmlManager', course: str) -> None:
        """ Scrape page source and store part of it in _evaluations_dct """
        search_result: str = self._scrape_tool.search_for_evaluation_hrefs(course)
        url: str = HtmlLocator.locate_evaluations(course, self._term, search_result)
        page_source = self._scrape_tool.get_page_source(url)
        sliced_html: str = HtmlSlicer.slice_evaluation_html(page_source, course, self._term)
        self._evaluation_dct[course] = sliced_html

    def scrape_grades(self: 'HtmlManager', course: str) -> None:
        """ Scrape page source and store part of it in _grades_dct """
        url: str = HtmlLocator.locate_grades(course, self._term)
        page_source: str = self._scrape_tool.get_page_source(url)
        sliced_html: str = HtmlSlicer.slice_grade_html(page_source, course, self._term)
        self._grades_dct[course] = sliced_html

    def scrape_information(self: 'HtmlManager', course: str) -> None:
        """ Scrape page source and store part of it in _information_dct """
        url: str = HtmlLocator.locate_information(course, self._term)
        page_source: str = self._scrape_tool.get_page_source(url)
        sliced_html: str = HtmlSlicer.slice_information_html(page_source, course, self._term)
        self._information_dct[course] = sliced_html

    def store_html(self: 'HtmlManager') -> None:
        """ Store the scraped html via the persistence class """
        HtmlPersistence.store_evaluation_html(self._evaluation_dct, self._term)
        HtmlPersistence.store_grade_html(self._grades_dct, self._term)
        HtmlPersistence.store_information_html(self._information_dct, self._term)

    def _scrape_course_archive(self: 'HtmlManager') -> None:
        """ Scrape page source and store it in _course_dct """
        raw_html_list: list[str] = []
        urls: list[str] = HtmlLocator.locate_course_archive(self._term)
        for url in urls:
            page_source: str = self._scrape_tool.get_page_source(url)
            raw_html_list.append(page_source)
        self._course_dct = HtmlParser.parse_course_archive(raw_html_list)

    def _fix_weird_timeout_bug(self: 'HtmlManager', course_list):
        """ The first information scrape will for some reason return
            a useless timeout page. My lazy attempt at a bugfix is to
            'flush out' the timeout page with a redundant scrape """
        if len(course_list) > 0:
            url: str = HtmlLocator.locate_information(course_list[0], self._term)
            _: str = self._scrape_tool.get_page_source(url)
