#%%

# Imports
# Helper functions and global constants
from utils import Utils
from website.global_constants.file_name_consts import FileNameConsts
from website.global_constants.config import Config


def scrape_course_numbers():
    """Create and save a dict of all DTU course numbers and their names."""

    def transform_date(date_str):
        # Replace '-' with '%2F'
        date_str = date_str.replace('-', '%2F')
        # Remove '/'
        date_str = date_str.replace('/', '')
        return date_str

    # The following url contains a list of all DTU courses
    print('Beginning the course number scrape...')
    driver = Utils.launch_selenium()
    years = transform_date(Config.course_years)
    url = "https://kurser.dtu.dk/search?CourseCode=&SearchKeyword=&Department=1&Department=10&Department=12&Department=13&Department=22&Department=23&Department=24&Department=25&Department=26&Department=27&Department=28&Department=29&Department=30&Department=33&Department=34&Department=36&Department=38&Department=41&Department=42&Department=46&Department=47&Department=59&Department=IHK&Department=83&CourseType=&TeachingLanguage=&Volume="+years
    html_raw = Utils.access_url_via_selenium(url, driver)

    # Initialize dictionary of all course names with course number as key
    course_dictionary = {}

    # In html_raw, each course starts with the following string: <a href="/course/01017">01017 - Discrete Mathematics</a><br />
    # Therefore, we are interested in finding '<a href="/course/' and extracting whatever comes after; by doing this we can find all the courses
    chopped_up_html = html_raw.split(' <a href="/course/')
    for i in range (1, len(chopped_up_html)):

        # Course number (the 5 characters immediately following <a href="/course/)
        html_snippet = chopped_up_html[i]
        course_number = html_snippet [0:5]

        # Course name (start of name is always 15 characters in, and end of name is '</a><br')
        html_snippet_first_half = html_snippet.split('</a><br')[0]
        course_name = html_snippet_first_half[15:len(html_snippet_first_half)]

        # Sometimes, the 5 characters immediately following <a href="/course/) is a yearly interval such as 2022-2023.
        # For example: <a href="/course/2022-2023/01005">01005 - Mathematics 1</a><br />
        # In that case (i.e. if 5th character is a '-'), the course number and name can be found 10 characters further into the string:
        if course_number[4] == '-':
            course_number = html_snippet [10:15]
            course_name = html_snippet_first_half[25:len(html_snippet_first_half)]

        # Add the name of the course to dictionary with course number as key
        course_dictionary[course_number] = course_name

    # Print that program is finished and give a sample output as test control
    print('Program finished - Course numbers scraped: '+str(len(course_dictionary)))
    print(f"Sample output: {course_number}: {course_dictionary[course_number]}")

    # Save dictionary as JSON file
    file_name = FileNameConsts.course_number_json
    Utils.save_dct_as_json(file_name, course_dictionary)


#%%
if __name__ == "__main__":

    scrape_course_numbers()