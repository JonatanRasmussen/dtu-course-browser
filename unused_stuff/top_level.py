from folder_1.folder_1_file import folder_1_hello_world
from folder_2.subfolder_1.subfolder_file import subfolder_hello_world

def top_level_hello_world():
    print("hello world from top level")

def run_script():
    folder_1_hello_world()
    subfolder_hello_world()

if __name__ == '__main__':
    run_script()
