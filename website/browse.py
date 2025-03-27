

# Imports
from flask import Blueprint, render_template, request, redirect, url_for, flash
import pandas as pd
# Helper functions and global constants
from website.context_dicts import data, last_updated_dct, current_args, summary_stats, create_filtered_list_from_url_args, turn_set_into_lst_and_sort
from .search import submit_search_field

browse = Blueprint('browse', __name__)

@browse.route('/browse', methods=['GET', 'POST'])
def browse_courses():
    """ Generate a browse page, featuring each course in the list as a seperate card """

    # Redirect user when they submit something in search field
    if request.method == 'POST':
        return submit_search_field(request.form.get('search_field_input'))

    # Check if no filters are selected
    url_args = request.args.to_dict()
    if not url_args:
        return redirect(url_for('browse.browse_courses', dk='language', eng='language'))

    # Proceed with filtering the courses
    filtered_courses = "filtered_courses"
    url_args = request.args.to_dict()
    set_of_courses_to_display = create_filtered_list_from_url_args(url_args)
    lst_of_courses_to_display = turn_set_into_lst_and_sort(set_of_courses_to_display, url_args)
    course_lst = {filtered_courses: lst_of_courses_to_display}


    return render_template("browse.html", course_lists = course_lst,
                                          dicts_to_display = {'list_of_dicts': [filtered_courses]},
                                          data = data(),
                                          stats = summary_stats(lst_of_courses_to_display),
                                          args = current_args(url_args),
                                          last_update = last_updated_dct())

    # Note: DO NOT change the name of any of the arguments!
