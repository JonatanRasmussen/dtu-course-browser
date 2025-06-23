

class DtuConsts:
    # DTU terms
    dtu_term_spring = "F"  # Foraar in danish
    dtu_term_autumn = "E"  # Efteraar in danish

    # DTU-variables, these MUST match the row indexes on dtu course base
    dtu_aid = "Aid"
    dtu_content = "Content"
    dtu_course_co_responsible = "Course co-responsible"
    dtu_course_type = "Course type"
    dtu_danish_title = "Danish title"
    dtu_date_of_examination = "Date of examination"
    dtu_department = "Department"
    dtu_departments_involved = "Department involved"
    dtu_duration_of_course = "Duration of Course"
    dtu_ects_points = "Point( ECTS )"
    dtu_evaluation = "Evaluation"
    dtu_exam_duration = "Exam duration"
    dtu_external_institution = "External Institution"
    dtu_general_course_objectives = "General course objectives"
    dtu_green_challenge_participation = "Green challenge participation"
    dtu_home_page = "Home page"
    dtu_language_of_instruction = "Language of instruction"
    dtu_last_updated = "Last updated"
    dtu_learning_objectives = "Learning objectives"
    dtu_location = "Location"
    dtu_mandatory_prerequisites = "Mandatory Prerequisites"
    dtu_not_applicable_together_with = "Not applicable together with"
    dtu_previous_course = "Previous Course"
    dtu_recommended_prerequisites = "Recommended Academic prerequisites"
    dtu_registration_sigh_up = "Registration Sign up"
    dtu_remarks = "Remarks"
    dtu_highlighted_message = "Highlighted Message"
    dtu_responsible = "Responsible"
    dtu_schedule = "Schedule"
    dtu_scope_and_form = "Scope and form"
    dtu_type_of_assessment = "Type of assessment"


    # Custom-named variables, these can be whatever but a new scrape must be performed if changed
    dtu_accosiated_study_lines = "Study lines"
    dtu_institute = "Institute"
    dtu_name_of_main_responsible = "Main responsible name"
    dtu_name_of_co_responsible_1 = "Co responsible name 1"
    dtu_name_of_co_responsible_2 = "Co responsible name 2"
    dtu_name_of_co_responsible_3 = "Co responsible name 3"
    dtu_name_of_co_responsible_4 = "Co responsible name 4"
    dtu_pic_of_main_responsible = "Main responsible pic"
    dtu_pic_of_co_responsible_1 = "Co responsible pic 1"
    dtu_pic_of_co_responsible_2 = "Co responsible pic 2"
    dtu_pic_of_co_responsible_3 = "Co responsible pic 3"
    dtu_pic_of_co_responsible_4 = "Co responsible pic 4"
    dtu_no_data_for_responsible = "NO_DATA"
    dtu_no_remarks = "None"
    dtu_no_highlighted_message = "None"


    # DTU-values, these MUST match the values found on dtu course base
    values_course_type = ["BSc", "MSc", "BScMSc", "BEng", "Ph.D.", "Deltidsdiplom", "Parttime master"]
    values_language = ["Danish", "English"]
    values_location = ["Campus Lyngby", "Campus Ballerup"]
    values_exam_aid = ["All Aid",
                        "Written works of reference are permitted",
                        "No Aid"]
    values_exam_type = ["Written examination",
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
    values_evaluation = ["7 step scale , internal examiner",
                        "7 step scale , external examiner",
                        "pass / not pass , internal examiner",
                        "pass / not pass , external examiner"]
    values_duration_of_course = ["13 weeks",
                                "3 weeks",
                                "13 weeks + 3 weeks",
                                "3 weeks + 13 weeks",
                                "13 weeks or 3 weeks",
                                "13 weeks + 13 weeks",
                                "13 weeks + 3 weeks + 13 weeks",
                                "13 weeks + 3 weeks + 13 weeks + 3 weeks",
                                "[The course is not following DTUs normal Schedule]"]
    values_schedule = ["Spring",
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