

# Imports
from flask import Blueprint, render_template, request
# Helper functions and global constants
from .search import submit_search_field
from website.context_dicts import course_lists, last_updated_dct, dicts_to_display, data, current_args
from website.global_constants.file_name_consts import FileNameConsts
from website.global_constants.config import Config


views = Blueprint('views', __name__)

@views.route('/', methods=['GET', 'POST'])
def home():
    """This is the main homepage of the site"""

    # Redirect user when they submit something in search field
    if request.method == 'POST':
        return submit_search_field(request.form.get('search_field_input'))

    url_args = request.args.to_dict()
    args_dct = current_args(url_args)
    # Render the home page
    return render_template("home.html", course_lists=course_lists(data()),
                                        dicts_to_display=dicts_to_display(),
                                        data = data(),
                                        args = args_dct,
                                        last_update = last_updated_dct())
    # Note: DO NOT change the name of any of the arguments!
