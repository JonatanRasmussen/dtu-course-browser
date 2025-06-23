import requests
from bs4 import BeautifulSoup, Tag

from utils import Utils
from website.global_constants.file_name_consts import FileNameConsts
from website.global_constants.dtu_consts import DtuConsts
from website.global_constants.config import Config


def scrape_archive(course_semesters):
    """Scrape archived course data for a given set of semesters"""

    def fetch_main_page(academic_year):
        """Fetch the HTML of the main DTU course archive page for a given academic year."""
        # An academic year is for example '2024-2025'
        url = f"https://kurser.dtu.dk/archive/{academic_year}"
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        return response.text

    def parse_course_codes(page_source):
        """Parse the HTML of the main archive page to extract a list of course codes."""
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

    def fetch_course_subpages(academic_year, course_codes):
        """Fetch the HTML for each course code's subpage within an academic year."""
        subpage_page_sources = []
        for code in course_codes:
            url = f"https://kurser.dtu.dk/archive/{academic_year}/coursecode/{code}"
            response = requests.get(url, timeout=10, headers={"Accept-Language": "en"})
            subpage_page_sources.append(response.text)
        return subpage_page_sources

    def parse_course_code_subpage(course_code_page_sources):
        """Parse course code subpages to extract course numbers and their corresponding names."""
        courses = {}
        for page_source in course_code_page_sources:
            soup = BeautifulSoup(page_source, 'html.parser')
            table = soup.find('table', class_='table')
            if isinstance(table, Tag):
                rows = table.find_all('tr')[1:]  # Skip header
                for row in rows:
                    if isinstance(row, Tag):
                        columns = row.find_all('td')
                        if len(columns) == 2:
                            course_number = columns[0].text.strip()
                            course_name = columns[1].text.strip()
                            courses[course_number] = course_name
        return courses


#%% Start of main script

    # Initialize dictionary that will contain all course data
    course_numbers_by_year = {}
    # Get list of academic years to be scraped
    academic_years = Utils.extract_unique_year_ranges(course_semesters)
    # Begin the webscrape and notify the user
    print(f'Scraping course archive for academic years {academic_years[0]} to {academic_years[-1]}...')
    # Loop through all academic years
    for academic_year in academic_years:
        # Fetch the main archive page containing links to all course codes for the year
        page_source = fetch_main_page(academic_year)
        # Parse the main page to get a list of all course codes (e.g., '01', '02', '10')
        course_codes = parse_course_codes(page_source)
        # Fetch the subpage for each course code, which lists all courses under that code
        course_code_page_sources = fetch_course_subpages(academic_year, course_codes)
        # Parse the subpages to get the final mapping of course numbers to course names
        course_number_and_names = parse_course_code_subpage(course_code_page_sources)
        # Add the scraped courses for the current year to the main dictionary
        course_numbers_by_year[academic_year] = course_number_and_names
        # Print current academic year to console so user can track the progress
        print(f'Finished scraping academic year {academic_year} ({len(course_number_and_names)} courses found)')
    # Save all scraped courses as a JSON file
    file_name = FileNameConsts.archived_courses_json
    Utils.save_dct_as_json(file_name, course_numbers_by_year)


#%%
if __name__ == "__main__":
    scrape_archive(Config.course_semesters)