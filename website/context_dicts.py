

# Imports
import json
# Helper functions and global constants
from website.global_constants.website_consts import WebsiteConsts
from website.global_constants.file_name_consts import FileNameConsts
from website.global_constants.config import Config

def load_course_data_dct_json_file(nested_dct_name):
    """Load json file containing all the data"""
    file_name = WebsiteConsts.json_course_data
    try:
        pythonanywhere_dct_name = FileNameConsts.pythonanywherecom_path_of_pkl + file_name + '.json'
        with open(pythonanywhere_dct_name) as f:
            dct = json.load(f)
        if nested_dct_name in dct:
            return dct[nested_dct_name]
        else:
            return {}
    except FileNotFoundError:
        dct_name = FileNameConsts.path_of_pkl + file_name + '.json'
        try:
            with open(dct_name) as f:
                dct = json.load(f)
            if nested_dct_name in dct:
                return dct[nested_dct_name]
            else:
                return {}
        except: # return empty dict if no file found
            print(f"Error: Dictionary with file name {file_name} was not found in {FileNameConsts.path_of_pkl}")
            return {}

def load_dct_from_json_file(file_name):
    """Load in dictionary from json file"""
    try:
        pythonanywhere_dct_name = FileNameConsts.pythonanywherecom_path_of_pkl + file_name + '.json'
        with open(pythonanywhere_dct_name) as f:
            dct = json.load(f)
        return dct
    except FileNotFoundError:
        try:
            dct_name = FileNameConsts.path_of_pkl + file_name + '.json'
            with open(dct_name) as f:
                dct = json.load(f)
            return dct
        except: # return empty dict if no file found
            print(f"Error: Dictionary with file name {file_name} was not found in {FileNameConsts.path_of_pkl}")
            return {}

def create_filtered_list_from_url_args(url_args):
    filter_dct = get_filter_dct()
    temp_dct = {}
    filers_found = 0
    for value in url_args:
        catagory = url_args[value]
        if (catagory in filter_dct) and (value in filter_dct[catagory]):
            filers_found += 1
            if catagory in temp_dct:
                temp_dct[catagory] += filter_dct[catagory][value]
            else:
                temp_dct[catagory] = filter_dct[catagory][value]
    courses_to_display = set()
    is_first_iteration = True
    for key in temp_dct:
        if is_first_iteration:
            is_first_iteration = False
            courses_to_display = set(temp_dct[key])
        else:
            courses_to_display = courses_to_display.intersection(temp_dct[key])
    return courses_to_display

def turn_set_into_lst_and_sort(set_of_courses_to_display, url_args):

    def get_arranged_lst(arrange_order, course_set, url_args):
        lst = []
        for course in arrange_order:
            if course in course_set:
                lst.append(course)
        if WebsiteConsts.sort_reverse in url_args:
            lst.reverse()
        return lst

    sort_by = WebsiteConsts.sort_by
    sorting_keys_as_dct = WebsiteConsts.json_as_sort_catagory
    sorting_keys = list(sorting_keys_as_dct)
    if (sort_by not in url_args) or (url_args[sort_by] not in sorting_keys):
        # Invalid url args
        arrange_order = list(courses().values())
        #print(f'not in: {arrange_order}')
        return get_arranged_lst(arrange_order, set_of_courses_to_display, url_args)
    else:
        # Valid url args
        sorting_catagory = url_args[sort_by]
        json_file_name = sorting_catagory
        #dct = load_dct_from_json_file(json_file_name)
        dct = load_course_data_dct_json_file(json_file_name)
        arrange_order = list(dct)
        if (sorting_catagory in sorting_keys):
            if (sorting_keys_as_dct[sorting_catagory]): #Boolean, decides if list should be reversed
                arrange_order.reverse()
        else:
            print(f'Alert: {sorting_catagory} not in {sorting_keys}')
        return get_arranged_lst(arrange_order, set_of_courses_to_display, url_args)

def dicts_to_display():
    return {'list_of_dicts': ['Course sample']}

def get_name_of_list(name_of_list):
    return {'list_of_dicts': [name_of_list]}

def course_lists(course_data): # Add dict name to dicts_to_display()
    all_courses = [
        "02105", "02003", "02456", "02476", "34126", "02180", "42500", "88383",
        "63852", "02450", "38106", "02402", "42620", "42893", "02393",
        "62999", "27020", "01001", "34366", "25102", "10605",
    ]

    # Filter courses to only include those that exist in course_data
    filtered_courses = [course_id for course_id in all_courses if course_id in course_data[WebsiteConsts.name]]

    if len(all_courses) != len(filtered_courses):
        missing_courses = [course_id for course_id in all_courses if course_id not in course_data[WebsiteConsts.name]]
        print("Update course sample in context dicts. Missing courses:", missing_courses)

    return {
        'Course sample': filtered_courses
    }
    """ return {
        'Jonatan Rasmussens passed courses: Programming, Data and Network': [
            '02393', '02476', '02561', '02180', '02806', '02161', '34346',
            '34210', '34331', '34333', '34334', '02105', '01017', '02502',
            '34313', '34302', '34229', '34120'
        ],
        'Jonatan Rasmussens passed courses: Polytechnical Foundation': [
            '02402', '01001', '01002', '26021', '10060', '02002', '27020',
            '42620'
        ],
        'Jonatan Rasmussens passed courses: Electives & Other': [
            '63851', '38106', '42009', '10610', '10603', '41011', '41012'
        ]
    } """

def last_updated_dct():
    return {WebsiteConsts.last_updated: Config.website_last_updated,
            WebsiteConsts.current_year: Config.website_current_year}

def data():
    dct = { WebsiteConsts.name: name(),
            WebsiteConsts.ects: ects(),
            WebsiteConsts.course_type: course_type(),
            WebsiteConsts.language: language(),
            WebsiteConsts.season: season(),
            WebsiteConsts.schedule: schedule(),
            WebsiteConsts.signups: signups(),
            WebsiteConsts.grade: grade(),
            WebsiteConsts.fail: fail(),
            WebsiteConsts.exam: exam(),
            WebsiteConsts.workload: workload(),
            WebsiteConsts.rating: rating(),
            WebsiteConsts.workload_tier: workload_tier(),
            WebsiteConsts.rating_tier: rating_tier(),
            WebsiteConsts.votes: votes(),
            WebsiteConsts.responsible: responsible()}
    return dct

def get_filter_dct():
    json_file_name = WebsiteConsts.json_filter_dct
    dct = load_dct_from_json_file(json_file_name)
    return dct

def current_args(url_args):
    filter_dct = get_filter_dct()
    args_without_sort_by = ""
    current_sort_by = ""
    for value in url_args:
        catagory = url_args[value]
        if (catagory in filter_dct) and (value in filter_dct[catagory]):
            if args_without_sort_by == "":
                args_without_sort_by += f"?{value}={catagory}"
            else:
                args_without_sort_by += f"&{value}={catagory}"
        elif value == WebsiteConsts.sort_by:
            current_sort_by = catagory

    return {WebsiteConsts.url_arg_key: args_without_sort_by, WebsiteConsts.sort_by: current_sort_by}

def summary_stats(course_lst):

    def calculate_average(json_dct, decimal_places):
        value_count = 0
        total_value = 0
        average_value = 0
        for course in course_lst:
            if (json_dct[course] != 0) and ((type(json_dct[course]) == int) or (type(json_dct[course]) == float)):
                value_count += 1
                total_value += json_dct[course]
        if value_count != 0:
            average_value = round((total_value / value_count), decimal_places)
            if decimal_places == 0:
                average_value = int(average_value)

        return average_value

    stat_dct = {"rating": calculate_average(rating(), 2),
                "workload": calculate_average(workload(), 2),
                "learning": calculate_average(eval_learning(), 2),
                "motivation": calculate_average(eval_motivation(), 2),
                "feedback": calculate_average(eval_feedback(), 2),
                "grade": calculate_average(grade(), 1),
                "failrate": calculate_average(fail(), 1),
                "signups": calculate_average(signups(), 0)}
    return stat_dct


def courses():
    json_file_name = WebsiteConsts.json_number
    dct = load_dct_from_json_file(json_file_name)
    return dct

def name():
    json_file_name = WebsiteConsts.json_name_english
    #dct = load_dct_from_json_file(json_file_name)
    dct = load_course_data_dct_json_file(json_file_name)
    return dct
    #return {'01005': 'Matematik 1',
    #        '01035': 'Grundlæggende kemi',
    #        '01069': 'Introduktion til indledende matematik og avanceret matematik'}

def ects():
    json_file_name = WebsiteConsts.json_course_ects
    #dct = load_dct_from_json_file(json_file_name)
    dct = load_course_data_dct_json_file(json_file_name)
    return dct

def course_type():
    json_file_name = WebsiteConsts.json_course_type
    #dct = load_dct_from_json_file(json_file_name)
    dct = load_course_data_dct_json_file(json_file_name)
    return dct

def language():
    json_file_name = WebsiteConsts.json_course_language
    #dct = load_dct_from_json_file(json_file_name)
    dct = load_course_data_dct_json_file(json_file_name)
    return dct

def season():
    json_file_name = WebsiteConsts.json_course_season
    #dct = load_dct_from_json_file(json_file_name)
    dct = load_course_data_dct_json_file(json_file_name)
    return dct

def schedule():
    json_file_name = WebsiteConsts.json_course_schedule
    #dct = load_dct_from_json_file(json_file_name)
    dct = load_course_data_dct_json_file(json_file_name)
    return dct

def signups():
    json_file_name = WebsiteConsts.json_course_signups
    #dct = load_dct_from_json_file(json_file_name)
    dct = load_course_data_dct_json_file(json_file_name)
    return dct

def grade():
    json_file_name = WebsiteConsts.json_course_grade
    #dct = load_dct_from_json_file(json_file_name)
    dct = load_course_data_dct_json_file(json_file_name)
    return dct

def fail():
    json_file_name = WebsiteConsts.json_course_fail
    #dct = load_dct_from_json_file(json_file_name)
    dct = load_course_data_dct_json_file(json_file_name)
    return dct

def exam():
    json_file_name = WebsiteConsts.json_course_exam
    #dct = load_dct_from_json_file(json_file_name)
    dct = load_course_data_dct_json_file(json_file_name)
    return dct

def workload():
    json_file_name = WebsiteConsts.json_course_workload
    #dct = load_dct_from_json_file(json_file_name)
    dct = load_course_data_dct_json_file(json_file_name)
    return dct

def rating():
    json_file_name = WebsiteConsts.json_course_rating
    #dct = load_dct_from_json_file(json_file_name)
    dct = load_course_data_dct_json_file(json_file_name)
    return dct

def workload_tier():
    json_file_name = WebsiteConsts.json_course_workload_tier
    #dct = load_dct_from_json_file(json_file_name)
    dct = load_course_data_dct_json_file(json_file_name)
    return dct

def rating_tier():
    json_file_name = WebsiteConsts.json_course_rating_tier
    #dct = load_dct_from_json_file(json_file_name)
    dct = load_course_data_dct_json_file(json_file_name)
    return dct

def votes():
    json_file_name = WebsiteConsts.json_course_votes
    #dct = load_dct_from_json_file(json_file_name)
    dct = load_course_data_dct_json_file(json_file_name)
    return dct

def responsible():
    json_file_name = WebsiteConsts.json_course_responsible
    #dct = load_dct_from_json_file(json_file_name)
    dct = load_course_data_dct_json_file(json_file_name)
    return dct

def eval_learning():
    json_file_name = WebsiteConsts.json_course_eval_learning
    #dct = load_dct_from_json_file(json_file_name)
    dct = load_course_data_dct_json_file(json_file_name)
    return dct

def eval_motivation():
    json_file_name = WebsiteConsts.json_course_eval_motivation
    #dct = load_dct_from_json_file(json_file_name)
    dct = load_course_data_dct_json_file(json_file_name)
    return dct

def eval_feedback():
    json_file_name = WebsiteConsts.json_course_eval_feedback
    #dct = load_dct_from_json_file(json_file_name)
    dct = load_course_data_dct_json_file(json_file_name)
    return dct


def faq_dict():
    faq_dict = {}

    q = "How is the ratings for each course calculated?"
    a = "Bla bla."
    faq_dict["rating_calc_q"] = q
    faq_dict["rating_calc_a"] = a

    q = "How is the workload for each course calculated?"
    a = "Bla bla bla."
    faq_dict["workload_calc_q"] = q
    faq_dict["workload_calc_a"] = a

    return faq_dict