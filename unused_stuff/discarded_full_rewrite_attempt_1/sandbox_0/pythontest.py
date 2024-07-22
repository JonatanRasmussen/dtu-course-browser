import json
from bs4 import BeautifulSoup

def extract_course_data(course_id, html_dict):
    course_html = html_dict.get(course_id, '')
    if not course_html:
        return {'error': 'Course ID not found'}

    soup = BeautifulSoup(course_html, 'html.parser')
    data = {}

    # Extract general statistics
    h2 = soup.find('h2')
    if h2:
        data['Course Title'] = h2.text.strip()

    table1 = soup.find_all('table')[0]
    for row in table1.find_all('tr'):
        cols = row.find_all('td')
        if len(cols) == 2:
            key = cols[0].text.strip()
            value = cols[1].text.strip()
            if key == 'Antal bestået':
                value, percentages = value.split('(')
                data[key] = {'Value': value.strip(), 'Percentages': ' '.join(percentages.strip(')').split())}
            else:
                data[key] = value

    # Extract grade distribution
    grade_distribution = {}
    table2 = soup.find_all('table')[1]
    for row in table2.find_all('tr')[1:]:  # skip the header row
        cols = row.find_all('td')
        if len(cols) >= 3:
            grade = cols[0].text.strip()
            count = cols[1].text.strip()
            percentages = cols[2].text.strip('()').strip().replace('(', '').replace(')', '')
            grade_distribution[grade] = f"{count} students ({percentages})"
        elif len(cols) == 2:  # Handle cases where the percentage might be missing
            grade = cols[0].text.strip()
            count = cols[1].text.strip()
            grade_distribution[grade] = f"{count} students"

    data['Grade Distribution'] = grade_distribution

    # Extract additional information
    footer = soup.find('div', {'class': 'contentFooter'})
    if footer:
        update_info = footer.text.strip().split('den')[-1].strip()
        data['Updated on'] = update_info

    return data

def modify_extracted_data(extracted_data):
    # Initialize the modified data dictionary
    modified_data = {}

    # Extract and modify the Course Title
    course_title = extracted_data.get('Course Title', '')
    course_id, _, rest = course_title.partition(' ')
    course_name, _, exam_period = rest.partition(',')
    modified_data['Course ID'] = course_id
    modified_data['Course Name'] = course_name.strip()
    modified_data['Exam Period'] = exam_period.strip()

    # Copy 'Antal tilmeldte' and 'Fremmødte' to the modified data
    modified_data['Total Enrolled'] = extracted_data.get('Antal tilmeldte', '')
    modified_data['Total Attended'] = extracted_data.get('Fremmødte', '')

    # Modify 'Antal bestået'
    antal_bestaet = extracted_data.get('Antal bestået', {}).get('Value', '')
    modified_data['Total Passed'] = antal_bestaet

    # Modify 'Eksamensgennemsnit'
    eksamensgennemsnit = extracted_data.get('Eksamensgennemsnit', '').split(' ')[0]
    modified_data['Exam Average'] = eksamensgennemsnit

    # Convert 'Andre versioner' to list
    andre_versioner = extracted_data.get('Andre versioner', '').split('\n')
    modified_data['Other Versions'] = andre_versioner

    # Flatten out the Grade Distribution
    grade_distribution = extracted_data.get('Grade Distribution', {})
    flattened_grade_distribution = {}
    for grade, value in grade_distribution.items():
        if grade == 'Karakter':
            flattened_grade_distribution['Grade'] = 'Number of Students'
        else:
            flattened_grade_distribution[grade] = int(value.split(' ')[0])
    modified_data['Grade Distribution'] = flattened_grade_distribution

    # Copy 'Updated on' to the modified data
    modified_data['Updated on'] = extracted_data.get('Updated on', '')

    return modified_data


def read_json_file(file_path):
    try:
        with open(file_path, 'r') as f:
            data = json.load(f)
        return data
    except FileNotFoundError:
        print(f"File {file_path} not found.")
        return None
    except json.JSONDecodeError:
        print(f"Error decoding JSON in {file_path}")
        return None

# Example usage
json_file = "E17_grades.json"  # Replace with your JSON file path
json_dict = read_json_file(json_file)

# Test the function with the sample HTML data
raw_data = extract_course_data("01025", json_dict)

# Modify the extracted data
modded_data = modify_extracted_data(raw_data)

print("Modified data:")
print(modded_data)
