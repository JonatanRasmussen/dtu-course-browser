

class FileNameConsts:
    # General
    scraped_data_folder_name = "scraped_data"
    archived_courses_json = "archived_courses"
    course_number_json = "course_numbers"
    df_index = 'COURSE'
    df_name = 'NAME'
    eval_df = 'scraped_evals'
    grade_df = 'scraped_grades'
    info_df = 'scraped_info'
    eval_format = 'format_evals'
    grade_format = 'format_grades'
    info_format = 'format_info'
    log_folder_name = 'logs'
    scrape_log_name = 'scrape_logs'
    format_log_name = 'format_logs'
    website_log_name = 'website_logs'

    # PythonAnywhere.com top level folder
    pythonanywherecom_top_folder = "dtu_course_project/"

    # CSV
    path_of_csv = "website/static/csv_files/"
    pythonanywherecom_path_of_csv = pythonanywherecom_top_folder + path_of_csv
    name_of_csv = "course_df"
    extended_csv_name = "extended_csv"
    planner_csv = "planner_csv"

    # PKL
    path_of_pkl = "website/static/pandas_df/"
    pythonanywherecom_path_of_pkl = pythonanywherecom_top_folder + path_of_pkl
    name_of_pkl = "course_df"
    extended_pkl_name = "extended_pkl"
    planner_pkl = "planner_pkl"