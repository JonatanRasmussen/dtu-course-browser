from html_parser import HtmlParser
from term import Term



class HtmlLocator:
    """ Low-level class that deterministically generates (or scrapes)
        urls that contains grades, evaluations and information for DTU
        courses. The urls are requsted via the html-scraper class that
        uses them to perform the actual web scraping """

    @staticmethod
    def locate_course_archive(term: str) -> list[str]:
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
        academic_year: str = Term.get_academic_year_from_str(term)
        urls: list[str] = []
        for char in ALPHABET:
            url_path: str = f'/archive/{academic_year}/letter/{char}'
            urls.append(URL_HOSTNAME + url_path)
        return urls

    @staticmethod
    def locate_evaluations(course_id: str, term: str, search_result: str) -> dict[str:str]:
        """ The evaluation urls are undeterministic and are obtained
            via scraping. The input, 'search_result', is a html-string
            that contains 'href_digits' needed to generate the url """
        href_digits: str = HtmlParser.parse_href_digits(search_result, term)
        url: str = ""
        if len(href_digits) != 0:
            URL_HOSTNAME: str = "https://evaluering.dtu.dk"
            url_path: str = f'/kursus/{course_id}/{href_digits}'
            url = URL_HOSTNAME + url_path
        return url

    @staticmethod
    def locate_grades(course_id: str, term: str) -> str:
        """ Deterministically generate the url for the specified grade page """
        exam_period: str = Term.get_exam_period_from_str(term)
        URL_HOSTNAME: str = "https://karakterer.dtu.dk"
        url_path: str = f'/Histogram/1/{course_id}/{exam_period}'
        url: str = URL_HOSTNAME + url_path
        return url

    @staticmethod
    def locate_information(course_id: str, term: str) -> str:
        """ Deterministically generate the url for the specified info page """
        academic_year: str = Term.get_academic_year_from_str(term)
        URL_HOSTNAME: str = "https://kurser.dtu.dk"
        url_path: str = f'/course/{academic_year}/{course_id}'
        url: str = URL_HOSTNAME + url_path
        return url
