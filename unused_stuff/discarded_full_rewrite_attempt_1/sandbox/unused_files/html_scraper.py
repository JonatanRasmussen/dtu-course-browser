'''
from term import Term

from web_scraping_tool import WebScrapingTool
from html_locator import HtmlLocator
from html_parser import HtmlParser

class HtmlScraper:
    """ This is a mid-level class that carries out the actual web
        scraping. It is managed and controlled by the html-manager
        class. Its purpose it to scrape and return page sources.
        The web scraping is achieved via the 'WebScrapingTool' """

    def __init__(self) -> None:
        self._evaluation_urls: dict[str,dict[str,str]] = {}
        self._scrape_tool: 'WebScrapingTool' = WebScrapingTool()

    def get_course_list(self, term) -> list[str]:
        raw_html_list: list[str] = self._scrape_course_archive(term)
        course_dct: dict[str,str] = HtmlParser.parse_course_archive(raw_html_list)
        course_list: list[str] = HtmlParser.convert_course_dict_to_list(course_dct)
        return course_list

    def scrape_evaluations(self: 'HtmlScraper', course_id: str, term: str) -> str:
        urls: dict[str,str] = self._get_evaluation_url(course_id)
        term = Term.validate_string(term)
        page_source: str = ""
        if term in urls:
            url: str = urls[term]
            page_source = self._scrape_tool.get_page_source(url)
        return page_source

    def scrape_grades(self: 'HtmlScraper', course_id: str, term: str) -> str:
        url: str = HtmlLocator.locate_grades(course_id, term)
        page_source: str = self._scrape_tool.get_page_source(url)
        return page_source

    def scrape_information(self: 'HtmlScraper', course_id: str, term: str) -> str:
        url: str = HtmlLocator.locate_information(course_id, term)
        page_source: str = self._scrape_tool.get_page_source(url)
        return page_source

    def _scrape_course_archive(self, term) -> list[str]:
        raw_html_list: list[str] = []
        urls: list[str] = HtmlLocator.locate_course_archive(term)
        for url in urls:
            page_source: str = self._scrape_tool.get_page_source(url)
            raw_html_list.append(page_source)
        return raw_html_list

    def _get_evaluation_url(self: 'HtmlScraper', course_id: str) -> dict[str,str]:
        dct: dict[str, dict[str, str]] = self._evaluation_urls
        if course_id in dct:
            urls: dict[str,str] = dct[course_id]
        else:
            href_page_source: str = self._access_href_digits(course_id)
            urls = HtmlLocator.locate_evaluations(course_id, href_page_source)
            self._evaluation_urls[course_id] = urls
        return urls

    def _access_href_digits(self: 'HtmlScraper', course_id: str) -> str:
        page_source: str = self._scrape_tool.search_for_evaluation_hrefs(course_id)
        return page_source

#%%
if __name__ == "__main__":
    testy = HtmlScraper()
    c02402 = "02402"
    c01015 = "01015"
    my_ps: str = testy.scrape_evaluations(c02402, 'E20')
    my_ps = testy.scrape_evaluations(c02402, 'E21')
    my_ps = testy.scrape_evaluations(c02402, 'F20')
    my_ps = testy.scrape_evaluations(c01015, 'F21')
    my_ps = testy.scrape_evaluations(c01015, 'E20')
    my_ps = testy.scrape_evaluations(c02402, 'F21')
    print('done')
'''