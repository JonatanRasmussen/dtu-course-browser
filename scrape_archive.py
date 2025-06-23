import requests
import json
import os
from bs4 import BeautifulSoup, Tag

from utils import Utils

class ArchiveScraper:

    @staticmethod
    def quick_test_scrape_for_debugging_please_ignore():
        """ Do a quick scrape to see if the code works."""
        course_semesters = ['F23', 'E23', 'F24']  # Example of valid semesters
        file_name = "archived_courses_test"
        ArchiveScraper.scrape_archive(course_semesters, file_name)

    @staticmethod
    def scrape_archive(course_semesters, file_name):
        """ Scrape course numbers and names that existed during the given semesters.
            Return a nested dict, with inner dict {'01005': 'Mat 1', '02402': 'Statistics', etc.}
            and outer dict {'2023-2024': [inner_dict], '2024-2025': [inner_dict]}, and so on.
            Also save the dict as json if file_name is not empty."""
        course_numbers_by_academic_year = {}  #Nested dict, the inner dict is Course code: Course Name (e.g. 02402: Statistics) and outer dict is academic years ('2023-2024', '2024-2025', etc.)
        academic_years = Utils.extract_unique_year_ranges(course_semesters)  #Convert semesters to academic years (Example: ['E23', 'F24', 'E24'] becomes ['2023-2024', '2024-2025'])
        print(f'Scraping course numbers for academic years {academic_years[0]} to {academic_years[-1]}...')
        for academic_year in academic_years:
            # What we want is a page with all courses available during a given academic year, for example 2024-2025
            # Annoyingly, this does not exist as a single page. Instead, it is spread across multiple 'course code' subpages.
            # The course code subpages are '01', '02', '10', and so on. The page for course code '01' has all the 01xxx courses, and so on.
            # Luckily, all course code subpages that exists for a given academic year is listed on the 'main page'.
            # By iterating over each course code subpage, we can obtain a complete dict of each course available during a given academic year
            course_codes = ArchiveScraper._scrape_course_codes_from_main_page(academic_year)  # All course codes available for the given year (e.g., '01', '02', '10')
            course_number_and_names = ArchiveScraper._scrape_course_code_subpages(academic_year, course_codes)  # All courses across each course code (01xxx, 02xxx, 10xxx, etc.)
            course_numbers_by_academic_year[academic_year] = course_number_and_names
            print(f'Finished scraping course numbers for academic year {academic_year} ({len(course_number_and_names)} courses found)')  # Print current academic year to console so user can track the progress
        if len(file_name) != 0:
            ArchiveScraper._save_dct_as_json(file_name, course_numbers_by_academic_year)  # Save all scraped courses as a JSON file
        return course_numbers_by_academic_year

    @staticmethod
    def scrape_course_numbers_for_semesters(course_semesters):
        """Return all course numbers that existed during the given semesters"""
        file_name = ""  # This prevents scraped course numbers from being saved to disk
        course_numbers_by_academic_year = ArchiveScraper.scrape_archive(course_semesters, file_name)
        unique_course_numbers = set()
        for inner_dict in course_numbers_by_academic_year.values():
            unique_course_numbers.update(inner_dict.keys())
        return sorted(unique_course_numbers)

    @staticmethod
    def _scrape_course_codes_from_main_page(academic_year):
        """Fetch the HTML of the main DTU course archive page for a given academic year."""
        # An academic year is for example '2024-2025'
        url = f"https://kurser.dtu.dk/archive/{academic_year}"
        response = requests.get(url, timeout=10, headers={"Accept-Language": "en"})
        response.raise_for_status()
        page_source = response.text
        # Now parse the page source to obtain the course codes
        split_at = "</strong>"
        last_page_source_table = page_source.split(split_at)[-1]
        soup = BeautifulSoup(last_page_source_table, 'html.parser')
        course_codes = []
        table = soup.find('table', class_='table')
        if isinstance(table, Tag):
            for a_tag in table.find_all('a'):
                if isinstance(a_tag, Tag):
                    code = a_tag.text.strip()
                    course_codes.append(code)
        return course_codes

    @staticmethod
    def _scrape_course_code_subpages(academic_year, course_codes):
        """Fetch the HTML for each course code's subpage within an academic year."""
        course_number_and_names = {}
        for code in course_codes:
            url = f"https://kurser.dtu.dk/archive/{academic_year}/coursecode/{code}"
            response = requests.get(url, timeout=10, headers={"Accept-Language": "en"})
            subpage_page_sources = response.text
            # Now parse out each course for the course code (e.g. all 01xxx courses for course code '01')
            soup = BeautifulSoup(subpage_page_sources, 'html.parser')
            table = soup.find('table', class_='table')
            if isinstance(table, Tag):
                rows = table.find_all('tr')[1:]  # Skip header
                for row in rows:
                    if isinstance(row, Tag):
                        columns = row.find_all('td')
                        if len(columns) == 2:
                            course_number = columns[0].text.strip()
                            course_name = columns[1].text.strip()
                            course_number_and_names[course_number] = course_name
        return course_number_and_names


#%%
if __name__ == "__main__":
    ArchiveScraper.quick_test_scrape_for_debugging_please_ignore()