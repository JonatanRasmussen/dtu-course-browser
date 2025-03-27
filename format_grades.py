#%%

# Imports
# Helper functions and global constants
from utils import Utils
from website.global_constants.config import Config
from website.global_constants.file_name_consts import FileNameConsts
from website.global_constants.grade_consts import GradeConsts


def format_grades(scraped_grades, course_number, course_semesters, file_name):
    """Return formatted scraped grades and calculate statistics"""

    # Initialization
    GRADE_12 = GradeConsts.grade_12
    GRADE_10 = GradeConsts.grade_10
    GRADE_7 = GradeConsts.grade_7
    GRADE_4 = GradeConsts.grade_4
    GRADE_02 = GradeConsts.grade_02
    GRADE_00 = GradeConsts.grade_00
    GRADE_MINUS_3 = GradeConsts.grade_minus_3
    PASSED = GradeConsts.grade_passed
    FAILED = GradeConsts.grade_failed
    ABSENT = GradeConsts.grade_absent
    AVERAGE_GRADE = GradeConsts.grade_average
    PERCENT_PASSED = GradeConsts.percent_passed
    PERCENT_FAILED = GradeConsts.percent_failed
    PERCENT_ABSENT = GradeConsts.percent_absent
    TOTAL_STUDENTS = GradeConsts.students_total
    STUDENTS_PER_SEMESTER = GradeConsts.students_per_semester
    TOTAL_SEMESTERS = GradeConsts.semesters_total
    NO_GRADES = GradeConsts.grade_none
    PASS_FAIL = GradeConsts.pass_fail

    def find_grade_average(grade_count):
        """Calculate and return average value of grades in a dict"""
        NUMERIC_GRADES = [GRADE_12, GRADE_10, GRADE_7, GRADE_4, GRADE_02, GRADE_00, GRADE_MINUS_3]
        PASS_FAIL_GRADES = [PASSED, FAILED, ABSENT]
        GRADE_WEIGHT = [12, 10, 7, 4, 2, 0, -3]
        grade_weighted = 0
        numeric_grade_count = 0
        any_grade_count = 0

        # Loop through each grades and weight them
        for i in range (0, len(NUMERIC_GRADES)):
            grade_weighted += grade_count[NUMERIC_GRADES[i]] * GRADE_WEIGHT[i]
            numeric_grade_count += grade_count[NUMERIC_GRADES[i]]
            any_grade_count += grade_count[NUMERIC_GRADES[i]]
        for i in range (0, len(PASS_FAIL_GRADES)):
            any_grade_count += grade_count[PASS_FAIL_GRADES[i]]

        # Don't divide by 0 or find average on PASSED/FAILED course type
        # Note that some PASSED/FAILED courses might contain up to 10% numeric grades (happens due to DTU rules)
        if any_grade_count == 0:
            grade_average = NO_GRADES
        elif numeric_grade_count * 10 <= (grade_count[PASSED] + grade_count[FAILED]):
            grade_average = PASS_FAIL
        else:
            grade_average = round(float(grade_weighted / numeric_grade_count), Config.data_decimal_precision)

        return grade_average

    def exam_percentage_passed(grade_count):
        """Return percentage of students that passed the exam"""
        PASSED_GRADES = [GRADE_12, GRADE_10, GRADE_7, GRADE_4, GRADE_02, PASSED]
        FAILED_GRADES = [GRADE_00, GRADE_MINUS_3, FAILED]
        ABSENT_GRADES = [ABSENT]
        passed_count = 0
        failed_count = 0
        absent_count = 0

        # Count grades
        for i in range (0, len(PASSED_GRADES)):
            passed_count += grade_count[PASSED_GRADES[i]]
        for i in range (0, len(FAILED_GRADES)):
            failed_count += grade_count[FAILED_GRADES[i]]
        for i in range (0, len(ABSENT_GRADES)):
            absent_count += grade_count[ABSENT_GRADES[i]]
        total_count = passed_count + failed_count + absent_count

        # Avoid division by 0 if course has no exam
        if total_count == 0:
            passed_exam_percent = NO_GRADES
            failed_exam_percent = NO_GRADES
            dropout_exam_percent = NO_GRADES
        else:
            passed_exam_percent = round(float(100 * (passed_count / total_count)), Config.data_percental_precision)
            failed_exam_percent = round(float(100 * (failed_count / total_count)), Config.data_percental_precision)
            dropout_exam_percent = round(float(100 * (absent_count / total_count)), Config.data_percental_precision)

        return (passed_exam_percent, failed_exam_percent, dropout_exam_percent)

    def create_statistics_dict(grade_count, semester):
        """ Performs a total of 3 calculations and returns the results as a dictionary:
            A) Find total number of students by summing up all the grades,
            B) Calculate the average grade,
            C) Calculate the percent of students passed / failed / absent"""
        number_of_students = sum(grade_count.values())
        grade_average = find_grade_average(grade_count)
        passed, failed, absent = exam_percentage_passed(grade_count)
        stat_dict = {semester+TOTAL_STUDENTS: number_of_students,
                     semester+AVERAGE_GRADE: grade_average,
                     semester+PERCENT_PASSED: passed,
                     semester+PERCENT_FAILED: failed,
                     semester+PERCENT_ABSENT: absent}
        return stat_dict

    def number_of_semesters(dct):
        """ Get number of semesters based on grades assigned at each exam period
            Note: the datatype 'list' is used to track amount of students for each semester """
        lst_of_number_of_students = []
        lst_of_number_of_failed_students = []

        # Count number of students for each exam period
        for i in range (0, len(course_semesters)):
            number_of_students = course_semesters[i]+'_'+TOTAL_STUDENTS
            if number_of_students in dct and dct[number_of_students] != 0:
                lst_of_number_of_students.append(dct[number_of_students])
                number_of_passed_students = course_semesters[i]+'_'+PERCENT_PASSED
                lst_of_number_of_failed_students.append(1 - (dct[number_of_passed_students]/100))
        if len(lst_of_number_of_students) == 0:
            stat_dct = {STUDENTS_PER_SEMESTER: 0, TOTAL_SEMESTERS: 0}
            return stat_dct
        else:
            # Some exam periods might be re-exam only, and should not count
            # as a semester. If exam attendance is way below average and
            # most students pass, it is probably a re-exam, not a semester
            avg_students = float(sum(lst_of_number_of_students)/len(lst_of_number_of_students))
            avg_not_passed = float(sum(lst_of_number_of_failed_students)/len(lst_of_number_of_failed_students))
            lst_of_number_of_real_semesters = []
            for i in range(0, len(lst_of_number_of_students)):
                if lst_of_number_of_students[i] > avg_students*(0.05 + avg_not_passed)*1.5:
                    lst_of_number_of_real_semesters.append(lst_of_number_of_students[i])

            # Return semester count and average enrolled students
            semesters = len(lst_of_number_of_real_semesters)
            if semesters == 0:
                enrolled = 0
            else:
                enrolled = int(round(float(sum(lst_of_number_of_real_semesters)/semesters)))
            stat_dct = {STUDENTS_PER_SEMESTER: enrolled, TOTAL_SEMESTERS: semesters}
            return stat_dct




#%%
    # Initialization
    grade_count_all_semesters = {GRADE_12: 0, GRADE_10: 0, GRADE_7: 0, GRADE_4: 0, GRADE_02: 0, GRADE_00: 0, GRADE_MINUS_3: 0, PASSED: 0, FAILED: 0, ABSENT: 0}
    course_grades = {}
    semester_grades = {}

    # Loop through all possible semester and grade combinations
    for semester in course_semesters:
        grade_count_this_semester = {GRADE_12: 0, GRADE_10: 0, GRADE_7: 0, GRADE_4: 0, GRADE_02: 0, GRADE_00: 0, GRADE_MINUS_3: 0, PASSED: 0, FAILED: 0, ABSENT: 0}
        for grade in GradeConsts.list_of_grades:

            key = semester+'_'+str(grade)
            if (key in scraped_grades) and (scraped_grades[key] != Config.data_null_value) and (scraped_grades[key] != GradeConsts.grade_none):
                grade_count_all_semesters[grade] += int(scraped_grades[key])
                grade_count_this_semester[grade] += int(scraped_grades[key])

        # Merge grades and grade statistics for each semester into one dict
        semester_grade_stats = create_statistics_dict(grade_count_this_semester, semester+'_')
        semester_grades = {**semester_grades, **semester_grade_stats}

        # Rename dictionary keys from GRADE_XX to SEMESTER_GRADE_XX
        grade_count_this_semester = Utils.rename_dict_keys(grade_count_this_semester, semester+'_', '')
        semester_grades = {**semester_grades, **grade_count_this_semester}

    # Merge raw data and statistics for entire course into one dict
    course_grade_stats = create_statistics_dict(grade_count_all_semesters, '')
    course_grades = {**course_grades, **course_grade_stats}
    course_grades = {**course_grades, **grade_count_all_semesters}


    # Merge semester-specific and non-semester-specific data into one dict
    enrolled_dct = number_of_semesters(semester_grades)
    grades = {**course_grades, **enrolled_dct}
    grades = {**grades, **semester_grades}

    return grades


#%%
if __name__ == "__main__":
    # Variables and initialization'
    #COURSE_NUMBERS = Utility.get_course_numbers()
    COURSE_NUMBERS = ['01005', '01017']


    # Main loop
    iteration_count = 0
    for course in COURSE_NUMBERS:
        df_location = FileNameConsts.grade_df
        df = Utils.load_scraped_df(df_location)

        scraped_grades = df.loc[course].to_dict()
        semesters = Config.course_semesters
        file_name = FileNameConsts.grade_format
        formatted_grades = format_grades(scraped_grades, course, semesters, file_name)

        # print formatted grades
        print(formatted_grades)

        # Display progress to user
        Utils.display_progress(iteration_count, COURSE_NUMBERS, FileNameConsts.grade_format, 200)
        iteration_count += 1 # iteration_count must be incremented AFTER display progress
