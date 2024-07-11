

# Imports
import pandas as pd
import math
import random
from flask import Blueprint, render_template, request, redirect, url_for
# Helper functions and global constants
from .search import submit_search_field
from website.global_constants.file_name_consts import FileNameConsts

course_database = Blueprint('course_database', __name__)

#for i in range (0, len(course_number_lst)):

name_and_path_of_pkl = FileNameConsts.path_of_pkl + FileNameConsts.name_of_pkl + ".pkl"
df = pd.read_pickle(name_and_path_of_pkl)
course_set = set(df.COURSE) #Course variable is given in URL

@course_database.route('/course/<string:course_number>', methods=['GET', 'POST'])
def route_to_course(course_number):
    """Route to (course number), or route to 404 if course does not exist in dataframe"""

    # Redirect user when they submit something in search field
    if request.method == 'POST':
        return submit_search_field(request.form.get('search_field_input'))

    # If course exists, route to course page. If not, route to 404 not found
    if course_number in course_set or course_number == "xxxxx":

        desired_course = course_number
        # Go to a random course if course_number is xxxxx
        if course_number == "xxxxx":
            desired_course = random.sample(list(course_set), 1)[0]

        data = df.loc[desired_course].to_dict()
        for key in data:
            if (isinstance(data[key], float) and math.isnan(data[key])):
                data[key] = 'None'
        extra_data = {'score': 'test123'}

        # When the dataframe was constructed from a pickle,
        # lists were accidentally converted to strings. Now converting them back...
        data_column_headers = ["MAIN_RESPONSIBLE_COURSES", "CO_RESPONSIBLE_1_COURSES", "CO_RESPONSIBLE_2_COURSES", "CO_RESPONSIBLE_3_COURSES", "CO_RESPONSIBLE_4_COURSES"]
        for k in range (0, len(data_column_headers)):
            data[data_column_headers[k]] = list(data[data_column_headers[k]].split("<br />"))

        # If course exists, route to course page. If not, route to 404 not found
        return render_template("course.html", data=data, extra_data=extra_data)
    else:
        return render_template("404_invalid_course.html", course=course_number)

@course_database.route('/random/', methods=['GET'])
def route_to_random():
    """Route to random course"""
    mystic_course = random.sample(list(course_set), 1)[0]
    return redirect(url_for('course_database.route_to_course', course_number=mystic_course))