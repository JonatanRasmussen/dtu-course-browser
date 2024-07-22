
def folder_2_hello_world():
    print("hello world from folder 2")

def access_top_level():
    if __package__ is None:
        import sys
        from os import path
        sys.path.append( path.dirname( path.dirname( path.abspath(__file__) ) ) )
        from top_level import run_script
    else:
        from ..top_level import run_script
    run_script()


def run_top_level_hello_world():
    if __package__ is None:
        import sys
        from os import path
        sys.path.append( path.dirname( path.dirname( path.abspath(__file__) ) ) )
        from top_level import top_level_hello_world
    else:
        from ..top_level import top_level_hello_world
    top_level_hello_world()

if __name__ == '__main__':
    run_top_level_hello_world()
    access_top_level()
