# Imports
from flask import Flask
import os

# Helper functions and global constants

def create_app():
    app = Flask(__name__)
    app.static_folder = 'static'

    # Try to load SECRET_KEY from secretkey.txt
    try:
        with open('secretkey.txt', 'r') as f:
            secret_key = f.read().strip()
    except FileNotFoundError:
        secret_key = 'default_secret_key'
        print()
        print("Custom warning: secretkey.txt file not found. Using default secret key.")
        print()

    app.config['SECRET_KEY'] = secret_key

    from .views import views
    app.register_blueprint(views, url_prefix='/')

    from .misc import misc
    app.register_blueprint(misc, url_prefix='/')

    from .browse import browse
    app.register_blueprint(browse, url_prefix='/')

    from .course_database import course_database
    app.register_blueprint(course_database, url_prefix='/')

    from .recommender import recommender
    app.register_blueprint(recommender, url_prefix='/')

    return app