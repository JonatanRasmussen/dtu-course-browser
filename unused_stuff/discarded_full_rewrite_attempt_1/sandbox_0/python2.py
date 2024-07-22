# Importing the necessary modules
import json
from bs4 import BeautifulSoup

# Function to read JSON file
def read_json_file(file_path):
    try:
        with open(file_path, 'r') as f:
            data = json.load(f)
        return data
    except FileNotFoundError:
        return {'error': 'File not found'}
    except json.JSONDecodeError:
        return {'error': 'Error decoding JSON'}

# Function to get the course ID
def get_course_id(soup):
    h2 = soup.find('h2')
    if h2:
        course_title = h2.text.strip()
        course_id, _, _ = course_title.partition(' ')
        return course_id
    return "Course ID not found"

# Function to get the course name
def get_course_name(soup):
    h2 = soup.find('h2')
    if h2:
        course_title = h2.text.strip()
        _, _, rest = course_title.partition(' ')
        course_name, _, _ = rest.partition(',')
        return course_name.strip()
    return "Course name not found"

# Function to get the exam period
def get_exam_period(soup):
    h2 = soup.find('h2')
    if h2:
        exam_title = h2.text.strip()
        _, _, rest = exam_title.partition(' ')
        _, _, exam_period = rest.partition(',')
        return exam_period.strip()
    return "Exam period not found"

# Revised functions to extract specific data based on the new BeautifulSoup object
def get_total_enrolled(soup):
    table1 = soup.find_all('table')[0]
    for row in table1.find_all('tr'):
        cols = row.find_all('td')
        if len(cols) == 2:
            key = cols[0].text.strip()
            value = cols[1].text.strip()
            if key == 'Antal tilmeldte':
                return value

def get_total_attended(soup):
    table1 = soup.find_all('table')[0]
    for row in table1.find_all('tr'):
        cols = row.find_all('td')
        if len(cols) == 2:
            key = cols[0].text.strip()
            value = cols[1].text.strip()
            if key == 'Fremmødte':
                return value

def get_total_passed(soup):
    table1 = soup.find_all('table')[0]
    for row in table1.find_all('tr'):
        cols = row.find_all('td')
        if len(cols) == 2:
            key = cols[0].text.strip()
            value = cols[1].text.strip()
            if key == 'Antal bestået':
                value, _ = value.split('(')
                return value.strip()

def get_exam_average(soup):
    table1 = soup.find_all('table')[0]
    for row in table1.find_all('tr'):
        cols = row.find_all('td')
        if len(cols) == 2:
            key = cols[0].text.strip()
            value = cols[1].text.strip()
            if key == 'Eksamensgennemsnit':
                return value.split(' ')[0]

def get_other_versions(soup):
    table1 = soup.find_all('table')[0]
    for row in table1.find_all('tr'):
        cols = row.find_all('td')
        if len(cols) == 2:
            key = cols[0].text.strip()
            value = cols[1].text.strip()
            if key == 'Andre versioner':
                return value.split('\n')

def get_grade_distribution(soup):
    grade_distribution = {}
    # Find the table containing grade distribution
    table = soup.find_all('table')[1]
    for row in table.find_all('tr')[1:]:  # skip the header row
        cols = row.find_all('td')
        if len(cols) >= 3:
            grade = cols[0].text.strip()
            count = cols[1].text.strip()
            grade_distribution[grade] = int(count)
    return grade_distribution

def get_updated_on(soup):
    # Find the div containing update information
    div_tag = soup.find('div', {'class': 'contentFooter'})
    if div_tag:
        update_info = div_tag.text.strip().split('den')[-1].strip()
        return update_info
    return "Update information not found"

def is_404_page(html_content):
    soup = BeautifulSoup(html_content, 'html.parser')
    header = soup.find('div', {'id': 'header'})
    content = soup.find('div', {'id': 'content'})

    # Check if header and content exist and contain specific text
    if header and content:
        if "Server Error" in header.text and "404 - File or directory not found." in content.text:
            return True
    return False

def is_valid_course_page(html_content):
    soup = BeautifulSoup(html_content, 'html.parser')

    # Check for the presence of an <h1> tag with text "Karakterfordeling"
    h1_tag = soup.find('h1')
    if not h1_tag or 'Karakterfordeling' not in h1_tag.text:
        return False

    # Check for the presence of an <h2> tag
    h2_tag = soup.find('h2')
    if not h2_tag:
        return False

    # Check for the presence of two <table> tags
    tables = soup.find_all('table')
    if len(tables) < 2:
        return False

    # Check for a div with class "contentFooter"
    content_footer = soup.find('div', {'class': 'contentFooter'})
    if not content_footer:
        return False

    return True

# Testing the new functions
def get_grade_data(course, term):
    # Reading the JSON file
    json_file = f"{term}_grades.json"  # Replace with your JSON file path
    json_dict = read_json_file(json_file)

    # Extracting the HTML content for the course "01025"
    grade_html = json_dict.get(course, "")
    if is_404_page(grade_html):
        return {"e404": grade_html}
    elif is_valid_course_page(grade_html):
        # Parsing the HTML content with BeautifulSoup
        juicy_soup = BeautifulSoup(grade_html, 'html.parser')
        return {"course_id": get_course_id(juicy_soup),
                "course_name": get_course_name(juicy_soup),
                "exam_period": get_exam_period(juicy_soup),
                "total_enrolled": get_total_enrolled(juicy_soup),
                "total_attended": get_total_attended(juicy_soup),
                "total_passed": get_total_passed(juicy_soup),
                "exam_average": get_exam_average(juicy_soup),
                "other_versions": get_other_versions(juicy_soup),
                "grade_distribution": get_grade_distribution(juicy_soup),
                "updated_on": get_updated_on(juicy_soup),
                }
    else:
        print(f"Error, html for {term}{course} was of an unexpected format.")
        return {"unrecognized_html": grade_html}

print(get_grade_data("01025", "E17"))
print(get_grade_data("01005", "E17"))
print(get_grade_data("TEST", "E17"))
print(get_grade_data("", "E17"))