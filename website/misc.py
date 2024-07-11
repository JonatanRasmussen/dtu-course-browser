

# Imports
from flask import Blueprint, render_template
from website.context_dicts import get_filter_dct
# Helper functions and global constants

misc = Blueprint('misc', __name__)

@misc.route('/faq')
def faq():
    return render_template("faq.html")


@misc.route('/test')
def test():
    filter_dct = get_filter_dct()
    #for catagory in filter_dct:
    #    for value in filter_dct[catagory]:
    #        print(f'browse?{value}={catagory}')
    return render_template("test.html")

@misc.route('/wip')
def wip():
    data = {'GRADE_12': 4, 'GRADE_10': 3, 'GRADE_7': 3, 'GRADE_4': 5, 'GRADE_02': 3, 'GRADE_00': 2, 'GRADE_MINUS_3': 0, 'PASSED': 0, 'FAILED': 0, 'ABSENT': 0, 'TOTAL_STUDENTS': 20, 'COURSE': '12345'}
    return render_template("wip.html", data=data)