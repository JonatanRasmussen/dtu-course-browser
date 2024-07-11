

# Imports
from flask import Blueprint, render_template, request
from website.context_dicts import get_filter_dct
from .search import submit_search_field
# Helper functions and global constants

misc = Blueprint('misc', __name__)

@misc.route('/faq', methods=['GET', 'POST'])
def faq():
    if request.method == 'POST':
        return submit_search_field(request.form.get('search_field_input'))
    return render_template("faq.html")

@misc.route('/test', methods=['GET', 'POST'])
def test():
    if request.method == 'POST':
        return submit_search_field(request.form.get('search_field_input'))
    return render_template("test.html")

@misc.route('/wip', methods=['GET', 'POST'])
def wip():
    if request.method == 'POST':
        return submit_search_field(request.form.get('search_field_input'))
    data = {'GRADE_12': 4, 'GRADE_10': 3, 'GRADE_7': 3, 'GRADE_4': 5, 'GRADE_02': 3, 'GRADE_00': 2, 'GRADE_MINUS_3': 0, 'PASSED': 0, 'FAILED': 0, 'ABSENT': 0, 'TOTAL_STUDENTS': 20, 'COURSE': '12345'}
    return render_template("wip.html", data=data)