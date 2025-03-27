#%%

# Imports
import pandas as pd
from utils import Utils
# Helper functions and global constants
from website.global_constants.file_name_consts import FileNameConsts
from website.global_constants.info_consts import InfoConsts


# Initialization
STUDY_LINES = InfoConsts.study_lines
MAIN_RESPONSIBLE_NAME = InfoConsts.main_responsible_name.key_df
MAIN_RESPONSIBLE_PIC = InfoConsts.main_responsible_pic.key_df
CO_RESPONSIBLE_1_NAME = InfoConsts.co_responsible_1_name.key_df
CO_RESPONSIBLE_1_PIC = InfoConsts.co_responsible_1_pic.key_df
CO_RESPONSIBLE_2_NAME = InfoConsts.co_responsible_2_name.key_df
CO_RESPONSIBLE_2_PIC = InfoConsts.co_responsible_2_pic.key_df
CO_RESPONSIBLE_3_NAME = InfoConsts.co_responsible_3_name.key_df
CO_RESPONSIBLE_3_PIC = InfoConsts.co_responsible_3_pic.key_df
CO_RESPONSIBLE_4_NAME = InfoConsts.co_responsible_4_name.key_df
CO_RESPONSIBLE_4_PIC = InfoConsts.co_responsible_4_pic.key_df
NO_RESPONSIBLE = InfoConsts.no_responsible
MAIN_RESPONSIBLE_COURSES = InfoConsts.main_responsible_courses
CO_RESPONSIBLE_1_COURSES = InfoConsts.co_responsible_1_courses
CO_RESPONSIBLE_2_COURSES = InfoConsts.co_responsible_2_courses
CO_RESPONSIBLE_3_COURSES = InfoConsts.co_responsible_3_courses
CO_RESPONSIBLE_4_COURSES = InfoConsts.co_responsible_4_courses


def format_study_line_scrape(string_of_study_lines, study_lines_dct, course_number='12345', type='list'):
    """Take a string of study lines and turn it into a formatted list"""

    if type=='list':
        study_lines_dct = {}

    #string_to_become_lst = (string_of_study_lines.split(";"))[0].split("'")  #Delete this
    string_to_become_lst = string_of_study_lines.split("'")
    lst = []

    # Turn the scraped string containing study lines into a list
    for k in range (1, len(string_to_become_lst), 2):
        lst.append(string_to_become_lst[k])
    for j in range(0, len(lst)):
        scraped_data = lst[j]

        # Absolutely mongoloid IT department at DTU using non-breaking space &nbsp; (this bug took 3 hours to track down)
        scraped_data = scraped_data.replace(" "," ")

        # Replace double comma
        scraped_data = scraped_data.replace("MSc,, ","MSc, ")

        # Removing the corrupt '??' value and replacing '&' character
        scraped_data = scraped_data.replace("??","") # 01005 is odd
        scraped_data = scraped_data.replace("&","and") # D&I is odd

        # Fixing typos made by whoever submitted the courses
        scraped_data = scraped_data.replace("Technological specialization coursee","Technological specialization course") # MSc space is odd
        scraped_data = scraped_data.replace("Technological Specialization Course","Technological specialization course") # MSc Bioinformatics and Systems Biology is odd
        scraped_data = scraped_data.replace("Design og Innovation","Design and Innovation") # Someone made an oopsie at random D&I course¨
        scraped_data = scraped_data.replace("Transport and Logistics","Transportation and Logistics") # Someone made an oopsie at 3 random transport courses
        scraped_data = scraped_data.replace("Communication Technlogies and System Design","Communication Technologies and System Design") # Someone made a spelling oopsie
        scraped_data = scraped_data.replace("Technology Core Courses ","Technology Core Courses") # Someone added an extra space at the end at 34313 and it ruins everything

        # As of October 2021, BSc 'Design of Sustainable Energy Systems'
        # straight up does not exist in the list of study lines?!?
        # instead, the courses accosiated with this study line has generic
        # names such as "Basic Natural Science Courses", "Technology Core Courses", etc.
        # therefore, we must check the exact element to isolate such cases...
        if scraped_data == "Basic Natural Science Courses" or scraped_data == "Technology Core Courses" or scraped_data == "Projects and general subjects":
            scraped_data = scraped_data.replace("Basic Natural Science Courses","BSc, Design of Sustainable Energy Systems")
            scraped_data = scraped_data.replace("Technology Core Courses","BSc, Design of Sustainable Energy Systems")
            scraped_data = scraped_data.replace("Projects and general subjects","BSc, Design of Sustainable Energy Systems")

        # I don't even know wtf happened here
        scraped_data = scraped_data.replace("Mandatory course, Mechanical Engineering, digitalital","BEng, Mechanical Engineering")
        scraped_data = scraped_data.replace("Sustainable Energy ergy", "Sustainable Energy")

        # In a similar vain to BSc Sustainable Energy, (2024/2025) Dunno what this is
        scraped_data = scraped_data.replace("Mandatory Courses","")
        scraped_data = scraped_data.replace("Mandatory courses","")
        scraped_data = scraped_data.replace("1. semester (optag før E24)","")

        # 2024/2025 this is very cursed
        scraped_data = scraped_data.replace("General competence course (BSc)","BSc,")
        scraped_data = scraped_data.replace("General competence course (MSc)","MSc,")
        scraped_data = scraped_data.replace("General competence course�(MSc)","MSc,")
        scraped_data = scraped_data.replace("General competence course (MSc)","MSc,")

        # 2024/2025 update
        scraped_data = scraped_data.replace("Technological Core Courses,","BSc,")
        scraped_data = scraped_data.replace("Projects and general subjects,","BSc,")
        scraped_data = scraped_data.replace("Projects and General Subjects ,","BSc,")
        scraped_data = scraped_data.replace("Projects (BSc),","BSc,")
        scraped_data = scraped_data.replace("Projects (BSc)","BSc,")
        scraped_data = scraped_data.replace("Elective MSc course (BSc),","BSc,")
        scraped_data = scraped_data.replace("Elective MSc course (BSc)","BSc,")
        scraped_data = scraped_data.replace("Elective courses,","BEng,")
        scraped_data = scraped_data.replace("Elective course (B Eng),","BEng,")
        scraped_data = scraped_data.replace("Mandatory course (B Eng),","BEng,")
        scraped_data = scraped_data.replace("Polytechnical foundation (BSc),","BSc,")
        scraped_data = scraped_data.replace("Polytechnical foundation (MSc)","MSc,")
        scraped_data = scraped_data.replace("Programme specific course (BSc),","BSc,")
        scraped_data = scraped_data.replace("Programme specific course (MSc)","MSc,")
        scraped_data = scraped_data.replace("Programme-specific course (MSc)","MSc,")
        scraped_data = scraped_data.replace("Programme-specific course (MSc)","MSc,")

        scraped_data = scraped_data.replace("Technological specialization course (MSc)","MSc,")
        scraped_data = scraped_data.replace("Technological Specialization course (MSc)","MSc,") # Capitalization error at (MSc) Bioinformatics and Systems Biology
        scraped_data = scraped_data.replace("Technological specialization course, MSc. Eng.,","MSc,") # No parenthesis at Design and Innovation

        # Add BSc to start of study lines to avoid identical names
        scraped_data = scraped_data.replace("Basic Natural Science Courses,","BSc,")
        scraped_data = scraped_data.replace("Technology Core Courses,","BSc,")
        scraped_data = scraped_data.replace("Projects and General Subjects,","BSc,")
        scraped_data = scraped_data.replace("Bachelor in","BSc,") # KID is odd
        scraped_data = scraped_data.replace("Teknologisk linjefag,","BSc,") # D&I is odd

        # Add MSc to start of study lines to avoid identical names
        scraped_data = scraped_data.replace("General competence course, MSc. Eng.,","MSc,")
        scraped_data = scraped_data.replace("General competence course, MSc. Eng.","MSc,") # MSc adv.mat.health is odd
        scraped_data = scraped_data.replace("eneral competence course, MSc. Eng.,","MSc,") # Fixing type where G is missing from General

        scraped_data = scraped_data.replace("Technological specialization course, MSc. Eng.,","MSc,")
        scraped_data = scraped_data.replace("Technological specialization course, MSc. Eng.","MSc,") # MSc adv.mat.health is odd

        # Add BEng to start of study lines to avoid identical names
        scraped_data = scraped_data.replace("Mandatory course, Bachelor of Engineering","BEng,")
        scraped_data = scraped_data.replace("Specialization course, Bachelor of Engineering","BEng,")

        # If a study line has multiple different names across courses, combine them
        scraped_data = scraped_data.replace("BEng, Building and Civil Engineering","BEng, Arctic Civil Engineering")
        scraped_data = scraped_data.replace("BSc, Biotechnology","BSc, Human Life Science Engineering")
        scraped_data = scraped_data.replace("BSc, Quantitative Biology and Disease Modelling","BSc, Human Life Science Engineering")

        # 2024/2025 If a study line has multiple different names across courses, combine them
        scraped_data = scraped_data.replace("MSc, Sustainable Energy Technologies","MSc, Sustainable Energy")
        scraped_data = scraped_data.replace("MSc, Technology Entreneurship","MSc, Technology Entrepreneurship")
        scraped_data = scraped_data.replace("Technology Entrepreneurship½","Technology Entrepreneurship")

        # Renaming study lines to match "official" list (https://www.dtu.dk/english/education/bachelor-beng-and-bsc-/bsc/programmes-in-danish/life-science-engineering) #Note: Bioengineering should keep the name "Medicine and Technology"
        scraped_data = scraped_data.replace("BEng, Mobility, Transportation and Logistics","BEng, Mobility, Transport and Logistics")
        scraped_data = scraped_data.replace("BSc, Network Technology and IT","BSc, Cybertechnology")
        scraped_data = scraped_data.replace("BSc, Human Life Science Engineering","BSc, Life Science Engineering")
        scraped_data = scraped_data.replace("MSc, Advanced and Applied Chemistry","MSc, Applied Chemistry")
        scraped_data = scraped_data.replace("MSc, Earth and Space Physics Engineering","MSc, Earth and Space Physics and Engineering")
        scraped_data = scraped_data.replace("MSc, Human-Centered Artificial Intelligence","MSc, Human Centered Artificial Intelligence")
        scraped_data = scraped_data.replace("MSc, Mathematical Modelling and Computing","MSc, Mathematical Modelling and Computation")
        scraped_data = scraped_data.replace("MSc, Transportation and Logistics","MSc, Transport and Logistics")
        scraped_data = scraped_data.replace("MSc, Bioinformatics Systems Biology","MSc, Bioinformatics and Systems Biology")
        scraped_data = scraped_data.replace("MSc, Bioinformatics and System Biologi","MSc, Bioinformatics and Systems Biology")

        # 2024/2025 Renaming study lines to match "official" list (https://www.dtu.dk/english/education/bachelor-beng-and-bsc-/bsc/programmes-in-danish/life-science-engineering)
        scraped_data = scraped_data.replace("General Engineering - taught in Danish","General Engineering")
        scraped_data = scraped_data.replace("BSc, Life Science Engineering","BSc, Human Life Science Engineering")
        scraped_data = scraped_data.replace("BSc, Life Science and Technology","BSc, Human Life Science Engineering")
        scraped_data = scraped_data.replace("BSc, Physics and Nanotechnology","BSc, Engineering Physics")
        scraped_data = scraped_data.replace("BSc, Artificiel Intelligence and Data","BSc, Artificial Intelligence and Data")
        scraped_data = scraped_data.replace("echnology Core Courses, Artificiel Intelligence and Data", "BSc, Artificial Intelligence and Data")
        scraped_data = scraped_data.replace("BEng, HealthcareTechnology","BEng, Healthcare Technology")
        scraped_data = scraped_data.replace("BEng, Softwaretechnology","BEng, Software Technology")


        # 2025/2026 Renaming study lines to match "official" list (https://www.dtu.dk/english/education/bachelor-beng-and-bsc-/bsc/programmes-in-danish/life-science-engineering)
        scraped_data = scraped_data.replace("MSc,, ","MSc, ")
        scraped_data = scraped_data.replace("MSc, Transportation and Logistics","MSc, Transport and Logistics")
        scraped_data = scraped_data.replace("MSc, Earth and Space Physics Engineering","MSc, Earth and Space Physics and Engineering")
        scraped_data = scraped_data.replace("MSc, Bioinformatics","MSc, Bioinformatics and Systems Biology")
        scraped_data = scraped_data.replace("MSc, Technology Entreneurship","MSc, Technology Entrepreneurship")
        scraped_data = scraped_data.replace("MSc, Human-Centered Artificial Intelligence","MSc, Human Centered Artificial Intelligence")
        scraped_data = scraped_data.replace("MSc, Bioinformatics and Systems Biology and Systems Biology", "MSc, Bioinformatics and Systems Biology")
        scraped_data = scraped_data.replace("MSc, MSc. Eng., Architectural Engineering","MSc, Architectural Engineering")

        # Replace double comma
        scraped_data = scraped_data.replace("MSc,, ","MSc, ")

        # Remove white spaces at start and end of string
        scraped_data = scraped_data.strip()

        # If whatever remains after the replace process is this, it is not a study line
        if scraped_data != '' and scraped_data != 'BSc' and scraped_data != 'MSc' and scraped_data != 'BEng':
            # Add study line to dict
            if scraped_data not in study_lines_dct:
                study_lines_dct[scraped_data] = []
            dct_content = study_lines_dct[scraped_data]
            new_entry = [course_number]
            updated_lst = dct_content + new_entry
            updated_lst = list(dict.fromkeys(updated_lst)) # Remove duplicates from list
            study_lines_dct[scraped_data] = updated_lst

    # Sort list and remove any duplicates
    study_lines_complete_lst = sorted(list(study_lines_dct.keys()))
    study_lines_complete_lst = list(dict.fromkeys(study_lines_complete_lst)) # Remove duplicates from list

    # Return list of study lines, or alternatively a dict (if type!='list')
    if type == 'list':
        return study_lines_complete_lst
    else:
        return study_lines_dct

def create_teacher_dct(df, course_numbers):
    """Create dictionary containing each teacher and all their associated courses"""

    # Make sure columns containing the "responsibles" exists:
    try:
        teacher_1_raw_dct = df[MAIN_RESPONSIBLE_NAME].to_dict()
        teacher_1_lst = list(teacher_1_raw_dct.values())
        teacher_2_raw_dct = df[CO_RESPONSIBLE_1_NAME].to_dict()
        teacher_2_lst = list(teacher_2_raw_dct.values())
        teacher_3_raw_dct = df[CO_RESPONSIBLE_2_NAME].to_dict()
        teacher_3_lst = list(teacher_3_raw_dct.values())
        teacher_4_raw_dct = df[CO_RESPONSIBLE_3_NAME].to_dict()
        teacher_4_lst = list(teacher_4_raw_dct.values())
        teacher_5_raw_dct = df[CO_RESPONSIBLE_4_NAME].to_dict()
        teacher_5_lst = list(teacher_5_raw_dct.values())
    except:
        print('Error: it seems that the columns containing the first five course responsibles does not exist in df')

    # Creating a dict of all teachers featuring a list of their courses
    teachers_dct = {}
    for i in range(0, len(course_numbers)):
        # List of all teachers for this course
        list_of_teachers = [teacher_1_lst[i], teacher_2_lst[i], teacher_3_lst[i], teacher_4_lst[i], teacher_5_lst[i]]
        for j in range (0, len(list_of_teachers)):
            responsible = list_of_teachers[j]

            # Add teacher to dict or simply update their course list if they are already in the dict
            if responsible != NO_RESPONSIBLE:
                if responsible not in teachers_dct:
                    teachers_dct[responsible] = str(course_numbers[i])
                else:
                    # Update the string currently in the dict by concatenation
                    current_string = teachers_dct[responsible]
                    new_string = "<br />" + str(course_numbers[i])
                    updated_string = current_string + new_string
                    teachers_dct[responsible] = updated_string

    return(teachers_dct)


def create_teacher_course_lst(df, course_numbers):
    """Create list of courses that each teacher is responsible for"""

    teachers_dct = create_teacher_dct(df, course_numbers)
    column_names = [MAIN_RESPONSIBLE_NAME, CO_RESPONSIBLE_1_NAME, CO_RESPONSIBLE_2_NAME, CO_RESPONSIBLE_3_NAME, CO_RESPONSIBLE_4_NAME]
    column_headers = [MAIN_RESPONSIBLE_COURSES, CO_RESPONSIBLE_1_COURSES, CO_RESPONSIBLE_2_COURSES, CO_RESPONSIBLE_3_COURSES, CO_RESPONSIBLE_4_COURSES]
    for k in range (0, len(column_headers)):
        linked_courses_lst = []
        try:
            responsible_dct = df[column_names[k]].to_dict()
        except:
            print(f'Error: {column_names[k]} is not a column in df')
        for i in range (0, len(course_numbers)):
            course_responsible = responsible_dct[course_numbers[i]]
            if course_responsible != NO_RESPONSIBLE:
                linked_courses_str = teachers_dct[course_responsible]
                linked_courses_lst.append(linked_courses_str)
            else:
                linked_courses_lst.append(NO_RESPONSIBLE)
        df[column_headers[k]] = linked_courses_lst
    return(df)


def create_lst_of_study_lines(df, course_numbers):
    """Create dictionary of all study lines and their associated courses"""

    # Make sure a column names "STUDY_LINES" exists:
    try:
        study_lines_scraped_nested_dct = df[STUDY_LINES].to_dict()
        scraped_study_lines = list(study_lines_scraped_nested_dct.values())
    except:
        print('Error: it seems that STUDY_LINES column in df does not exist')

    # The column STUDY_LINES is a string containing a list of study lines
    study_lines_dct = {}
    for i in range(0, len(course_numbers)):
        # The string of study lines are formatted and turned into a list:
        study_lines_dct = format_study_line_scrape(scraped_study_lines[i], study_lines_dct, course_numbers[i], type='dict')

    # We now have a list of all study lines across all course numbers
    study_lines_complete_lst = sorted(list(study_lines_dct.keys()))
    for i in range (0, len(study_lines_complete_lst)):
        print(study_lines_complete_lst[i])
    # Show all courses associated with any study line by entering a study:
    #print(study_lines_dct["MSc, Communication Technologies and System Design"])
    #print(study_lines_dct["MSc, Human Centered Artificial Intelligence"])
    #print(study_lines_dct["MSc, Autonomous Systems"])
    return study_lines_dct



#%%
if __name__ == "__main__":
    # Read existing df

    df = pd.read_pickle(FileNameConsts.path_of_pkl+FileNameConsts.name_of_pkl+".pkl")
    course_numbers = Utils.get_course_numbers()

    # FUNCTIONALITY 1: PRINT LIST OF STUDY LINES
    study_lines_dct = create_lst_of_study_lines(df, course_numbers)


    # FUNCTIONALITY 2: CREATE TEACHERS' COURSES LIST
    #dct = create_teacher_dct(df, course_numbers)
    #df = create_teacher_course_lst(df, course_numbers)
    #print(df)