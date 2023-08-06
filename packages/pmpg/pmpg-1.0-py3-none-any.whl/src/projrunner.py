import subprocess

PYTHON = "python3"
PIP = "pip3"

def install_packs(packages: dict):
    if len(packages) == 0:
        return
    
    for name, version in zip(packages.keys(), packages.values()):
        try:
            if len(version) == 0: 
                subprocess.run(f"{PIP} install {name}", shell = True, check = True)
            else:
                subprocess.run(f"{PIP} install {name}=={version}", shell = True, check = True)
        except subprocess.CalledProcessError as exception:
            print(exception.args)


def run(endpoint: str):
    try:
        subprocess.run(f"{PYTHON} {endpoint}", shell = True, check = True)
    except subprocess.CalledProcessError:
        print("Need install python3")