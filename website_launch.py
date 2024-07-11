# Helper functions and global constants
from website import create_app

def website_launch_main():
    """ Run website locally """
    app = create_app()
    app.run(debug = True)
    #app.run(debug = True, host='82.210.204.141', port=8080)


if __name__ == '__main__':
    website_launch_main()
