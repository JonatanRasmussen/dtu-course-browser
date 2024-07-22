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

def find_course_name(soup):
    h2_tag = soup.find('h2')
    if h2_tag:
        text = h2_tag.text.strip()
        prefix = "Resultater : "
        if text.startswith(prefix):
            course_info = text[len(prefix):]
            course_name = course_info.rsplit(" ", 1)
            return course_name
    return "Course name not found"

def find_term(soup):
    h2_tag = soup.find('h2')
    if h2_tag:
        text = h2_tag.text.strip()
        prefix = "Resultater : "
        if text.startswith(prefix):
            course_info = text[len(prefix):]
            term = course_info.rsplit(" ", 1)
            return term
    return "Term not found"

def find_could_respond_stat(soup):
    label = soup.find(string="kunne besvare dette evalueringsskema")
    if label:
        label_parent = label.find_parent()
        if label_parent:
            return label_parent.find_previous_sibling().text.strip()
    return "Statistik for 'kunne besvare' not found"

def find_did_respond_stat(soup):
    label = soup.find(string="har besvaret dette evalueringsskema")
    if label:
        label_parent = label.find_parent()
        if label_parent:
            return label_parent.find_previous_sibling().text.strip()
    return "Statistik for 'har besvaret' not found"

def find_did_not_respond_stat(soup):
    label = soup.find(string="har tilkendegivet ikke at have fulgt kurset")
    if label:
        label_parent = label.find_parent()
        if label_parent:
            return label_parent.find_previous_sibling().text.strip()
    return "Statistik for 'har tilkendegivet' not found"

def extract_survey_results_updated(soup):
    results = {}
    question_headers = soup.find_all("div", class_="CourseSchemaResultHeader grid_6 clearmarg")

    for header in question_headers:
        question_number = header.find("div", class_="FinalEvaluation_Result_QuestionPositionColumn grid_1 clearright").text.strip()
        question_text = header.find("div", class_="FinalEvaluation_QuestionText grid_5 clearleft").text.strip()
        question_key = f"{question_number} - {question_text}"

        results[question_key] = []

        row_containers = header.find_next_siblings("div", class_="RowWrapper")

        for row in row_containers:
            opinion_text = row.find("div", class_="FinalEvaluation_Result_OptionColumn grid_1 clearmarg").text.strip()
            answer_count = row.find("div", class_="Answer_Result_Background").find("span").text.strip()

            # Updated code to find the answer_percentage
            answer_percentage_element = row.find("span", class_="FinalEvaluation_Result_AnswerPercentageSpan")
            answer_percentage = answer_percentage_element.next_sibling if answer_percentage_element else None

            if answer_percentage:
                answer_percentage = answer_percentage.strip()

            results[question_key].append({
                'Opinion': opinion_text,
                'Count': answer_count,
                'Percentage': answer_percentage
            })

    return results

# Modify the function to format the question numbers as Q1.1, Q1.2, etc.
def transform_survey_results(input_dict):
    transformed_dict = {}
    for question, responses in input_dict.items():
        # Shorten the question string to only include the question number
        q_number = question.split(" ")[0]
        q_number = "Q" + q_number  # Keep the '.' in the question number

        # Initialize an empty dictionary for the current question
        transformed_dict[q_number] = {}
        for response in responses:
            # Add the count of each opinion to the dictionary
            opinion = response['Opinion']
            count = int(response['Count'])
            transformed_dict[q_number][opinion] = count
    return transformed_dict

def is_404_page(eval_html):
    #TO DO: Don't let 404 page be blank!
    if len(eval_html) == 0:
        return True
    return False

def is_valid_course_page(eval_html):
    if ("Statistik" in eval_html) and ("kunne besvare dette evalueringsskema" in eval_html):
        return True
    return False

# Testing the new functions
def get_eval_data(course, term):
    # Reading the JSON file
    json_file = f"{term}_evaluations.json"  # Replace with your JSON file path
    json_dict = read_json_file(json_file)

    # Extracting the HTML content for the course "01025"
    eval_html = json_dict.get(course, "")
    if is_404_page(eval_html):
        return {"e404": eval_html}
    elif is_valid_course_page(eval_html):
        # Parsing the HTML content with BeautifulSoup
        juicy_soup = BeautifulSoup(eval_html, 'html.parser')
        survey_result_dct = extract_survey_results_updated(juicy_soup)
        return {"Course Name": find_course_name(juicy_soup),
                "Term": find_term(juicy_soup),
                "Could Respond": find_could_respond_stat(juicy_soup),
                "Did Respond": find_did_respond_stat(juicy_soup),
                "Did Not Respond": find_did_not_respond_stat(juicy_soup),
                "Survey Results": transform_survey_results(survey_result_dct),
                }
    else:
        print(f"Error, html for {term}{course} was of an unexpected format.")
        return {"unrecognized_html": eval_html}

print(get_eval_data("30857", "F23"))
print(get_eval_data("02402", "F23"))
print(get_eval_data("TEST", "F23"))


