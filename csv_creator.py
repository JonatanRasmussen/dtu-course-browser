#%%

# Imports
import pandas as pd
import json
from pandas.io.parsers import read_csv
# Helper functions and global constants
from filter_list_creator import filter_dct_to_json
from format_evaluations import format_evaluations
from format_grades import format_grades
from format_info import format_info
from format_study_lines import create_teacher_course_lst
from utils import Utils
from website.global_constants import website_consts
from website.global_constants.config import Config
from website.global_constants.eval_consts import EvalConsts
from website.global_constants.file_name_consts import FileNameConsts
from website.global_constants.grade_consts import GradeConsts
from website.global_constants.info_consts import InfoConsts
from website.global_constants.website_consts import WebsiteConsts


# Initialization
COURSE = FileNameConsts.df_index
NAME = InfoConsts.name_english


def csv_creator(course_numbers, course_names, name_and_path_of_csv, name_and_path_of_pkl, premade_columns):
    """Create and save .csv file with data for all courses"""

    # Open scraped grades df
    grade_df_location = FileNameConsts.grade_df
    grade_df = Utils.load_scraped_df(grade_df_location)
    grade_file_name = FileNameConsts.grade_format

    # Open scraped evals df
    eval_df_location = FileNameConsts.eval_df
    eval_df = Utils.load_scraped_df(eval_df_location)
    eval_file_name = FileNameConsts.eval_format

    # Open scraped info df
    info_df_location = FileNameConsts.info_df
    info_df = Utils.load_scraped_df(info_df_location)
    info_file_name = FileNameConsts.info_format

    # Adding data dicts to the data frame, one course at a time
    semesters = Config.course_semesters
    for i in range (0, len(course_numbers)):
        scraped_grades = grade_df.loc[course_numbers[i]].to_dict()
        scraped_evals = eval_df.loc[course_numbers[i]].to_dict()
        scraped_info = info_df.loc[course_numbers[i]].to_dict()
        formatted_grades_dct = format_grades(scraped_grades, course_numbers[i], semesters, grade_file_name)
        formatted_evals_dct = format_evaluations(scraped_evals, course_numbers[i], semesters, eval_file_name)
        formatted_info_dct = format_info(scraped_info, course_numbers[i], info_file_name)

        data_dct = {**formatted_grades_dct, **formatted_evals_dct, **formatted_info_dct}

        # Create list with column names, this will be the data frame columns
        if i == 0:
            if premade_columns == []:
                column_names = [COURSE] + [NAME] + list(data_dct.keys())
            else:
                column_names = [COURSE] + [NAME] + premade_columns
        # Create a dictionary with one value for each column in the data frame
        df_input = {COURSE: [str(course_numbers[i])], NAME: [str(course_names[i])]}
        for j in range(2, len(column_names)):
            if str(column_names[j]) in data_dct:
                df_input[str(column_names[j])] = [data_dct[column_names[j]]]
            else:
                df_input[str(column_names[j])] = [None]

        # On first loop, create df, then add a new row to data frame on each loop
        if i == 0:
            df = pd.DataFrame(data = df_input)
        else:
            new_df_row = pd.DataFrame(data = df_input)
            df = pd.concat([df, new_df_row], ignore_index=True)

        #df = df.append(new_csv_row, ignore_index=True)

        # Display progress to user
        Utils.display_progress(i, course_numbers, name_and_path_of_csv, 50)

    # Set course ID as df index
    print("Success! Setting course ID as df index...")
    df = df.copy() # df is copied to 'fix fragmentation', which prevents a pandas PerformanceWarning
    df.set_index(COURSE, inplace=True, drop=False)
    print(df)

    # Append columns containing each responsibles' course list
    print('Finishing the csv...')
    if (InfoConsts.main_responsible_name.key_df) in premade_columns or premade_columns == []:
        df = create_teacher_course_lst(df, course_numbers)

    # Save data frame to CSV
    print()
    print(f'csv file {name_and_path_of_csv} has been succesfully created')
    df.to_csv(name_and_path_of_csv, index = False, header=True)
    print(df)

    # Save CSV file as pickle and also save specific columns as json dct
    read_csv_to_pickle(name_and_path_of_csv, name_and_path_of_pkl)
    if premade_columns != []:
        write_csv_columns_to_json(name_and_path_of_csv)
    else:
        print()
        filter_dct_to_json()
        print()



def read_csv_to_pickle(name_and_path_of_csv, name_and_path_of_pkl):
    """Turn csv file into dataframe pickle with help from Pandas"""
    # This pickle is the database that gets accessed whenever any specific course page is accessed via the website.

    # Load in data frame from csv
    print("Loading csv with Pandas...")
    df = pd.read_csv(name_and_path_of_csv, dtype={'COURSE': str}, low_memory=False)

    # Set course ID as df index
    print("Success! Setting course ID as df index...")
    df.set_index(COURSE, inplace=True, drop=False)

    # Save data frame to pickle file
    print("Success! Saving data frame to pickle format...")
    df.to_pickle(name_and_path_of_pkl)
    #df_extra.to_pickle("static/database/course_df_extra.pkl")



def write_csv_columns_to_json(name_and_path_of_csv):
    """Turn csv columns into dictionary files stored as jsons"""
    # This jsons are the database that gets accessed whenever the "discovery" page (home page) is loaded.

    def rename_dct_value(dct, column):
        """Loop through dct and rename certain values so they fit the cards on the home page"""
        if column == InfoConsts.course_type.key_df:
            for key in dct:
                if dct[key] == InfoConsts.bsc + InfoConsts.separator_plus + InfoConsts.msc:
                    dct[key] = InfoConsts.bsc+"/"+InfoConsts.msc
                elif dct[key] == InfoConsts.deltidsmaster:
                    dct[key] = InfoConsts.msc
                elif dct[key] == InfoConsts.deltidsdiplom:
                    dct[key] = InfoConsts.beng
        elif column == InfoConsts.semester_period.key_df:
            for key in dct:
                if dct[key] == "Autumn":
                    dct[key] = WebsiteConsts.shortened_autumn
                elif dct[key] == InfoConsts.not_yet_assigned_value or dct[key] == InfoConsts.unknown_value:
                    dct[key] = WebsiteConsts.no_data
                elif dct[key] == "January" or dct[key] == "June" or dct[key] == "July" or dct[key] == "August" or dct[key] == "Spring":
                    pass
                else:
                    dct[key] = WebsiteConsts.multiple_timeslots
        elif column == InfoConsts.time_of_week.key_df:
            for key in dct: # Do not touch these, it will break stuff
                if dct[key] == "E1A (Autumn, Mon 8-12)" or dct[key] == "F1A (Spring, Mon 8-12)":
                    dct[key] = "Mon_8_12" # Do not touch these, it will break stuff
                elif dct[key] == "E1B (Autumn, Thurs 13-17)" or dct[key] == "F1B (Spring, Thurs 13-17)":
                    dct[key] = "Thurs_13_17"
                elif dct[key] == "E2A (Autumn, Mon 13-17)" or dct[key] == "F2A (Spring, Mon 13-17)":
                    dct[key] = "Mon_13_17"
                elif dct[key] == "E2B (Autumn, Thurs 8-12)" or dct[key] == "F2B (Spring, Thurs 8-12)":
                    dct[key] = "Thurs_8_12"
                elif dct[key] == "E3A (Autumn, Tues 8-12)" or dct[key] == "F3A (Spring, Tues 8-12)":
                    dct[key] = "Tues_8_12"
                elif dct[key] == "E3B (Autumn, Fri 13-17)" or dct[key] == "F3B (Spring, Fri 13-17)":
                    dct[key] = "Fri_13_17"
                elif dct[key] == "E4A (Autumn, Tues 13-17)" or dct[key] == "F4A (Spring, Tues 13-17)":
                    dct[key] = "Tues_13_17"
                elif dct[key] == "E4B (Autumn, Fri 8-12)" or dct[key] == "F4B (Spring, Fri 8-12)":
                    dct[key] = "Fri_8_12"
                elif dct[key] == "E5A (Autumn, Wed 8-12)" or dct[key] == "F5A (Spring, Wed 8-12)":
                    dct[key] = "Wed_8_12"
                elif dct[key] == "E5B (Autumn, Wed 13-17)" or dct[key] == "F5B (Spring, Wed 13-17)":
                    dct[key] = "Wed_13_17"
                elif dct[key] == "E7 (Autumn, Tues 18-22)" or dct[key] == "F7 (Spring, Tues 18-22)":
                    dct[key] = "Tues_18_22"
                elif dct[key] == "E1A (Autumn, Mon 8-12)<br />E1B (Autumn, Thurs 13-17)" or dct[key] == "F1A (Spring, Mon 8-12)<br />F1B (Spring, Thurs 13-17)":
                    dct[key] = "Multi_Mon_8_12_Thurs_13_17"
                elif dct[key] == "E2A (Autumn, Mon 13-17)<br />E2B (Autumn, Thurs 8-12)" or dct[key] == "F2A (Spring, Mon 13-17)<br />F2B (Spring, Thurs 8-12)":
                    dct[key] = "Multi_Mon_13_17_Thurs_8_12"
                elif dct[key] == "E3A (Autumn, Tues 8-12)<br />E3B (Autumn, Fri 13-17)" or dct[key] == "F3A (Spring, Tues 8-12)<br />F3B (Spring, Fri 13-17)":
                    dct[key] = "Multi_Tues_8_12_Fri_13_17"
                elif dct[key] == "E4A (Autumn, Tues 13-17)<br />E4B (Autumn, Fri 8-12)" or dct[key] == "F4A (Spring, Tues 13-17)<br />F4B (Spring, Fri 8-12)":
                    dct[key] = "Multi_Tues_13_17_Fri_8_12"
                elif dct[key] == "E5A (Autumn, Wed 8-12)<br />E5B (Autumn, Wed 13-17)" or dct[key] == "F5A (Spring, Wed 8-12)<br />F5B (Spring, Wed 13-17)":
                    dct[key] = "Multi_Wed_8_12_Wed_13_17"
                else:
                    dct[key] = WebsiteConsts.multiple_unknowns
        elif column == GradeConsts.grade_average or column == EvalConsts.workload_average_score or column == EvalConsts.rating_average_score or column == EvalConsts.learning_average_score or column == EvalConsts.motivation_average_score or column == EvalConsts.feedback_average_score:
            for key in dct:
                if dct[key] == GradeConsts.pass_fail:
                    dct[key] = WebsiteConsts.shortened_pass_fail
                elif dct[key] == GradeConsts.grade_none:
                    dct[key] = WebsiteConsts.shortened_no_grades
                elif dct[key] == EvalConsts.no_evaluations:
                    dct[key] = WebsiteConsts.shortened_no_evaluations
                else:
                    try:
                        dct[key] = round(float(dct[key]), 1)
                    except:
                        print(f"Warning: {dct[key]} was expected to be numeric, yet it could not be rounded!")
        elif column == GradeConsts.percent_failed:
            for key in dct:
                if dct[key] == GradeConsts.grade_none:
                    dct[key] = "0"
                else:
                    try:
                        if float(dct[key]) < 10:
                            dct[key] = round(float(dct[key]), 1)
                        else:
                            dct[key] = int(round(float(dct[key]), 0))
                    except:
                        print(f"Warning: {dct[key]} was expected to be numeric, yet it could not be rounded!")
        elif column == InfoConsts.exam_type.key_df:
            for key in dct:
                if dct[key] == InfoConsts.exam_both:
                    dct[key] = WebsiteConsts.shortened_written_oral
                elif (dct[key] == InfoConsts.exam_none) or (dct[key] == InfoConsts.unknown_value):
                    dct[key] = WebsiteConsts.exam_project
        return dct


    def save_dct_as_json(df, column, json_name):
        """Load a column from csv as dictionary and save it as json"""

        def turn_to_float(item):
            if (column == GradeConsts.grade_average) or (column == GradeConsts.percent_failed) or (column == EvalConsts.workload_average_score) or (column == EvalConsts.rating_average_score) or (column == EvalConsts.learning_average_score) or (column == EvalConsts.motivation_average_score) or (column == EvalConsts.feedback_average_score):
                if isinstance(item, str):
                    return -0.1
            elif (column == InfoConsts.main_responsible_pic.key_df):
                return str(item)
            return item

        dct = df.to_dict()[column]
        dct_data = rename_dct_value(dct, column)
        sorted_dct = dict(sorted(dct_data.items(), key=lambda item: turn_to_float(item[1]))) # Be careful, this line will do absolutely nothing WITHOUT RAISING A WARNING if dct_data contains a mix of strings and numbers
        path_and_file_name = FileNameConsts.path_of_pkl + json_name + '.json'
        with open(path_and_file_name, 'w') as fp:
            json.dump(sorted_dct, fp)
        print(f"The dictionary {json_name}.json has been saved...")


    # Load in data frame from csv
    df = pd.read_csv(name_and_path_of_csv, dtype={'COURSE': str}, low_memory=False)

    # Save course json before setting course column as df index
    save_dct_as_json(df, FileNameConsts.df_index, WebsiteConsts.json_number)

    # Set index
    df = df.set_index(COURSE)

    # All the json files that must be created
    save_dct_as_json(df, InfoConsts.name_english, WebsiteConsts.json_name_english)
    save_dct_as_json(df, InfoConsts.ects_points.key_df, WebsiteConsts.json_course_ects)
    save_dct_as_json(df, InfoConsts.course_type.key_df, WebsiteConsts.json_course_type)
    save_dct_as_json(df, InfoConsts.language.key_df, WebsiteConsts.json_course_language)
    save_dct_as_json(df, InfoConsts.semester_period.key_df, WebsiteConsts.json_course_season)
    save_dct_as_json(df, InfoConsts.time_of_week.key_df, WebsiteConsts.json_course_schedule)
    save_dct_as_json(df, GradeConsts.students_per_semester, WebsiteConsts.json_course_signups)
    save_dct_as_json(df, GradeConsts.grade_average, WebsiteConsts.json_course_grade)
    save_dct_as_json(df, GradeConsts.percent_failed, WebsiteConsts.json_course_fail)
    save_dct_as_json(df, InfoConsts.exam_type.key_df, WebsiteConsts.json_course_exam)
    save_dct_as_json(df, EvalConsts.workload_average_score, WebsiteConsts.json_course_workload)
    save_dct_as_json(df, EvalConsts.rating_average_score, WebsiteConsts.json_course_rating)
    save_dct_as_json(df, EvalConsts.workload_tier, WebsiteConsts.json_course_workload_tier)
    save_dct_as_json(df, EvalConsts.rating_tier, WebsiteConsts.json_course_rating_tier)
    save_dct_as_json(df, EvalConsts.motivation_votes, WebsiteConsts.json_course_votes)
    save_dct_as_json(df, InfoConsts.main_responsible_pic.key_df, WebsiteConsts.json_course_responsible)
    save_dct_as_json(df, EvalConsts.learning_average_score, WebsiteConsts.json_course_eval_learning)
    save_dct_as_json(df, EvalConsts.motivation_average_score, WebsiteConsts.json_course_eval_motivation)
    save_dct_as_json(df, EvalConsts.feedback_average_score, WebsiteConsts.json_course_eval_feedback)

def csv_creator_main():
    """ Clean, format and parse the scraped_data into a csv used by my website """
    # Variables and initialization
    COURSE_NUMBERS = Utils.get_course_numbers()
    COURSE_NAMES = Utils.get_course_names()
    #COURSE_NUMBERS = ['02402']

    # Define columns in the smaller of the two CSV-files
    BASIC_COLUMNS = [InfoConsts.danish_name.key_df, InfoConsts.language.key_df, InfoConsts.ects_points.key_df, InfoConsts.course_type.key_df,
                     GradeConsts.students_per_semester, InfoConsts.semester_period.key_df, InfoConsts.exam_type.key_df,
                     InfoConsts.assignments.key_df, InfoConsts.time_of_week.key_df, InfoConsts.last_updated.key_df]

    GRADE_COLUMNS = [GradeConsts.grade_12, GradeConsts.grade_10, GradeConsts.grade_7, GradeConsts.grade_4, GradeConsts.grade_02,
                     GradeConsts.grade_00, GradeConsts.grade_minus_3, GradeConsts.grade_passed, GradeConsts.grade_failed,
                     GradeConsts.grade_absent, GradeConsts.grade_average, GradeConsts.students_total, GradeConsts.percent_passed,
                     GradeConsts.percent_failed, GradeConsts.percent_absent]

    EVAL_COLUMNS = [EvalConsts.rating_tier, EvalConsts.rating_average_score, EvalConsts.rating_votes,
                    EvalConsts.learning_tier, EvalConsts.learning_average_score, EvalConsts.learning_votes,
                    EvalConsts.motivation_tier, EvalConsts.motivation_average_score, EvalConsts.motivation_votes,
                    EvalConsts.feedback_tier, EvalConsts.feedback_average_score, EvalConsts.feedback_votes,
                    EvalConsts.workload_tier, EvalConsts.workload_average_score, EvalConsts.workload_votes, EvalConsts.workload_4_star, EvalConsts.workload_5_star]

    RESPONSIBLE_COLUMNS =  [InfoConsts.main_responsible_name.key_df, InfoConsts.main_responsible_pic.key_df,
                            InfoConsts.co_responsible_1_name.key_df, InfoConsts.co_responsible_1_pic.key_df,
                            InfoConsts.co_responsible_2_name.key_df, InfoConsts.co_responsible_2_pic.key_df,
                            InfoConsts.co_responsible_3_name.key_df, InfoConsts.co_responsible_3_pic.key_df,
                            InfoConsts.co_responsible_4_name.key_df, InfoConsts.co_responsible_4_pic.key_df]

    CONTENT_COLUMNS =  [InfoConsts.course_description.key_df, InfoConsts.scope_and_form.key_df, (InfoConsts.exam_type.key_df)+'_'+InfoConsts.raw_key,
                        (InfoConsts.exam_aid.key_df)+'_'+InfoConsts.raw_key, (InfoConsts.location.key_df)+'_'+InfoConsts.raw_key, InfoConsts.time_of_week_updated.key_df,
                        InfoConsts.exam_duration.key_df, InfoConsts.home_page.key_df, InfoConsts.learning_objectives.key_df, InfoConsts.course_content.key_df, InfoConsts.remarks.key_df,
                        InfoConsts.recommended_prerequisites.key_df, InfoConsts.mandatory_prerequisites.key_df, InfoConsts.study_lines.key_df, GradeConsts.semesters_total, InfoConsts.institute.key_df]

    SEMESTER_ELEMENTS = [GradeConsts.students_total, GradeConsts.grade_average, GradeConsts.percent_failed,
                         GradeConsts.grade_12, GradeConsts.grade_10, GradeConsts.grade_7, GradeConsts.grade_4, GradeConsts.grade_02, GradeConsts.grade_00, GradeConsts.grade_minus_3,
                         EvalConsts.learning_votes, EvalConsts.workload_average_score, EvalConsts.learning_average_score,
                         EvalConsts.motivation_average_score, EvalConsts.feedback_average_score]

    SEMESTER_COLUMNS = Utils.generate_columns(Config.course_semesters, SEMESTER_ELEMENTS, add_index = False)

    # Create CSV file
    PREMADE_COLUMNS = BASIC_COLUMNS + GRADE_COLUMNS + EVAL_COLUMNS + RESPONSIBLE_COLUMNS + CONTENT_COLUMNS + SEMESTER_COLUMNS # If adding a new column_name, be sure to add it to format info script as well!
    name_and_path_of_csv = FileNameConsts.path_of_csv + FileNameConsts.name_of_csv + ".csv"
    name_and_path_of_pkl = FileNameConsts.path_of_pkl + FileNameConsts.name_of_pkl + ".pkl"
    print("Creating csv file: "+name_and_path_of_csv)
    print()
    csv_creator(COURSE_NUMBERS, COURSE_NAMES, name_and_path_of_csv, name_and_path_of_pkl, PREMADE_COLUMNS)

    # Create extended csv
    PREMADE_COLUMNS = []
    path_name_extended_csv = FileNameConsts.path_of_csv + FileNameConsts.extended_csv_name + ".csv"
    path_name_extended_pkl = FileNameConsts.path_of_pkl + FileNameConsts.extended_pkl_name + ".pkl"
    csv_creator(COURSE_NUMBERS, COURSE_NAMES, path_name_extended_csv, path_name_extended_pkl, PREMADE_COLUMNS)
    print("Creating extended csv file: "+path_name_extended_csv)
    print()

    # Success!
    print("Success! Program will now terminate.")



#%%
if __name__ == "__main__":
    csv_creator_main()