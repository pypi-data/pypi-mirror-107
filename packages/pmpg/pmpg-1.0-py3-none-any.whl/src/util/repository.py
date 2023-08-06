import subprocess
import os

CMD = "git init"
ERR = "-bash: /usr/bin/git: No such file or directory"


def create(pwd: str, project_name: str):
    try:
        os.chdir(f"{pwd}/{project_name}")
        subprocess.run(CMD, shell = True, check = True)
    except subprocess.CalledProcessError:
        print("Need install git")
