

# Imports
from flask import Flask
# Helper functions and global constants


def create_app():
    app = Flask(__name__)
    app.static_folder = 'static'
    app.config['SECRET_KEY'] = 'cookiecutter24470763'

    from .views import views
    app.register_blueprint(views, url_prefix='/')

    from .misc import misc
    app.register_blueprint(misc, url_prefix='/')

    from .browse import browse
    app.register_blueprint(browse, url_prefix='/')

    from .course_database import course_database
    app.register_blueprint(course_database, url_prefix='/')

    return app