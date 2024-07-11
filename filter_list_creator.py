#%%

# Imports
import json
import pandas as pd
# Helper functions and global constants
from utils import Utils
from website.global_constants.file_name_consts import FileNameConsts
from website.global_constants.info_consts import InfoConsts
from website.global_constants.website_consts import WebsiteConsts


def get_dct_from_df_column(column_name, df):
    """ Given a df and the name of a column in the df that the dct should be sorted by,
        return a dct with each course (as key) and its value in column_name.
        If column_name does not exist in df, return an empty dct """
    if column_name in df:
        dct = df.set_index(FileNameConsts.df_index)[column_name].to_dict()
    else:
        # Raise an error if column_name does not exist as a column in df
        message = f"Filter list creator; {column_name} not found in df!"
        Utils.logger(message, "warning", FileNameConsts.format_log_name)
        dct = {}
    return dct


def sort_dct_by_value(dct):
    """ Sort each key in a dict based on its value"""
    return dict(sorted(dct.items(), key=lambda item: item[1]))


def create_dct_of_column_names(lst_of_column_names, translated_lst_of_column_names, df):
    """ Create a dct containing course lists for each column_name """
    dct_of_column_names = {}
    for column_name in lst_of_column_names:
        # Transpose a df column into a dct with courses as key and sort it by value
        dct = get_dct_from_df_column(column_name, df)
        # For each course in df's column_name, if value == 1, append it to list
        lst_of_courses_with_val_1 = []
        for course in dct.keys():
            if dct[course] == 1:
                lst_of_courses_with_val_1.append(course)
        column_name_translations = dict(zip(lst_of_column_names, translated_lst_of_column_names))
        # Make sure values_df is the same length as values_url, otherwise the translation above will fail
        if len(lst_of_column_names) != len(translated_lst_of_column_names):
            print(f"Error, {len(lst_of_column_names)} != {len(translated_lst_of_column_names)}: Go to info_consts file and ensure that values_df is the same length as values_url. First element: {lst_of_column_names[0]}, {translated_lst_of_column_names[0]}")
        translated_column_name = column_name_translations[column_name]
        dct_of_column_names[translated_column_name] = lst_of_courses_with_val_1
    return dct_of_column_names


def filter_dct_creator():
    """ Create and save a filter dict that will contain a bunch of nested dicts
        Each nested dict covers a filter category, such as "Language" or "Schedule"
        For example, the nested dict for "Language" contains the keys "Danish" and "English"
        The value for each of those keys is a list of all the danish courses and english courses
        To access the list of all courses in english, access filter_dct[Language][English] """

    filter_dct = {}

    # Load in data frame from csv
    name_and_path_of_extended_pkl = FileNameConsts.path_of_pkl + FileNameConsts.extended_pkl_name + ".pkl"
    df = pd.read_pickle(name_and_path_of_extended_pkl)

    # Add nested dicts to filter_dct, one by one
    info_lst = InfoConsts.info_to_format
    for info in info_lst:
        #print(info.values_df)
        if info.values_df != []:
            #print(f"{info.key_url}: {info.values_url}")
            values_df_no_duplicates = list(dict.fromkeys(info.values_df))
            filter_dct[info.key_url] = create_dct_of_column_names(values_df_no_duplicates, info.values_url, df)
    return filter_dct

def filter_dct_to_json():
    """ Create and save dct used for website filter functionality """
    filter_dct = filter_dct_creator()

    # save as JSON
    json_name  = WebsiteConsts.json_filter_dct
    path_and_file_name = FileNameConsts.path_of_pkl + json_name + '.json'
    with open(path_and_file_name, 'w') as fp:
        json.dump(filter_dct, fp)
    print(f"The dictionary {json_name}.json has been saved...")

    """
    # Language lists
    dct_key = FilterConsts.filter_language
    column_name_list = [InfoConsts.language_danish,
                        InfoConsts.language_english]
    filter_dct[dct_key] = create_dct_of_column_names(column_name_list, df)

    # Institutes
    dct_key = FilterConsts.filter_institute
    column_name_list = list(InfoConsts.institute_dct.values())
    filter_dct[dct_key] = create_dct_of_column_names(column_name_list, df)

    # Add list of all courses associated with each study line to dct
    dct_key = FilterConsts.filter_study_lines
    filter_dct[dct_key] = create_lst_of_study_lines(df, course_numbers)

    """



#%%
if __name__ == "__main__":

    filter_dct = filter_dct_creator()
    # save as JSON
    json_name  = WebsiteConsts.json_filter_dct
    path_and_file_name = FileNameConsts.path_of_pkl + json_name + '.json'
    with open(path_and_file_name, 'w') as fp:
        json.dump(filter_dct, fp)
    print(f"The dictionary {json_name}.json has been saved...")

    # test print
    with open(path_and_file_name) as f:
        filter_dct = json.load(f)
    #print(filter_dct["study_lines"]["BSC_EE1"])