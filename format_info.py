#%%
import html
from scrape_info import InfoScraper
from format_study_lines import format_study_line_scrape
from utils import Utils
from website.global_constants.config import Config
from website.global_constants.file_name_consts import FileNameConsts
from website.global_constants.info_consts import InfoConsts


class InfoFormatter:

    @staticmethod
    def quick_test_for_debugging_please_ignore():
        """ Do a quick formatting test to see if the code works."""
        course_numbers = ['01001', '02402']  # Example of valid courses for the below semesters
        academic_year = '2023-2024'  # Example of valid academic year
        file_name = ""  # This prevents scraped data from being saved to disk
        df = InfoScraper.scrape_info(course_numbers, academic_year, file_name)
        iteration_count = 0
        for course_number in course_numbers:
            formatted_info = InfoFormatter.format_info(df, course_number)
            print(formatted_info)
            Utils.display_progress(iteration_count, course_numbers, FileNameConsts.info_format, 200)
            iteration_count += 1 # iteration_count must be incremented AFTER display progress


    @staticmethod
    def format_info(df, course_number):
        """Return formatted scraped info"""

        # Initialize dict containing formatted info
        scraped_info = df.loc[course_number].to_dict()
        formatted_info = {}
        info_to_format = InfoConsts.info_to_format

        for info_catagory in info_to_format:
            formatted_info = InfoFormatter._look_for_info(
                scraped_info,
                course_number,
                formatted_info,
                info_catagory.key_raw,
                info_catagory.key_df,
                info_catagory.values_raw,
                info_catagory.values_df,
                info_catagory.add_raw
            )

        # ECTS-oddity (TO-DO: fix this)
        ECTS_POINTS = InfoConsts.ects_points.key_df
        formatted_info[ECTS_POINTS] = InfoFormatter._ects_add_decimal_point(formatted_info[ECTS_POINTS])

        #institute = get_institute_from_number(course_number)
        #formatted_info[InfoConsts.institute] = institute

        # Return formatted info dict
        return formatted_info

    @staticmethod
    def _ects_add_decimal_point(ects_points):
        """Add missing decimal point that gets removed during ECTS scrape"""
        # It is assumed that no courses are greater than 20 ECTS.
        # In case this assumption is wrong, a bug will happen. Too bad!
        # We assume the decimal point has gone missing. Divide by 10 to compensate.
        # This is not an edge case, all decimal ects values have their decimal point missing?!?!
        # I don't know why and I don't care enough to implement a proper fix. Sad trumpet noise...
        try:
            if int(ects_points) > 21:
                ects_points = str(float(int(ects_points) / 10))
        except (ValueError, TypeError):
            pass
        return ects_points

    @staticmethod
    def _is_start_of_string_equal(key_value, potential_value, key):
        """Return boolean value 'True' if one string is contained in the other"""
        key_value = str(key_value)
        potential_value = str(potential_value)

        # Special check is needed when checking the value of 'Duration' key
        if key == 'Duration of Course':
            if key_value == potential_value:
                return True

        # Special check is needed when checking the value of 'Schedule' key
        elif key == 'Schedule':
            key_value = key_value.replace("Spring F1 (Mon 8-12, Thurs 13-17)", "Spring F1A (Mon 8-12) and Spring F1B (Thurs 13-17)")
            key_value = key_value.replace("Spring F2 (Mon 13-17, Thurs 8-12)", "Spring F2A (Mon 13-17) and Spring F2B (Thurs 8-12)")
            key_value = key_value.replace("Spring F3 (Tues 8-12, Fri 13-17)", "Spring F3A (Tues 8-12) and Spring F3B (Fri 13-17)")
            key_value = key_value.replace("Spring F4 (Tues 13-17, Fri 8-12)", "Spring F4A (Tues 13-17) and Spring F4B (Fri 8-12)")
            key_value = key_value.replace("Spring F5 (Wed 8-17)", "Spring F5A (Wed 8-12) and Spring F5B (Wed 13-17)")
            key_value = key_value.replace("Autumn E1 (Mon 8-12, Thurs 13-17)", "Autumn E1A (Mon 8-12) and Autumn E1B (Thurs 13-17)")
            key_value = key_value.replace("Autumn E2 (Mon 13-17, Thurs 8-12)", "Autumn E2A (Mon 13-17) and Autumn E2B (Thurs 8-12)")
            key_value = key_value.replace("Autumn E3 (Tues 8-12, Fri 13-17)", "Autumn E3A (Tues 8-12) and Autumn E3B (Fri 13-17)")
            key_value = key_value.replace("Autumn E4 (Tues 13-17, Fri 8-12)", "Autumn E4A (Tues 13-17) and Autumn E4B (Fri 8-12)")
            key_value = key_value.replace("Autumn E5 (Wed 8-17)", "Autumn E5A (Wed 8-12) and Autumn E5B (Wed 13-17)")
            key_value = key_value.replace("F7 (Tues 18-22)", "Spring F7 (Tues 18-22)")
            key_value = key_value.replace("E7 (Tues 18-22)", "Autumn E7 (Tues 18-22)")
            # Is a double-space or the word "and" continuing the key?
            # If yes, check all potential continuations of the key
            key_value = key_value.replace(' and ', '  ')
            #print(course_number+': '+key_value)
            lst_key = key_value.split('  ')
            for i in range(0, len(lst_key)):
                # Does one string start with the other string?
                #print(str(lst_key[i] == potential_value)+': '+lst_key[i] +' == '+ potential_value)
                if lst_key[i] == potential_value:
                    return True

        # Special check is needed when checking the value of 'assignments' key
        elif key == "Type of assessment":
            key_value = key_value.replace("Oral examination and", "Oral exam and")
            key_value = key_value.replace("Written examination and", "Written exam and")
            str_length = len(potential_value)
            # Is start of key_value string equal to potential_value string?
            if key_value[0:str_length] == potential_value[0:str_length]:
                return True

        # For every other key besides the exceptions above
        else:
            str_length = len(potential_value)
            # Is start of key_value string equal to potential_value string?
            if key_value[0:str_length] == potential_value[0:str_length]:
                return True

        # The two string were not considered equal
        return False

    @staticmethod
    def _look_for_info(scraped_info, course_number, formatted_info, key, key_renamed, values, values_renamed, add_raw):
        """If values[i] is in scraped info, add it to formatted_info dict"""

        keys_expected_to_hold_a_known_value = [
            InfoConsts.study_lines.key_df,
            InfoConsts.exam_aid.key_df,
            InfoConsts.semester_period.key_df,
            InfoConsts.time_of_week.key_df,
            InfoConsts.time_of_week_updated.key_df,
            InfoConsts.location.key_df
        ]

        keys_with_broken_encoding = [
            InfoConsts.main_responsible_name.key_df,
            InfoConsts.co_responsible_1_name.key_df,
            InfoConsts.co_responsible_2_name.key_df,
            InfoConsts.co_responsible_3_name.key_df,
            InfoConsts.co_responsible_4_name.key_df,
        ]

        if key_renamed in keys_expected_to_hold_a_known_value:
            log_type="log"
        else:
            log_type="Warning"

        # Create keys with default values for formatted_info
        formatted_info[key_renamed] = InfoConsts.not_yet_assigned_value
        for i in range(0, len(values_renamed)):
            formatted_info[values_renamed[i]] = 0

        # Copy the raw data value to dict if add_raw == True
        if add_raw is True:
            formatted_info[key_renamed+'_'+InfoConsts.raw_key] = InfoConsts.not_yet_assigned_value
            # Special case for type of assessment:
            if key in scraped_info and key != "Type of assessment":
                formatted_info[key_renamed+'_'+InfoConsts.raw_key] = str(scraped_info[key])
            elif key in scraped_info and key == "Type of assessment":
                exam_type_raw = str(scraped_info[key])
                exam_type_raw = exam_type_raw.replace("Oral examination and", "Oral exam and")
                exam_type_raw = exam_type_raw.replace("Written examination and", "Written exam and")
                exam_values = ["Written examination ",
                            "Written exam and reports ",
                            "Written exam and exercises ",
                            "Written exam and experiments ",
                            "Oral examination ",
                            "Oral exam and reports ",
                            "Oral exam and exercises ",
                            "Oral exam and experiments ",
                            "Evaluation of exercises/reports ",
                            "Evaluation of experiments and reports ",
                            "Written or oral examination ",
                            "Written and oral examination ",
                            "Report/dissertation "]
                for k in range (0, len(exam_values)):
                    exam_type_raw = exam_type_raw.replace(exam_values[k],exam_values[k]+"<br />")
                formatted_info[key_renamed+'_'+InfoConsts.raw_key] = exam_type_raw

        # Update the boolean keys in formatted_info with the scraped data
        lst_of_booleans = []
        boolean_value_count = 0
        lst_of_study_lines = []
        if key in scraped_info and key_renamed != InfoConsts.institute.key_df:
            if key_renamed == InfoConsts.study_lines.key_df and scraped_info[key] is not None and len(scraped_info[key]) != 0:
                lst_of_study_lines = format_study_line_scrape(scraped_info[key], {})
            for i in range(0, len(values)):
                # Check each of the expected values and see if they match what's in the scraped dict (if yes, append them to the output string)
                if InfoFormatter._is_start_of_string_equal(scraped_info[key], values[i], key) or (values[i] in lst_of_study_lines):
                    formatted_info[values_renamed[i]] = 1
                    boolean_value_count += 1
                    lst_of_booleans.append(str(values_renamed[i]))
                    for j in range (0, len(values)):
                        if formatted_info[values_renamed[j]] == InfoConsts.not_yet_assigned_value:
                            formatted_info[values_renamed[j]] = 0

            # Print a warning if an element in the scraped study line list was not recognized
            if key_renamed == InfoConsts.study_lines.key_df and len(lst_of_study_lines) != boolean_value_count:
                message = f"{FileNameConsts.info_format}, {course_number}: {len(lst_of_study_lines) - boolean_value_count} unknown study line(s)"
                Utils.logger(message, "warning", FileNameConsts.format_log_name)
                for study_line in lst_of_study_lines:
                    if study_line not in values:
                        print(f'Warning, {course_number}: "{study_line}" was not recognized as a study line. Go to line ~300 of info_consts.py and manually update list')

            # Check if all expected values in SCRAPED_INFO_DICT[key] was found
            if len(values) == 0:
                formatted_info[key_renamed] = str(scraped_info[key])
                if key_renamed in keys_with_broken_encoding:
                    formatted_info[key_renamed] = html.unescape(str(scraped_info[key]))
                if log_type.lower() != 'none':
                    message = f"{FileNameConsts.info_format}, {course_number}: '{key_renamed}' = '{scraped_info[key]}'"
                    #Utils.logger(message, "log", FileNameConsts.format_log_name)
            elif boolean_value_count == 0:
                if key_renamed == InfoConsts.study_lines.key_df:
                    lst_of_booleans.append(InfoConsts.no_linked_study_lines)
                    formatted_info[values_renamed[-1]] = 1
                elif key_renamed == InfoConsts.location.key_df:
                    formatted_info[values_renamed[-1]] = 1
                elif (key_renamed == InfoConsts.time_of_week.key_df) or (key_renamed == InfoConsts.semester_period.key_df):
                    lst_of_booleans.append(InfoConsts.unspecified_schedule)
                else:
                    lst_of_booleans.append(InfoConsts.unknown_value)
                message = f"{FileNameConsts.info_format}, {course_number}: {key_renamed}'s boolean sum is 0"
                Utils.logger(message, log_type, FileNameConsts.format_log_name)

        # Institute is decided based on course number rather than scraped data
        elif key_renamed == InfoConsts.institute.key_df:
            institute = InfoFormatter._get_institute_from_number(course_number)
            formatted_info[key_renamed] = institute
            for i in range(0, len(values_renamed)):
                if institute == values_renamed[i]:
                    formatted_info[values_renamed[i]] = 1
                    boolean_value_count += 1
            if boolean_value_count == 0:
                print(f"{FileNameConsts.info_format}, {course_number}: {key_renamed}'s bool sum 0")

        # If key was not found in scraped_info_dict:
        else:
            message = f"{FileNameConsts.info_format}, {course_number}: {key_renamed} not found in info_scrape"
            Utils.logger(message, log_type, FileNameConsts.format_log_name)

        # Combine lst_of_booleans into string
        if len(lst_of_booleans) > 0:
            # Remove duplicates by temporary converting list to dict
            lst_of_booleans = list(dict.fromkeys(lst_of_booleans))
            # Join lst_of_booleans into string
            if key_renamed == InfoConsts.study_lines.key_df:
                SEPARATOR = InfoConsts.separator_html
            elif key_renamed == InfoConsts.time_of_week.key_df:
                SEPARATOR = InfoConsts.separator_html
            else:
                SEPARATOR = InfoConsts.separator_plus
            booleans_as_word = SEPARATOR.join(lst_of_booleans)
            # Convert to numeric data type, if possible
            if booleans_as_word.isnumeric():
                booleans_as_word = float(booleans_as_word)
                if booleans_as_word.is_integer():
                    booleans_as_word = int(booleans_as_word)
            formatted_info[key_renamed] = booleans_as_word
        return formatted_info

    @staticmethod
    def _get_institute_from_number(course_number):
        """Categorize institute from first two digits in course number"""
        department_dct = InfoConsts.institute
        department_dct = dict(zip(InfoConsts.institute.values_raw, InfoConsts.institute.values_df))
        first_two_digits = course_number[0:2]
        if first_two_digits in department_dct:
            department = department_dct[first_two_digits]
        else:
            department = "Partner University"
            message = f"{FileNameConsts.info_format}, {course_number}: Institute {first_two_digits} is unknown"
            Utils.logger(message, "warning", FileNameConsts.format_log_name)
        return department

    @staticmethod
    def parse_previous_courses_from_dtu_website_rawstring(raw_input):
        """Parse the string that contains previous course numbers for a course"""
        def split_by_separators(s):
            """Define all separators"""
            s = s.replace(" and ", "|")
            s = s.replace("/", "|")
            s = s.replace(",", "|")
            return s.split("|")
        parts = split_by_separators(raw_input)
        course_codes = []
        for part in parts:
            code = part.strip()
            if '-' in code:
                continue
            if code.isdigit():
                course_codes.append(code)
            elif code.isalnum() and any(c.isdigit() for c in code):
                course_codes.append(code)
        return course_codes


#%%
if __name__ == "__main__":
    InfoFormatter.quick_test_for_debugging_please_ignore()