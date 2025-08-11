from website.global_constants.dtu_consts import DtuConsts

class Info:
    """ Template class, containing the variables that any 'info' should contain """
    def __init__(self, key_1, key_2, key_3, lst_1, lst_2, lst_3, raw):
        self.key_raw = key_1  # Keep this in sync with what's on DTU's website
        self.key_df = key_2  # Custom name for dataframe column
        self.key_url = key_3  # Custom short-name for url-input-filter
        self.values_raw = lst_1  # Keep this in sync with what's on DTU's website
        self.values_df = lst_2  # Custom names for dataframe values
        self.values_url = lst_3  # Custom value short-names for url-filter
        self.add_raw = raw  # Boolean, set as true if info contains a teachers' comment

    @staticmethod
    def contains_values():
        return False


class InfoConsts:

    bsc = "BSc"
    msc = "MSc"
    beng = "BEng"
    phd = "Ph.D."
    deltidsdiplom = "BEng"
    deltidsmaster = "MSc"

    autumn = "Autumn"
    spring = "Spring"
    january = "January"
    june = "June"
    july = "July"
    august = "August"

    exam_written = "Written exam"
    exam_oral = "Oral exam"
    exam_none = "Report hand-in"
    exam_both = "Written/oral exam"

    separator_plus = ' + '
    separator_html = '<br />'
    name_english = "NAME"
    not_yet_assigned_value = "No data available"
    unknown_value = "Unknown data value"
    unspecified_schedule = "Unspecified"
    no_linked_study_lines = "Not linked to any study lines"
    no_responsible = "NO_DATA"
    main_responsible_courses = "MAIN_RESPONSIBLE_COURSES"
    co_responsible_1_courses = "CO_RESPONSIBLE_1_COURSES"
    co_responsible_2_courses = "CO_RESPONSIBLE_2_COURSES"
    co_responsible_3_courses = "CO_RESPONSIBLE_3_COURSES"
    co_responsible_4_courses = "CO_RESPONSIBLE_4_COURSES"
    raw_key = "RAW"

    @staticmethod
    def _danish_name():
        key_raw = DtuConsts.dtu_danish_title  # Decided by DTU's website
        key_df = "DANISH_NAME"
        key_url = "danish"
        values_raw = []  # Decided by DTU's website
        values_df = []
        values_url = []
        add_raw = False
        return Info(key_raw, key_df, key_url, values_raw, values_df, values_url, add_raw)
    danish_name = _danish_name()

    @staticmethod
    def _ects_points():
        key_raw = DtuConsts.dtu_ects_points  # Decided by DTU's website
        key_df = "ECTS_POINTS"
        key_url = "ects"
        values_raw = []  # Decided by DTU's website
        values_df = []
        values_url = []
        add_raw = False
        return Info(key_raw, key_df, key_url, values_raw, values_df, values_url, add_raw)
    ects_points = _ects_points()

    @staticmethod
    def _language():
        key_raw = "Language of instruction"  # Decided by DTU's website
        key_df = "LANGUAGE"
        key_url = "language"
        values_raw = DtuConsts.values_language  # Decided by DTU's website
        values_df = ["Danish", "English"]
        values_url = ["dk", "eng"]
        add_raw = False
        return Info(key_raw, key_df, key_url, values_raw, values_df, values_url, add_raw)
    language = _language()

    @staticmethod
    def _grade_type():
        key_raw = DtuConsts.dtu_evaluation  # Decided by DTU's website
        key_df = "GRADE_TYPE"
        key_url = "gradetype"
        values_raw = DtuConsts.values_evaluation  # Decided by DTU's website
        values_df = ["SEVEN_STEP_SCALE",
                      "SEVEN_STEP_SCALE",
                      "PASS_OR_FAIL",
                      "PASS_OR_FAIL"]
        values_url = ["sevenstep", "passfail"]
        add_raw = False
        return Info(key_raw, key_df, key_url, values_raw, values_df, values_url, add_raw)
    grade_type = _grade_type()

    @staticmethod
    def _examiner():
        key_raw = DtuConsts.dtu_evaluation  # Decided by DTU's website
        key_df = "EXAMINER"
        key_url = "examiner"
        values_raw = DtuConsts.values_evaluation  # Decided by DTU's website
        values_df =  ["EXAMINER_INTERNAL",
                      "EXAMINER_EXTERNAL",
                      "EXAMINER_INTERNAL",
                      "EXAMINER_EXTERNAL"]
        values_url = ["internal", "external"]
        add_raw = False
        return Info(key_raw, key_df, key_url, values_raw, values_df, values_url, add_raw)
    examiner = _examiner()

    @staticmethod
    def _location():
        key_raw = DtuConsts.dtu_location  # Decided by DTU's website
        key_df = "CAMPUS"
        key_url = "campus"
        values_raw = DtuConsts.values_location  # Decided by DTU's website
        values_df = ["CAMPUS_LYNGBY", "CAMPUS_BALLERUP", "CAMPUS_OTHER"]
        values_url = ["lyngby", "ballerup", "elsewhere"]
        add_raw = True
        return Info(key_raw, key_df, key_url, values_raw, values_df, values_url, add_raw)
    location = _location()

    @staticmethod
    def _course_type():
        key_raw = DtuConsts.dtu_course_type  # Decided by DTU's website
        key_df = "COURSE_TYPE"
        key_url = "course_type"
        values_raw = DtuConsts.values_course_type  # Decided by DTU's website
        values_df = ["BSc", "MSc", "MSc", "BEng", "Ph.D.", "BEng", "MSc"]
        values_url = ["bsc", "msc", "beng", "phd"]
        add_raw = False
        return Info(key_raw, key_df, key_url, values_raw, values_df, values_url, add_raw)
    course_type = _course_type()

    @staticmethod
    def _exam_type():
        key_raw = DtuConsts.dtu_type_of_assessment  # Decided by DTU's website
        key_df = "EXAM_TYPE"
        key_url = "exam_type"
        values_raw = DtuConsts.values_exam_type  # Decided by DTU's website
        values_df = ["Written exam",
                      "Written exam",
                      "Written exam",
                      "Written exam",
                      "Oral exam",
                      "Oral exam",
                      "Oral exam",
                      "Oral exam",
                      "Report hand-in",
                      "Report hand-in",
                      "Report hand-in",
                      "Oral exam",
                      "Oral exam",
                      "Report hand-in"]
        values_url = ["written", "oral", "reporthandin"]
        add_raw = True
        return Info(key_raw, key_df, key_url, values_raw, values_df, values_url, add_raw)
    exam_type = _exam_type()

    @staticmethod
    def _assignments():
        key_raw = DtuConsts.dtu_type_of_assessment  # Decided by DTU's website
        key_df = "ASSIGNMENTS"
        key_url = "assignments"
        values_raw = DtuConsts.values_exam_type  # Decided by DTU's website
        values_df = ["No mandatory assignments",
                        "Mandatory reports",
                        "Mandatory exercises",
                        "Mandatory experiments",
                        "No mandatory assignments",
                        "Mandatory reports",
                        "Mandatory exercises",
                        "Mandatory experiments",
                        "Mandatory experiments",
                        "Mandatory reports",
                        "Mandatory experiments",
                        "No mandatory assignments",
                        "No mandatory assignments",
                        "Mandatory reports"]
        values_url = ["noassign", "reports", "exercises", "experiments"]
        add_raw = False
        return Info(key_raw, key_df, key_url, values_raw, values_df, values_url, add_raw)
    assignments = _assignments()

    @staticmethod
    def _exam_aid():
        key_raw = DtuConsts.dtu_aid  # Decided by DTU's website
        key_df = "EXAM_AID"
        key_url = "aid"
        values_raw = DtuConsts.values_exam_aid  # Decided by DTU's website
        values_df = ["All aid", "No computers", "No aid"]
        values_url = ["digitalaid", "analogaid", "noaid"]
        add_raw = True
        return Info(key_raw, key_df, key_url, values_raw, values_df, values_url, add_raw)
    exam_aid = _exam_aid()

    @staticmethod
    def _course_duration():
        key_raw = DtuConsts.dtu_duration_of_course  # Decided by DTU's website
        key_df = "COURSE_DURATION"
        key_url = "course_duration"
        values_raw = DtuConsts.values_duration_of_course  # Decided by DTU's website
        values_df = ["DURATION_13_WEEKS",
                      "DURATION_3_WEEKS",
                      "DURATION_16_WEEKS",
                      "DURATION_16_WEEKS",
                      "DURATION_16_WEEKS",
                      "DURATION_26_WEEKS",
                      "DURATION_26_WEEKS",
                      "DURATION_26_WEEKS",
                      "DURATION_UNIQUE"]
        values_url = ["13week", "3week", "16week", "26week", "xweek"]
        add_raw = False
        return Info(key_raw, key_df, key_url, values_raw, values_df, values_url, add_raw)
    course_duration = _course_duration()

    @staticmethod
    def _time_of_week():
        key_raw = DtuConsts.dtu_schedule  # Decided by DTU's website
        key_df = "TIME_OF_WEEK"
        key_url = "time_of_week"
        values_raw = DtuConsts.values_schedule  # Decided by DTU's website
        values_df = ["Special schedule",
                      "F1A (Spring, Mon 8-12)",
                      "F1B (Spring, Thurs 13-17)",
                      "F2A (Spring, Mon 13-17)",
                      "F2B (Spring, Thurs 8-12)",
                      "F3A (Spring, Tues 8-12)",
                      "F3B (Spring, Fri 13-17)",
                      "F4A (Spring, Tues 13-17)",
                      "F4B (Spring, Fri 8-12)",
                      "F5A (Spring, Wed 8-12)",
                      "F5B (Spring, Wed 13-17)",
                      "F7 (Spring, Tues 18-22)",
                      "Special schedule",
                      "E1A (Autumn, Mon 8-12)",
                      "E1B (Autumn, Thurs 13-17)",
                      "E2A (Autumn, Mon 13-17)",
                      "E2B (Autumn, Thurs 8-12)",
                      "E3A (Autumn, Tues 8-12)",
                      "E3B (Autumn, Fri 13-17)",
                      "E4A (Autumn, Tues 13-17)",
                      "E4B (Autumn, Fri 8-12)",
                      "E5A (Autumn, Wed 8-12)",
                      "E5B (Autumn, Wed 13-17)",
                      "E7 (Autumn, Tues 18-22)",
                      "3-week January",
                      "3-week June",
                      "3-week July",
                      "3-week August"]
        values_url = ["offschedule",
                      "F1A", "F1B", "F2A", "F2B", "F3A",
                      "F3B", "F4A", "F4B", "F5A", "F5B", "F7",
                      "E1A", "E1B", "E2A", "E2B", "E3A",
                      "E3B", "E4A", "E4B", "E5A", "E5B", "E7",
                      "W3january",
                      "W3june",
                      "W3july",
                      "W3august"]
        add_raw = False
        return Info(key_raw, key_df, key_url, values_raw, values_df, values_url, add_raw)
    time_of_week = _time_of_week()

    @staticmethod
    def _time_of_week_updated():
        key_raw = DtuConsts.dtu_schedule  # Decided by DTU's website
        key_df = "TIMETABLE_PLACEMENT"
        key_url = "timetable"
        values_raw = DtuConsts.values_schedule  # Decided by DTU's website
        values_df = ["Special schedule",
                      "1A Mon 8-12", "1B Thurs 13-17",
                      "2A Mon 13-17", "2B Thurs 8-12",
                      "3A Tues 8-12", "3B Fri 13-17",
                      "4A Tues 13-17", "4B Fri 8-12",
                      "5A Wed 8-12", "5B Wed 13-17", "7 Tues 18-22",
                      "Special schedule",
                      "1A Mon 8-12", "1B Thurs 13-17",
                      "2A Mon 13-17", "2B Thurs 8-12",
                      "3A Tues 8-12", "3B Fri 13-17",
                      "4A Tues 13-17", "4B Fri 8-12",
                      "5A Wed 8-12", "5B Wed 13-17", "7 Tues 18-22",
                      "3-week", "3-week",
                      "3-week", "3-week"]
        values_url = ["offschedule",
                      "Mon 8-12", "Thu 13-17",
                      "Mon 13-17", "Thu 8-12",
                      "Tue 8-12", "Fri 13-17",
                      "Tue 13-17", "Fri 8-12",
                      "Wed 8-12", "Wed 13-17", "Tue 18-22",
                      "3-week"]
        add_raw = False
        return Info(key_raw, key_df, key_url, values_raw, values_df, values_url, add_raw)
    time_of_week_updated = _time_of_week_updated()

    @staticmethod
    def _semester_period():
        key_raw = DtuConsts.dtu_schedule  # Decided by DTU's website
        key_df = "SEMESTER_PERIOD"
        key_url = "semester_period"
        values_raw = DtuConsts.values_schedule  # Decided by DTU's website
        values_df = ["Spring", "Spring", "Spring", "Spring", "Spring", "Spring",
                      "Spring", "Spring", "Spring", "Spring", "Spring", "Spring",
                      "Autumn", "Autumn", "Autumn", "Autumn", "Autumn", "Autumn",
                      "Autumn", "Autumn", "Autumn", "Autumn", "Autumn", "Autumn",
                      "January", "June", "July", "August"]
        values_url = ["spring", "autumn", "jan", "jun", "jul", "aug"]
        add_raw = False
        return Info(key_raw, key_df, key_url, values_raw, values_df, values_url, add_raw)
    semester_period = _semester_period()

    @staticmethod
    def _study_lines():
        key_raw = DtuConsts.dtu_accosiated_study_lines  # Decided by DTU's website
        key_df = "STUDY_LINES"
        key_url = "study_lines"
        values_raw = ["BEng, Architectural Engineering",
                    "BEng, Arctic Civil Engineering",
                    "BEng, Chemical Engineering and International Business",
                    "BEng, Chemical and Bio Engineering",
                    "BEng, Civil Engineering",
                    "BEng, Computer Engineering", ##
                    "BEng, Electrical Energy Technology",
                    "BEng, Electrical Engineering",
                    "BEng, Fisheries Technology",
                    "BEng, Food Safety and Quality",
                    "BEng, Global Business Engineering",
                    "BEng, Healthcare Technology",
                    "BEng, IT and Economics",
                    "BEng, Manufacturing and Management",
                    "BEng, Mechanical Engineering",
                    "BEng, Mobility, Transport and Logistics",
                    "BEng, Naval Architecture and Offshore Engineering", ##
                    "BEng, Process and Innovation",
                    "BEng, Software Technology",
                    "BSc, Architectural Engineering",
                    "BSc, Artificial Intelligence and Data",
                    "BSc, Biomedical Engineering",
                    "BSc, Chemistry and Technology",
                    "BSc, Civil Engineering",
                    "BSc, Computer Engineering",
                    "BSc, Cybertechnology",
                    "BSc, Data Science and Management",
                    "BSc, Design and Innovation",
                    "BSc, Design of Sustainable Energy Systems",
                    "BSc, Earth and Space Physics and Engineering",
                    "BSc, Electrical Engineering",
                    "BSc, Engineering Physics",
                    "BSc, Environmental Engineering",
                    "BSc, General Engineering",
                    "BSc, Human Life Science Engineering",
                    "BSc, Life Science and Technology",
                    "BSc, Mathematics and Technology",
                    "BSc, Mechanical Engineering",
                    "BSc, Software Technology",
                    "BSc, Sustainable Energy Design",
                    "MSc, Applied Chemistry",
                    "MSc, Architectural Engineering",
                    "MSc, Autonomous Systems",
                    "MSc, Bioinformatics and Systems Biology",
                    "MSc, Biomaterial Engineering for Medicine",
                    "MSc, Biomedical Engineering",
                    "MSc, Biotechnology",
                    "MSc, Business Analytics",
                    "MSc, Chemical and Biochemical Engineering",
                    "MSc, Civil Engineering",
                    "MSc, Communication Technologies and System Design",
                    "MSc, Computer Science and Engineering",
                    "MSc, Design and Innovation",
                    "MSc, Earth and Space Physics and Engineering",
                    "MSc, Electrical Engineering",
                    "MSc, Engineering Acoustics",
                    "MSc, Engineering Light",
                    "MSc, Engineering Physics",
                    "MSc, Environmental Engineering",
                    "MSc, Food Technology",
                    "MSc, Human Centered Artificial Intelligence",
                    "MSc, Industrial Engineering and Management",
                    "MSc, Materials and Manufacturing Engineering",
                    "MSc, Mathematical Modelling and Computation",
                    "MSc, Mechanical Engineering",
                    "MSc, Ocean Engineering",
                    "MSc, Pharmaceutical Design and Engineering",
                    "MSc, Quantitative Biology and Disease Modelling", #
                    "MSc, Sustainable Energy", #DELETE
                    "MSc, Sustainable Energy Systems",
                    "MSc, Sustainable Energy Technologies",
                    "MSc, Sustainable Fisheries and Aquaculture",
                    "MSc, Transport and Logistics", #
                    "MSc, Technology Entrepreneurship",
                    "MSc, Wind Energy"]  # Decided by DTU's website
        values_df = values_raw + ["NO_STUDYLINE"]

        def shorten_study_lines(study_line_lst):
            # Remove all lowercase letters
            new_lst = []
            for element in study_line_lst:
                modified_element = element
                modified_element = modified_element.replace("BEng, ","BENG_")
                modified_element = modified_element.replace("BSc, ","BSC_")
                modified_element = modified_element.replace("MSc, ","MSC_")
                new_element = ""
                for char in modified_element:
                    if char.isupper() or char == "_":
                        new_element += char
                new_lst.append(new_element)

            # Rename duplicate elements in list (add a number to the end)
            no_duplicates = []
            for i, v in enumerate(new_lst):
                totalcount = new_lst.count(v)
                count = new_lst[:i].count(v)
                no_duplicates.append(v + str(count + 1) if totalcount > 1 else v)
            return no_duplicates

        values_url = shorten_study_lines(values_raw) + ["no_studyline"]
        add_raw = True
        return Info(key_raw, key_df, key_url, values_raw, values_df, values_url, add_raw)
    study_lines = _study_lines()

    @staticmethod
    def _old_recommended_prerequisites():
        key_raw = DtuConsts.dtu_old_recommended_prerequisites  # Decided by DTU's website
        key_df = "LEGACY_RECOMMENDED_PREREQUISITES"
        key_url = "old_rec_prereq"
        values_raw = []  # Decided by DTU's website
        values_df = []
        values_url = []
        add_raw = False
        return Info(key_raw, key_df, key_url, values_raw, values_df, values_url, add_raw)
    old_recommended_prerequisites = _old_recommended_prerequisites()

    @staticmethod
    def _recommended_prerequisites():
        key_raw = DtuConsts.dtu_recommended_prerequisites  # Decided by DTU's website
        key_df = "RECOMMENDED_PREREQUISITES"
        key_url = "rec_prereq"
        values_raw = []  # Decided by DTU's website
        values_df = []
        values_url = []
        add_raw = False
        return Info(key_raw, key_df, key_url, values_raw, values_df, values_url, add_raw)
    recommended_prerequisites = _recommended_prerequisites()

    @staticmethod
    def _mandatory_prerequisites():
        key_raw = DtuConsts.dtu_mandatory_prerequisites  # Decided by DTU's website
        key_df = "MANDATORY_PREREQUISITES"
        key_url = "mand_prereq"
        values_raw = []  # Decided by DTU's website
        values_df = []
        values_url = []
        add_raw = False
        return Info(key_raw, key_df, key_url, values_raw, values_df, values_url, add_raw)
    mandatory_prerequisites = _mandatory_prerequisites()

    @staticmethod
    def _course_description():
        key_raw = DtuConsts.dtu_general_course_objectives  # Decided by DTU's website
        key_df = "COURSE_DESCRIPTION"
        key_url = "description"
        values_raw = []  # Decided by DTU's website
        values_df = []
        values_url = []
        add_raw = False
        return Info(key_raw, key_df, key_url, values_raw, values_df, values_url, add_raw)
    course_description = _course_description()

    @staticmethod
    def _learning_objectives():
        key_raw = DtuConsts.dtu_learning_objectives  # Decided by DTU's website
        key_df = "LEARNING_OBJECTIVES"
        key_url = "learn_obj"
        values_raw = []  # Decided by DTU's website
        values_df = []
        values_url = []
        add_raw = False
        return Info(key_raw, key_df, key_url, values_raw, values_df, values_url, add_raw)
    learning_objectives = _learning_objectives()

    @staticmethod
    def _course_content():
        key_raw = DtuConsts.dtu_content  # Decided by DTU's website
        key_df = "COURSE_CONTENT"
        key_url = "content"
        values_raw = []  # Decided by DTU's website
        values_df = []
        values_url = []
        add_raw = False
        return Info(key_raw, key_df, key_url, values_raw, values_df, values_url, add_raw)
    course_content = _course_content()

    @staticmethod
    def _remarks():
        key_raw = DtuConsts.dtu_remarks  # Decided by DTU's website
        key_df = "REMARKS"
        key_url = "remarks"
        values_raw = []  # Decided by DTU's website
        values_df = []
        values_url = []
        add_raw = False
        return Info(key_raw, key_df, key_url, values_raw, values_df, values_url, add_raw)
    remarks = _remarks()

    @staticmethod
    def _highlighted_message():
        key_raw = DtuConsts.dtu_highlighted_message  # In this case, NOT decided by DTU's website
        key_df = "HIGHLIGHTED_MESSAGE"
        key_url = "highlighted_message"
        values_raw = []  # Decided by DTU's website
        values_df = []
        values_url = []
        add_raw = False
        return Info(key_raw, key_df, key_url, values_raw, values_df, values_url, add_raw)
    highlighted_message = _highlighted_message()

    @staticmethod
    def _last_updated():
        key_raw = DtuConsts.dtu_last_updated  # Decided by DTU's website
        key_df = "LAST_UPDATED"
        key_url = "last_update"
        values_raw = []  # Decided by DTU's website
        values_df = []
        values_url = []
        add_raw = False
        return Info(key_raw, key_df, key_url, values_raw, values_df, values_url, add_raw)
    last_updated = _last_updated()

    @staticmethod
    def _scope_and_form():
        key_raw = DtuConsts.dtu_scope_and_form  # Decided by DTU's website
        key_df = "SCOPE_AND_FORM"
        key_url = "scope"
        values_raw = []  # Decided by DTU's website
        values_df = []
        values_url = []
        add_raw = False
        return Info(key_raw, key_df, key_url, values_raw, values_df, values_url, add_raw)
    scope_and_form = _scope_and_form()

    @staticmethod
    def _exam_duration():
        key_raw = DtuConsts.dtu_exam_duration  # Decided by DTU's website
        key_df = "EXAM_DURATION"
        key_url = "exam_duration"
        values_raw = []  # Decided by DTU's website
        values_df = []
        values_url = []
        add_raw = False
        return Info(key_raw, key_df, key_url, values_raw, values_df, values_url, add_raw)
    exam_duration = _exam_duration()

    @staticmethod
    def _home_page():
        key_raw = DtuConsts.dtu_home_page  # Decided by DTU's website
        key_df = "HOME_PAGE"
        key_url = "webpage"
        values_raw = []  # Decided by DTU's website
        values_df = []
        values_url = []
        add_raw = False
        return Info(key_raw, key_df, key_url, values_raw, values_df, values_url, add_raw)
    home_page = _home_page()

    @staticmethod
    def _previous_course():
        key_raw = DtuConsts.dtu_previous_course  # Decided by DTU's website
        key_df = "PREVIOUS_COURSE"
        key_url = ""
        values_raw = []  # Decided by DTU's website
        values_df = []
        values_url = []
        add_raw = False
        return Info(key_raw, key_df, key_url, values_raw, values_df, values_url, add_raw)
    previous_course = _previous_course()

    @staticmethod
    def _registration_sign_up():
        key_raw = DtuConsts.dtu_registration_sigh_up  # Decided by DTU's website
        key_df = "SIGN_UP_LOCATION"
        key_url = ""
        values_raw = []  # Decided by DTU's website
        values_df = []
        values_url = []
        add_raw = False
        return Info(key_raw, key_df, key_url, values_raw, values_df, values_url, add_raw)
    registration_sign_up = _registration_sign_up()

    @staticmethod
    def _not_applicable_together_with():
        key_raw = DtuConsts.dtu_not_applicable_together_with  # Decided by DTU's website
        key_df = "COURSE_POINT_LOCK"
        key_url = ""
        values_raw = []  # Decided by DTU's website
        values_df = []
        values_url = []
        add_raw = False
        return Info(key_raw, key_df, key_url, values_raw, values_df, values_url, add_raw)
    not_applicable_together_with = _not_applicable_together_with()

    @staticmethod
    def _green_challenge():
        key_raw = DtuConsts.dtu_green_challenge_participation # Decided by DTU's website
        key_df = "GREEN_CHALLENGE"
        key_url = ""
        values_raw = []  # Decided by DTU's website
        values_df = []
        values_url = []
        add_raw = False
        return Info(key_raw, key_df, key_url, values_raw, values_df, values_url, add_raw)
    green_challenge = _green_challenge()

    @staticmethod
    def _department_responsible():
        key_raw = DtuConsts.dtu_department  # Decided by DTU's website
        key_df = "DEPARTMENT_RESPONSIBLE"
        key_url = ""
        values_raw = []  # Decided by DTU's website
        values_df = []
        values_url = []
        add_raw = False
        return Info(key_raw, key_df, key_url, values_raw, values_df, values_url, add_raw)
    department_responsible = _department_responsible()

    @staticmethod
    def _departments_involved():
        key_raw = DtuConsts.dtu_departments_involved  # Decided by DTU's website
        key_df = "DEPARTMENTS_INVOLVED"
        key_url = ""
        values_raw = []  # Decided by DTU's website
        values_df = []
        values_url = []
        add_raw = False
        return Info(key_raw, key_df, key_url, values_raw, values_df, values_url, add_raw)
    departments_involved = _departments_involved()

    @staticmethod
    def _external_institution():
        key_raw = DtuConsts.dtu_external_institution  # Decided by DTU's website
        key_df = "EXTERNAL_INSTITUTES"
        key_url = ""
        values_raw = []  # Decided by DTU's website
        values_df = []
        values_url = []
        add_raw = False
        return Info(key_raw, key_df, key_url, values_raw, values_df, values_url, add_raw)
    external_institution = _external_institution()

    @staticmethod
    def _date_of_examination():
        key_raw = DtuConsts.dtu_date_of_examination  # Decided by DTU's website
        key_df = "EXAM_DATE"
        key_url = ""
        values_raw = []  # Decided by DTU's website
        values_df = []
        values_url = []
        add_raw = False
        return Info(key_raw, key_df, key_url, values_raw, values_df, values_url, add_raw)
    date_of_examination = _date_of_examination()

    @staticmethod
    def _course_main_responsible_contact():
        key_raw = DtuConsts.dtu_responsible  # Decided by DTU's website
        key_df = "COURSE_MAIN_RESPONSIBLE_CONTACT"
        key_url = ""
        values_raw = []  # Decided by DTU's website
        values_df = []
        values_url = []
        add_raw = False
        return Info(key_raw, key_df, key_url, values_raw, values_df, values_url, add_raw)
    course_main_responsible_contact = _course_main_responsible_contact()

    @staticmethod
    def _course_co_responsible_contact():
        key_raw = DtuConsts.dtu_course_co_responsible  # Decided by DTU's website
        key_df = "COURSE_CO_RESPONSIBLE_CONTACT"
        key_url = ""
        values_raw = []  # Decided by DTU's website
        values_df = []
        values_url = []
        add_raw = False
        return Info(key_raw, key_df, key_url, values_raw, values_df, values_url, add_raw)
    course_co_responsible_contact = _course_co_responsible_contact()

    @staticmethod
    def _institute():
        key_raw = DtuConsts.dtu_institute #DOES NOT EXIST FOR INSTITUTE, institute is decided based on course number only
        key_df = "INSTITUTE"
        key_url = "institute"
        values_raw = ["01", "02", "10", "56", "12",
                      "22", "23", "CB", "25", "26", "27",
                      "29", "28", "88", "30", "31", "34",
                      "41", "42", "38", "46", "63", "47", "62", "MA", "KU"]
        values_df = ["Applied Mathematics", #01
                    "Computer Science", #02
                    "Physics", #10
                    "Physics", #56
                    "Environmental Engineering", #12
                    "Health Technology", #22
                    "National Food Institute", #23
                    "National Food Institute", #CB
                    "Aquatic Resources", #25
                    "Chemistry", # 26
                    "Biotechnology and Biomedicine", #27
                    "Biotechnology and Biomedicine", #29
                    "Chemical Engineering", #28
                    "Chemical Engineering", #88
                    "National Space Institute", #30
                    "Electrical Engineering", #31
                    "Photonics Engineering", #34
                    "Mechanical Engineering", #41
                    "Management and Economics", #42
                    "Management and Economics", #38
                    "Wind Energy", #46
                    "Wind Energy", #63
                    "Energy Conversion and Storage", #47
                    "BEng - Bachelor of Engineering", #62
                    "BEng - Bachelor of Engineering", #MA
                    "KU - Copenhagen University"] #KU
        values_url = ["01", "02", "10", "12",
                      "22", "23", "25", "26", "27",
                      "29", "30", "31", "34", "41",
                      "42", "46", "47", "62", "KU"]
        add_raw = False
        return Info(key_raw, key_df, key_url, values_raw, values_df, values_url, add_raw)
    institute = _institute()

    @staticmethod
    def _course_responsible(raw_key, df_key):
        key_raw = raw_key
        key_df = df_key
        key_url = ""
        values_raw = []
        values_df = []
        values_url = []
        add_raw = False
        return Info(key_raw, key_df, key_url, values_raw, values_df, values_url, add_raw)

    # Name and picture of course responsibles
    main_responsible_name = _course_responsible(DtuConsts.dtu_name_of_main_responsible,
                                                "MAIN_RESPONSIBLE_NAME")
    main_responsible_pic = _course_responsible(DtuConsts.dtu_pic_of_main_responsible,
                                                "MAIN_RESPONSIBLE_PIC")
    co_responsible_1_name = _course_responsible(DtuConsts.dtu_name_of_co_responsible_1,
                                                "CO_RESPONSIBLE_1_NAME")
    co_responsible_1_pic = _course_responsible(DtuConsts.dtu_pic_of_co_responsible_1,
                                                "CO_RESPONSIBLE_1_PIC")
    co_responsible_2_name = _course_responsible(DtuConsts.dtu_name_of_co_responsible_2,
                                                "CO_RESPONSIBLE_2_NAME")
    co_responsible_2_pic = _course_responsible(DtuConsts.dtu_pic_of_co_responsible_2,
                                                "CO_RESPONSIBLE_2_PIC")
    co_responsible_3_name = _course_responsible(DtuConsts.dtu_name_of_co_responsible_3,
                                                "CO_RESPONSIBLE_3_NAME")
    co_responsible_3_pic = _course_responsible(DtuConsts.dtu_pic_of_co_responsible_3,
                                                "CO_RESPONSIBLE_3_PIC")
    co_responsible_4_name = _course_responsible(DtuConsts.dtu_name_of_co_responsible_4,
                                                "CO_RESPONSIBLE_4_NAME")
    co_responsible_4_pic = _course_responsible(DtuConsts.dtu_pic_of_co_responsible_4,
                                                "CO_RESPONSIBLE_4_PIC")

    info_to_format = [danish_name,
                      ects_points,
                      language,
                      grade_type,
                      examiner,
                      location,
                      course_type,
                      exam_type,
                      exam_aid,
                      assignments,
                      course_duration,
                      time_of_week,
                      time_of_week_updated,
                      semester_period,
                      study_lines,
                      old_recommended_prerequisites,
                      recommended_prerequisites,
                      mandatory_prerequisites,
                      course_description,
                      learning_objectives,
                      course_content,
                      remarks,
                      highlighted_message,
                      last_updated,
                      scope_and_form,
                      exam_duration,
                      home_page,
                      previous_course,
                      registration_sign_up,
                      not_applicable_together_with,
                      green_challenge,
                      department_responsible,
                      departments_involved,
                      external_institution,
                      date_of_examination,
                      course_main_responsible_contact,
                      course_co_responsible_contact,
                      institute,
                      main_responsible_name,
                      main_responsible_pic,
                      co_responsible_1_name,
                      co_responsible_1_pic,
                      co_responsible_2_name,
                      co_responsible_2_pic,
                      co_responsible_3_name,
                      co_responsible_3_pic,
                      co_responsible_4_name,
                      co_responsible_4_pic]

    scrape_info_column_names = [element.key_raw for element in info_to_format]