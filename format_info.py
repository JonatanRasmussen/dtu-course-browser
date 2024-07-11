#%%

# Imports
# Helper functions and global constants
from format_study_lines import format_study_line_scrape
from utils import Utils
from website.global_constants.config import Config
from website.global_constants.file_name_consts import FileNameConsts
from website.global_constants.info_consts import InfoConsts


def format_info(scraped_info, course_number, info_name):
    """Return formatted scraped info"""

    def ects_add_decimal_point(ects_points):
        """Add missing decimal point that gets removed during ECTS scrape"""
        try:
            if int(ects_points) > 21:
                ects_points = str(float(int(ects_points) / 10))
        except:
            pass
        return ects_points

    def is_start_of_string_equal(key_value, potential_value, key):
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
            key_value = key_value.replace("F7 (Tues 18-22)", "Spring E7 (Tues 18-22)")
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

    def look_for_info(formatted_info, key, key_renamed, values, values_renamed, add_raw):
        """If values[i] is in scraped info, add it to formatted_info dict"""

        keys_expected_to_hold_a_known_value = [InfoConsts.study_lines.key_df,
                                               InfoConsts.exam_aid.key_df,
                                               InfoConsts.semester_period.key_df,
                                               InfoConsts.time_of_week.key_df,
                                               InfoConsts.time_of_week_updated.key_df,
                                               InfoConsts.location.key_df]
        if key_renamed in keys_expected_to_hold_a_known_value:
            log_type="log"
        else:
            log_type="Warning"

        # Create keys with default values for formatted_info
        formatted_info[key_renamed] = InfoConsts.not_yet_assigned_value
        for i in range(0, len(values_renamed)):
            formatted_info[values_renamed[i]] = 0

        # Copy the raw data value to dict if add_raw == True
        if add_raw == True:
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
            if key_renamed == InfoConsts.study_lines.key_df:
                lst_of_study_lines = format_study_line_scrape(scraped_info[key], {})
            for i in range(0, len(values)):
                # Check each of the expected values and see if they match what's in the scraped dict (if yes, append them to the output string)
                if is_start_of_string_equal(scraped_info[key], values[i], key) or (values[i] in lst_of_study_lines):
                    formatted_info[values_renamed[i]] = 1
                    boolean_value_count += 1
                    lst_of_booleans.append(str(values_renamed[i]))
                    for j in range (0, len(values)):
                        if formatted_info[values_renamed[j]] == InfoConsts.not_yet_assigned_value:
                            formatted_info[values_renamed[j]] = 0

            # Print a warning if an element in the scraped study line list was not recognized
            if key_renamed == InfoConsts.study_lines.key_df and len(lst_of_study_lines) != boolean_value_count:
                message = f"{info_name}, {course_number}: {len(lst_of_study_lines) - boolean_value_count} unknown study line(s)"
                Utils.logger(message, "warning", FileNameConsts.format_log_name)
                for k in range(0, len(lst_of_study_lines)):
                    """ if course_number == "41636":
                    print(lst_of_study_lines[k])
                    testy = lst_of_study_lines[k]
                    if "General competence" in testy:
                        print("WTFFFF")
                        folder_name = "wtfff"
                        Utils.create_folder(folder_name)
                        file_location = f'{folder_name}/{"wtf"}.txt'
                        with open(file_location, 'w', encoding='utf-8') as file:
                            file.write(testy)
                            file.close()
                    testy = testy.replace("General competence course (MSc)", "GENERAL COMPETENCE ")
                    print(testy) """ # NEVER FORGET THIS ABSOLUTE DEGENERACY OF CHASING DOWN A ' ' using non-breaking space &nbsp;
                    if lst_of_study_lines[k] not in values:
                        print(f'Warning, {course_number}: "{lst_of_study_lines[k]}" was not recognized as a study line. Go to line ~630 and manually update list')

            # Check if all expected values in SCRAPED_INFO_DICT[key] was found
            if len(values) == 0:
                formatted_info[key_renamed] = str(scraped_info[key])
                if log_type.lower() != 'none':
                    message = f"{info_name}, {course_number}: '{key_renamed}' = '{scraped_info[key]}'"
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
                message = f"{info_name}, {course_number}: {key_renamed}'s boolean sum is 0"
                Utils.logger(message, log_type, FileNameConsts.format_log_name)

        # Institute is decided based on course number rather than scraped data
        elif key_renamed == InfoConsts.institute.key_df:
            institute = get_institute_from_number(course_number)
            formatted_info[key_renamed] = institute
            for i in range(0, len(values_renamed)):
                if institute == values_renamed[i]:
                    formatted_info[values_renamed[i]] = 1
                    boolean_value_count += 1
            if boolean_value_count == 0:
                print(f"{info_name}, {course_number}: {key_renamed}'s bool sum 0")

        # If key was not found in scraped_info_dict:
        else:
            message = f"{info_name}, {course_number}: {key_renamed} not found in info_scrape"
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
            if log_type.lower() != 'none':
                message = f"{info_name}, {course_number}: '{key_renamed}' = '{booleans_as_word}'"
                #Utils.logger(message, "log", FileNameConsts.format_log_name)

        # Special case for ECTS-points:


        return formatted_info

    def get_institute_from_number(course_number):
        """Categorize institute from first two digits in course number"""
        department_dct = InfoConsts.institute
        department_dct = dict(zip(InfoConsts.institute.values_raw, InfoConsts.institute.values_df))
        first_two_digits = course_number[0:2]
        if first_two_digits in department_dct:
            department = department_dct[first_two_digits]
        else:
            department = "Partner University"
            message = f"{info_name}, {course_number}: Institute {first_two_digits} is unknown"
            Utils.logger(message, "warning", FileNameConsts.format_log_name)
        return department


#%%

    # Initialize dict containing formatted info
    formatted_info = {}
    info_to_format = InfoConsts.info_to_format

    for info_catagory in info_to_format:
        formatted_info = look_for_info(formatted_info,
                                       info_catagory.key_raw,
                                       info_catagory.key_df,
                                       info_catagory.values_raw,
                                       info_catagory.values_df,
                                       info_catagory.add_raw)

    # ECTS-oddity (TO-DO: fix this)
    ECTS_POINTS = InfoConsts.ects_points.key_df
    formatted_info[ECTS_POINTS] = ects_add_decimal_point(formatted_info[ECTS_POINTS])

    #institute = get_institute_from_number(course_number)
    #formatted_info[InfoConsts.institute] = institute

    # Return formatted info dict
    return formatted_info

    # Initialization custom names
    '''
    NAME_DANISH = InfoConsts.name_danish

    LANGUAGE = InfoConsts.language
    LANGUAGE_DANISH = InfoConsts.language_danish
    LANGUAGE_ENGLISH = InfoConsts.language_english

    INSTITUTE = InfoConsts.institute

    GRADE_TYPE = InfoConsts.grade_type
    GRADE_SEVEN_STEP_SCALE = InfoConsts.grade_seven_step_scale
    GRADE_PASS_OR_FAIL = InfoConsts.grade_pass_or_fail
    EXAMINER = InfoConsts.examiner
    EXAMINER_INTERNAL = InfoConsts.examiner_internal
    EXAMINER_EXTERNAL = InfoConsts.examiner_external

    CAMPUS = InfoConsts.campus
    CAMPUS_LYNGBY = InfoConsts.campus_lyngby
    CAMPUS_BALLERUP = InfoConsts.campus_ballerup

    COURSE_TYPE = InfoConsts.course_type
    BSC = InfoConsts.bsc
    MSC = InfoConsts.msc
    BENG = InfoConsts.beng
    PHD = InfoConsts.phd
    DELTIDSDIPLOM = InfoConsts.beng
    DELTIDSMASTER = InfoConsts.msc

    EXAM_AID = InfoConsts.exam_aid
    ALL_AID = InfoConsts.all_aid
    WRITTEN_AID = InfoConsts.written_aid
    NO_AID = InfoConsts.no_aid

    EXAM_TYPE = InfoConsts.exam_type
    EXAM_WRITTEN = InfoConsts.exam_written
    EXAM_ORAL = InfoConsts.exam_oral
    EXAM_NONE = InfoConsts.exam_none
    EXAM_BOTH = InfoConsts.exam_both
    ASSIGNMENTS = InfoConsts.assignments
    ASSIGNMENTS_NONE = InfoConsts.assignments_none
    ASSIGNMENTS_REPORTS = InfoConsts.assignments_reports
    ASSIGNMENTS_EXERCISES = InfoConsts.assignments_exercises
    ASSIGNMENTS_EXPERIMENTS = InfoConsts.assignments_experiments
    #EXAM_TYPE_UNEDITED = InfoConsts.exam_type_unedited
    #EXAM_WRITTEN_REPORTS = InfoConsts.exam_written_reports
    #EXAM_WRITTEN_EXERCISES = InfoConsts.exam_written_exercises
    #EXAM_WRITTEN_EXPERIMENTS = InfoConsts.exam_written_experiments
    #EXAM_ORAL_REPORTS = InfoConsts.exam_oral_reports
    #EXAM_ORAL_EXERCISES = InfoConsts.exam_oral_exercises
    #EXAM_ORAL_EXPERIMENTS = InfoConsts.exam_oral_experiments
    #EXAM_NONE_REPORTS = InfoConsts.exam_none_reports
    #EXAM_NONE_EXPERIMENTS = InfoConsts.exam_none_experiments

    COURSE_DURATION = InfoConsts.course_duration
    DURATION_13_WEEKS = InfoConsts.duration_13_weeks
    DURATION_3_WEEKS = InfoConsts.duration_3_weeks
    DURATION_16_WEEKS = InfoConsts.duration_16_weeks
    DURATION_26_WEEKS = InfoConsts.duration_26_weeks
    DURATION_UNIQUE = InfoConsts.duration_unique

    UNIQUE_SCHEDULE = InfoConsts.unique_schedule
    THREE_WEEK_JANUARY = InfoConsts.three_week_january
    THREE_WEEK_JUNE = InfoConsts.three_week_june
    THREE_WEEK_JULY = InfoConsts.three_week_july
    THREE_WEEK_AUGUST = InfoConsts.three_week_august
    SPRING = InfoConsts.spring
    F1A = InfoConsts.F1A
    F1B = InfoConsts.F1B
    F2A = InfoConsts.F2A
    F2B = InfoConsts.F2B
    F3A = InfoConsts.F3A
    F3B = InfoConsts.F3B
    F4A = InfoConsts.F4A
    F4B = InfoConsts.F4B
    F5A = InfoConsts.F5A
    F5B = InfoConsts.F5B
    F7 = InfoConsts.F7
    AUTUMN = InfoConsts.autumn
    E1A = InfoConsts.E1A
    E1B = InfoConsts.E1B
    E2A = InfoConsts.E2A
    E2B = InfoConsts.E2B
    E3A = InfoConsts.E3A
    E3B = InfoConsts.E3B
    E4A = InfoConsts.E4A
    E4B = InfoConsts.E4B
    E5A = InfoConsts.E5A
    E5B = InfoConsts.E5B
    E7 = InfoConsts.E7
    JANUARY = InfoConsts.january
    JUNE = InfoConsts.june
    JULY = InfoConsts.july
    AUGUST = InfoConsts.august

    RECOMMENDED_PREREQUISITES = InfoConsts.recommended_prerequisites
    MANDATORY_PREREQUISITES = InfoConsts.mandatory_prerequisites

    LAST_UPDATED = InfoConsts.last_updated

    COURSE_OBJECTIVES = InfoConsts.course_description
    LEARNING_OBJECTIVES = InfoConsts.learning_objectives
    COURSE_CONTENT = InfoConsts.course_content

    SCOPE_AND_FORM = InfoConsts.scope_and_form
    EXAM_DURATION = InfoConsts.exam_duration
    EXAM_AID = InfoConsts.exam_aid
    WEBPAGE = InfoConsts.webpage

    MAIN_RESPONSIBLE_NAME = InfoConsts.main_responsible_name
    MAIN_RESPONSIBLE_PIC = InfoConsts.main_responsible_pic
    CO_RESPONSIBLE_1_NAME = InfoConsts.co_responsible_1_name
    CO_RESPONSIBLE_1_PIC = InfoConsts.co_responsible_1_pic
    CO_RESPONSIBLE_2_NAME = InfoConsts.co_responsible_2_name
    CO_RESPONSIBLE_2_PIC = InfoConsts.co_responsible_2_pic
    CO_RESPONSIBLE_3_NAME = InfoConsts.co_responsible_3_name
    CO_RESPONSIBLE_3_PIC = InfoConsts.co_responsible_3_pic
    CO_RESPONSIBLE_4_NAME = InfoConsts.co_responsible_4_name
    CO_RESPONSIBLE_4_PIC = InfoConsts.co_responsible_4_pic

    STUDY_LINES = InfoConsts.study_lines

    STUDYLINE_LST = InfoConsts.studyline_lst
    '''

"""
# Get Danish name
    key = "Danish title"
    values = []
    key_renamed = NAME_DANISH
    values_renamed = []
    add_raw = False
    formatted_info = look_for_info(formatted_info, key, key_renamed, values, values_renamed, add_raw, "Warning")

# Get number of ECTS points
    key = "Point( ECTS )"
    values = []
    key_renamed = ECTS_POINTS
    values_renamed = []
    add_raw = False
    formatted_info = look_for_info(formatted_info, key, key_renamed, values, values_renamed, add_raw, "Warning")
    formatted_info[ECTS_POINTS] = ects_add_decimal_point(formatted_info[ECTS_POINTS])

# Get language type
    key = "Language of instruction"
    values = ["Danish", "English"]
    key_renamed = LANGUAGE
    values_renamed = [LANGUAGE_DANISH, LANGUAGE_ENGLISH]
    add_raw = False
    formatted_info = look_for_info(formatted_info, key, key_renamed, values, values_renamed, add_raw, "Warning")

# Get institute
    institute = get_institute_from_number(course_number)
    formatted_info[INSTITUTE] = institute

# Get grade type and examiner type
    key = "Evaluation"
    values = ["7 step scale , internal examiner",
              "7 step scale , external examiner",
              "pass / not pass , internal examiner",
              "pass / not pass , external examiner"]
    key_renamed = GRADE_TYPE
    values_renamed = [GRADE_SEVEN_STEP_SCALE,
                      GRADE_SEVEN_STEP_SCALE,
                      GRADE_PASS_OR_FAIL,
                      GRADE_PASS_OR_FAIL]
    add_raw = False
    formatted_info = look_for_info(formatted_info, key, key_renamed, values, values_renamed, add_raw, "Warning")
    key_renamed = EXAMINER
    values_renamed = [EXAMINER_INTERNAL,
                      EXAMINER_EXTERNAL,
                      EXAMINER_INTERNAL,
                      EXAMINER_EXTERNAL]
    add_raw = False
    formatted_info = look_for_info(formatted_info, key, key_renamed, values, values_renamed, add_raw, "Warning")

# Get campus
    key = "Location"
    values = ["Campus Lyngby", "Campus Ballerup"]
    key_renamed = CAMPUS
    values_renamed = [CAMPUS_LYNGBY, CAMPUS_BALLERUP]
    add_raw = True
    formatted_info = look_for_info(formatted_info, key, key_renamed, values, values_renamed, add_raw)

# Get course type
    key = "Course type"
    values = ["BSc", "MSc", "BScMSc", "BEng", "Ph.D.", "Deltidsdiplom", "Parttime master"]
    key_renamed = COURSE_TYPE
    values_renamed = [BSC, MSC, MSC, BENG, PHD, DELTIDSDIPLOM, DELTIDSMASTER]
    add_raw = False
    formatted_info = look_for_info(formatted_info, key, key_renamed, values, values_renamed, add_raw, "Warning")

# Get type of assessment
# SPAGHETTI-WARNING: look_for_info calls is_start_of_string_equal,
# which turns "examination" into "exam" if it's followed by
# reports/exercises/experiments. This may cause bugs
    key = "Type of assessment"
    values = ["Written examination",
              "Written exam and reports",
              "Written exam and exercises",
              "Written exam and experiments",
              "Oral examination",
              "Oral exam and reports",
              "Oral exam and exercises",
              "Oral exam and experiments",
              "Evaluation of experiments",
              "Evaluation of exercises/reports",
              "Evaluation of experiments and reports",
              "Written or oral examination",
              "Written and oral examination",
              "Report/dissertation"]
    key_renamed = EXAM_TYPE
    values_renamed = [EXAM_WRITTEN,
                      EXAM_WRITTEN,
                      EXAM_WRITTEN,
                      EXAM_WRITTEN,
                      EXAM_ORAL,
                      EXAM_ORAL,
                      EXAM_ORAL,
                      EXAM_ORAL,
                      EXAM_NONE,
                      EXAM_NONE,
                      EXAM_NONE,
                      EXAM_BOTH,
                      EXAM_BOTH,
                      EXAM_NONE]
    add_raw = True
    formatted_info = look_for_info(formatted_info, key, key_renamed, values, values_renamed, add_raw)
    key_renamed = ASSIGNMENTS
    values_renamed = [ASSIGNMENTS_NONE,
                      ASSIGNMENTS_REPORTS,
                      ASSIGNMENTS_EXERCISES,
                      ASSIGNMENTS_EXPERIMENTS,
                      ASSIGNMENTS_NONE,
                      ASSIGNMENTS_REPORTS,
                      ASSIGNMENTS_EXERCISES,
                      ASSIGNMENTS_EXPERIMENTS,
                      ASSIGNMENTS_EXPERIMENTS,
                      ASSIGNMENTS_REPORTS,
                      ASSIGNMENTS_EXPERIMENTS,
                      ASSIGNMENTS_NONE,
                      ASSIGNMENTS_NONE,
                      ASSIGNMENTS_REPORTS]
    add_raw = False
    formatted_info = look_for_info(formatted_info, key, key_renamed, values, values_renamed, add_raw)
    #key_renamed = EXAM_TYPE_UNEDITED
    #values_renamed = [EXAM_WRITTEN,
    #                  EXAM_WRITTEN_REPORTS,
    #                  EXAM_WRITTEN_EXERCISES,
    #                  EXAM_WRITTEN_EXPERIMENTS,
    #                  EXAM_ORAL,
    #                  EXAM_ORAL_REPORTS,
    #                  EXAM_ORAL_EXERCISES,
    #                  EXAM_ORAL_EXPERIMENTS,
    #                  EXAM_ORAL_EXPERIMENTS,
    #                  EXAM_NONE_REPORTS,
    #                  EXAM_NONE_EXPERIMENTS,
    #                  EXAM_BOTH,
    #                  EXAM_BOTH,
    #                  EXAM_NONE_REPORTS]
    #add_raw = False
    #formatted_info = look_for_info(formatted_info, key, key_renamed, values, values_renamed, add_raw)

# Get course duration
    key = "Duration of Course"
    values = ["13 weeks",
              "3 weeks",
              "13 weeks + 3 weeks",
              "3 weeks + 13 weeks",
              "13 weeks or 3 weeks",
              "13 weeks + 13 weeks",
              "[The course is not following DTUs normal Schedule]"]
    key_renamed = COURSE_DURATION
    values_renamed = [DURATION_13_WEEKS,
                      DURATION_3_WEEKS,
                      DURATION_16_WEEKS,
                      DURATION_16_WEEKS,
                      DURATION_16_WEEKS,
                      DURATION_26_WEEKS,
                      DURATION_UNIQUE]
    add_raw = False
    formatted_info = look_for_info(formatted_info, key, key_renamed, values, values_renamed, add_raw, "Warning")

# Get schedule
    key = "Schedule"
    values = ["Spring",
              "Spring F1A (Mon 8-12)",
              "Spring F1B (Thurs 13-17)",
              "Spring F2A (Mon 13-17)",
              "Spring F2B (Thurs 8-12)",
              "Spring F3A (Tues 8-12)",
              "Spring F3B (Fri 13-17)",
              "Spring F4A (Tues 13-17)",
              "Spring F4B (Fri 8-12)",
              "Spring F5A (Wed 8-12)",
              "Spring F5B (Wed 13-17)",
              "Spring E7 (Tues 18-22)",
              "Autumn",
              "Autumn E1A (Mon 8-12)",
              "Autumn E1B (Thurs 13-17)",
              "Autumn E2A (Mon 13-17)",
              "Autumn E2B (Thurs 8-12)",
              "Autumn E3A (Tues 8-12)",
              "Autumn E3B (Fri 13-17)",
              "Autumn E4A (Tues 13-17)",
              "Autumn E4B (Fri 8-12)",
              "Autumn E5A (Wed 8-12)",
              "Autumn E5B (Wed 13-17)",
              "Autumn E7 (Tues 18-22)",
              "January",
              "June",
              "July",
              "August",]
    key_renamed = TIME_OF_WEEK
    values_renamed = [UNIQUE_SCHEDULE,
                      F1A,
                      F1B,
                      F2A,
                      F2B,
                      F3A,
                      F3B,
                      F4A,
                      F4B,
                      F5A,
                      F5B,
                      F7,
                      UNIQUE_SCHEDULE,
                      E1A,
                      E1B,
                      E2A,
                      E2B,
                      E3A,
                      E3B,
                      E4A,
                      E4B,
                      E5A,
                      E5B,
                      E7,
                      THREE_WEEK_JANUARY,
                      THREE_WEEK_JUNE,
                      THREE_WEEK_JULY,
                      THREE_WEEK_AUGUST]
    add_raw = False
    formatted_info = look_for_info(formatted_info, key, key_renamed, values, values_renamed, add_raw)
    key_renamed = TIME_OF_YEAR
    values_renamed = [SPRING,
                      SPRING,
                      SPRING,
                      SPRING,
                      SPRING,
                      SPRING,
                      SPRING,
                      SPRING,
                      SPRING,
                      SPRING,
                      SPRING,
                      SPRING,
                      AUTUMN,
                      AUTUMN,
                      AUTUMN,
                      AUTUMN,
                      AUTUMN,
                      AUTUMN,
                      AUTUMN,
                      AUTUMN,
                      AUTUMN,
                      AUTUMN,
                      AUTUMN,
                      AUTUMN,
                      JANUARY,
                      JUNE,
                      JULY,
                      AUGUST]
    add_raw = False
    formatted_info = look_for_info(formatted_info, key, key_renamed, values, values_renamed, add_raw)

# Get name of study lines
    key = STUDY_LINES
    values = []
    key_renamed = STUDY_LINES
    values_renamed = []
    add_raw = False
    formatted_info = look_for_info(formatted_info, key, key_renamed, values, values_renamed, add_raw, "None")

# Get course duration
    key = STUDY_LINES
    values = STUDYLINE_LST
    key_renamed = STUDY_LINES_FORMATTED
    values_renamed = values
    add_raw = False
    formatted_info = look_for_info(formatted_info, key, key_renamed, values, values_renamed, add_raw)

# Get last updated
    key = LAST_UPDATED
    values = []
    key_renamed = LAST_UPDATED
    values_renamed = []
    add_raw = False
    formatted_info = look_for_info(formatted_info, key, key_renamed, values, values_renamed, add_raw, "Warning")

# Get name of main responsible
    key = MAIN_RESPONSIBLE_NAME
    values = []
    key_renamed = MAIN_RESPONSIBLE_NAME
    values_renamed = []
    add_raw = False
    formatted_info = look_for_info(formatted_info, key, key_renamed, values, values_renamed, add_raw)

# Get image hyperlink of main responsible
    key = MAIN_RESPONSIBLE_PIC
    values = []
    key_renamed = MAIN_RESPONSIBLE_PIC
    values_renamed = []
    add_raw = False
    formatted_info = look_for_info(formatted_info, key, key_renamed, values, values_renamed, add_raw)

# Get name of co-responsible #1
    key = CO_RESPONSIBLE_1_NAME
    values = []
    key_renamed = CO_RESPONSIBLE_1_NAME
    values_renamed = []
    add_raw = False
    formatted_info = look_for_info(formatted_info, key, key_renamed, values, values_renamed, add_raw)

# Get image hyperlink of co-responsible #1
    key = CO_RESPONSIBLE_1_PIC
    values = []
    key_renamed = CO_RESPONSIBLE_1_PIC
    values_renamed = []
    add_raw = False
    formatted_info = look_for_info(formatted_info, key, key_renamed, values, values_renamed, add_raw)

# Get name of co-responsible #2
    key = CO_RESPONSIBLE_2_NAME
    values = []
    key_renamed = CO_RESPONSIBLE_2_NAME
    values_renamed = []
    add_raw = False
    formatted_info = look_for_info(formatted_info, key, key_renamed, values, values_renamed, add_raw)

# Get image hyperlink of co-responsible #2
    key = CO_RESPONSIBLE_2_PIC
    values = []
    key_renamed = CO_RESPONSIBLE_2_PIC
    values_renamed = []
    add_raw = False
    formatted_info = look_for_info(formatted_info, key, key_renamed, values, values_renamed, add_raw)

# Get name of co-responsible #3
    key = CO_RESPONSIBLE_3_NAME
    values = []
    key_renamed = CO_RESPONSIBLE_3_NAME
    values_renamed = []
    add_raw = False
    formatted_info = look_for_info(formatted_info, key, key_renamed, values, values_renamed, add_raw)

# Get image hyperlink of co-responsible #3
    key = CO_RESPONSIBLE_3_PIC
    values = []
    key_renamed = CO_RESPONSIBLE_3_PIC
    values_renamed = []
    add_raw = False
    formatted_info = look_for_info(formatted_info, key, key_renamed, values, values_renamed, add_raw)

# Get name of co-responsible #4
    key = CO_RESPONSIBLE_4_NAME
    values = []
    key_renamed = CO_RESPONSIBLE_4_NAME
    values_renamed = []
    add_raw = False
    formatted_info = look_for_info(formatted_info, key, key_renamed, values, values_renamed, add_raw)

# Get image hyperlink of co-responsible #4
    key = CO_RESPONSIBLE_4_PIC
    values = []
    key_renamed = CO_RESPONSIBLE_4_PIC
    values_renamed = []
    add_raw = False
    formatted_info = look_for_info(formatted_info, key, key_renamed, values, values_renamed, add_raw)

# Get recommended prerequisites
    key = "Recommended prerequisites"
    values = []
    key_renamed = RECOMMENDED_PREREQUISITES
    values_renamed = []
    add_raw = False
    formatted_info = look_for_info(formatted_info, key, key_renamed, values, values_renamed, add_raw, "None")

# Get mandatory prerequisites
    key = "Mandatory Prerequisites"
    values = []
    key_renamed = MANDATORY_PREREQUISITES
    values_renamed = []
    add_raw = False
    formatted_info = look_for_info(formatted_info, key, key_renamed, values, values_renamed, add_raw, "None")

# Get course objectives description
    key = COURSE_OBJECTIVES
    values = []
    key_renamed = COURSE_OBJECTIVES
    values_renamed = []
    add_raw = False
    formatted_info = look_for_info(formatted_info, key, key_renamed, values, values_renamed, add_raw, "None")

# Get course learning objectives
    key = LEARNING_OBJECTIVES
    values = []
    key_renamed = LEARNING_OBJECTIVES
    values_renamed = []
    add_raw = False
    formatted_info = look_for_info(formatted_info, key, key_renamed, values, values_renamed, add_raw, "None")

# Get course content list
    key = COURSE_CONTENT
    values = []
    key_renamed = COURSE_CONTENT
    values_renamed = []
    add_raw = False
    formatted_info = look_for_info(formatted_info, key, key_renamed, values, values_renamed, add_raw, "None")

# Get scope and form
    key = "Scope and form"
    values = []
    key_renamed = SCOPE_AND_FORM
    values_renamed = []
    add_raw = False
    formatted_info = look_for_info(formatted_info, key, key_renamed, values, values_renamed, add_raw, "None")

# Get exam duration
    key = "Exam duration"
    values = []
    key_renamed = EXAM_DURATION
    values_renamed = []
    add_raw = False
    formatted_info = look_for_info(formatted_info, key, key_renamed, values, values_renamed, add_raw, "None")

# Get type of aid for exam
    key = "Aid"
    values = ["All Aid", "Written works of reference are permitted", "No Aid"]
    key_renamed = EXAM_AID
    values_renamed = [ALL_AID, WRITTEN_AID, NO_AID]
    add_raw = True
    formatted_info = look_for_info(formatted_info, key, key_renamed, values, values_renamed, add_raw, "None")

# Get home page
    key = "Home page"
    values = []
    key_renamed = WEBPAGE
    values_renamed = []
    add_raw = False
    formatted_info = look_for_info(formatted_info, key, key_renamed, values, values_renamed, add_raw, "None")


# The following formatting is for extended csv only
# Get "Previous Course"
    key = "Previous Course"
    values = []
    key_renamed = InfoConsts.previous_course
    values_renamed = []
    add_raw = False
    formatted_info = look_for_info(formatted_info, key, key_renamed, values, values_renamed, add_raw, "None")

# Get "Registration Sign up"
    key = "Registration Sign up"
    values = []
    key_renamed = InfoConsts.registration_sign_up
    values_renamed = []
    add_raw = False
    formatted_info = look_for_info(formatted_info, key, key_renamed, values, values_renamed, add_raw, "None")

# Get "Not applicable together with"
    key = "Not applicable together with"
    values = []
    key_renamed = InfoConsts.not_applicable_with
    values_renamed = []
    add_raw = False
    formatted_info = look_for_info(formatted_info, key, key_renamed, values, values_renamed, add_raw, "None")

# Get "Green challenge participation"
    key = "Green challenge participation"
    values = []
    key_renamed = InfoConsts.green_challenge
    values_renamed = []
    add_raw = False
    formatted_info = look_for_info(formatted_info, key, key_renamed, values, values_renamed, add_raw, "None")

# Get "Department"
    key = "Department"
    values = []
    key_renamed = InfoConsts.department_main
    values_renamed = []
    add_raw = False
    formatted_info = look_for_info(formatted_info, key, key_renamed, values, values_renamed, add_raw, "None")

# Get "Department involved"
    key = "Department involved"
    values = []
    key_renamed = InfoConsts.department_involved
    values_renamed = []
    add_raw = False
    formatted_info = look_for_info(formatted_info, key, key_renamed, values, values_renamed, add_raw, "None")

# Get "External Institution"
    key = "External Institution"
    values = []
    key_renamed = InfoConsts.external_institution
    values_renamed = []
    add_raw = False
    formatted_info = look_for_info(formatted_info, key, key_renamed, values, values_renamed, add_raw, "None")

# Get "Date of examination"
    key = "Date of examination"
    values = []
    key_renamed = InfoConsts.date_of_examination
    values_renamed = []
    add_raw = False
    formatted_info = look_for_info(formatted_info, key, key_renamed, values, values_renamed, add_raw, "None")

# Get "Responsible"
    key = "Responsible"
    values = []
    key_renamed = InfoConsts.responsible_contact
    values_renamed = []
    add_raw = False
    formatted_info = look_for_info(formatted_info, key, key_renamed, values, values_renamed, add_raw, "None")

# Get "Course co-responsible"
    key = "Course co-responsible"
    values = []
    key_renamed = InfoConsts.responsible_co_contact
    values_renamed = []
    add_raw = False
    formatted_info = look_for_info(formatted_info, key, key_renamed, values, values_renamed, add_raw, "None")

"""


#%%
if __name__ == "__main__":
    # Variables and initialization'
    #COURSE_NUMBERS = Utility.get_course_numbers()
    COURSE_NUMBERS = ['01005', '01017']


    # Main loop
    iteration_count = 0
    for course in COURSE_NUMBERS:
        df_location = FileNameConsts.info_df
        df = Utils.load_scraped_df(df_location)

        scraped_info = df.loc[course].to_dict()
        semesters = Config.course_semesters
        file_name = FileNameConsts.info_format
        formatted_info = format_info(scraped_info, course, file_name)

        # print formatted info
        print(formatted_info)

        # Display progress to user
        Utils.display_progress(iteration_count, COURSE_NUMBERS, FileNameConsts.info_format, 200)
        iteration_count += 1 # iteration_count must be incremented AFTER display progress