import os 
from .util import projconfig
from .util import repository


SRC    = "src"
INIT   = "__init__.py"
README = "readme.md"
MAIN   = "main.py"
ENTRY = """
def main():
    print("Hello world")

if __name__ == "__main__":
    main()
"""

def create_file(path: str, name_of_file: str, data: str):
    with open(f"{path}/{name_of_file}", "w") as file:
        file.write(data)


def create(pwd: str, project_name: str):
    try:
        path = f"{pwd}/{project_name}"
        os.mkdir(path)
        
        projconfig.create(pwd, project_name)
        create_file(path, MAIN, ENTRY)
        create_file(path, README, f"# {project_name}")

        path = f"{path}/{SRC}"
        os.mkdir(path)

        create_file(path, INIT, "")
    except FileExistsError:
        print(f"{pwd}/{project_name}/src already exsist!")

