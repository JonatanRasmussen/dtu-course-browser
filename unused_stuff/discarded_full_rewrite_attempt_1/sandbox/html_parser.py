""" External modules """
import urllib
import pandas as pd
from bs4 import BeautifulSoup


class HtmlParser:
    """ Parse raw page source html to a variety of desired formats """

    @staticmethod
    def parse_course_archive(page_source_list: list[str]) -> dict[str,str]:
        """ Extract pairs of course IDs and Names from page source and return them as a dict """
        course_dct: dict[str, str] = {}
        for page_source in page_source_list:
            course_dct.update(HtmlParser._parse_course_list(page_source))
        return course_dct

    @staticmethod
    def _parse_course_list(page_source: str) -> dict[str,str]:
        soup = BeautifulSoup(page_source, 'html.parser')
        table: any = soup.find('table', {'class': 'table'})
        dct: dict[str,str] = {}
        if table is not None:
            rows: any = table.find_all('tr')[1:]
            for row in rows:
                course_id: str = row.find('td').text
                course_name: str = row.find_all('td')[1].text
                dct[course_id] = course_name
        sorted_dct: dict[str,str] = {key: dct[key] for key in sorted(dct)}
        return sorted_dct


    @staticmethod
    def parse_evaluations(page_source: str) -> str:
        """ temp """
        a: str = page_source
        b = "ø"
        return a+b

    @staticmethod
    def parse_grades(page_source: str) -> dict[str,int]:
        """ Pandas grabs the raw html of the specified url and attempts to extract any tables it can find. If the url links to
            a valid exam period for the course, 3 tables will be found (the 3rd table contains the grades), and the grades are
            formatted into a dict. If the url contains 0 tables, the exam period is invalid and an empty dict is returned instead."""
        df_found = False
        try:
            # We assunme that if pd.read_html finds a table, the url contain grades
            df = pd.read_html(page_source, header=0)
            # These grades are loaded into a dictionary based on the following code
            table_containing_grades = df[2]
            df_found = True
            table_containing_grades = table_containing_grades.set_index('Karakter')
            table_containing_grades = table_containing_grades.iloc[:,0]
            scraped_dict = table_containing_grades.to_dict()
            scraped_dict = {str(k): v for k, v in scraped_dict.items()}
            scraped_dict = {k.capitalize(): v for k, v in scraped_dict.items()}
        # If url is invalid (no table found), then return an empty dict
        except (urllib.error.HTTPError, IndexError):
            scraped_dict = {}
        # If the following ever happens it probably means that DTU has updated their website and I have to re-write my code
        if scraped_dict == {} and df_found is True:
            raise ValueError("Grades found on url but dict is empty. DTU might have updated their site")
        return scraped_dict

    @staticmethod
    def parse_href_digits(search_result: str, term: str) -> str:
        """ Extract and return a dict of each semester and the url pointing to its evaluations """
        soup = BeautifulSoup(search_result, 'html.parser')
        div_elements: any = soup.find_all('div', class_='Term')
        dct: dict[str,str] = {} # The terms that were returned from the search_result
        for div_element in div_elements:
            semester: str = div_element.text.strip()
            if semester != "Semester": #The Semester-key has a NoneType parent; don't add to dict
                href: str = div_element.find_parent('a')['href']
                formatted_semester: str = semester.replace('-', "")[:3] #Format 'E-18-13' to 'E18'
                formatted_href: str = href.split('/')[-1]# Format '/kursus/01005/168580' to '168580'
                dct[formatted_semester] = formatted_href
        if term in dct:
            href_digits: str = dct[term]
        else:
            href_digits = ""
        return href_digits
