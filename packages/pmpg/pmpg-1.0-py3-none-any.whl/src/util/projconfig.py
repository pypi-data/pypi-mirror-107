from dataclasses import dataclass, asdict, field
from typing import List, Dict
from platform import python_version
import toml

DEFAULT_NAME = "config.toml"

@dataclass
class Project:
    project_name: str
    version: str = "0.1.0"
    version_of_python: str = field(repr = True, default = python_version())
    authors: List[str] = field(repr = True, default_factory = lambda: ["Author name and Author email"])

@dataclass
class RunProps:
    endpoint: str = field(repr = True, default = "main.py")

@dataclass
class Config:
    project: Project
    run_props: RunProps
    packages: Dict[str, str] = field(repr = False, default_factory = lambda: {})
    




def create(pwd: str, package_name: str):
    project = Project(package_name)
    run_props = RunProps()
    dict_resp_of_config = asdict(Config(project, run_props))
    with open(f"{pwd}/{package_name}/{DEFAULT_NAME}", "w") as config_file:
        toml_resp_of_config = toml.dump(dict_resp_of_config, config_file)


def parse(pwd: str) -> dict:
    dict_resp_of_config = {}
    try:
        with open(f"{pwd}/{DEFAULT_NAME}", "r") as config_file:
            dict_resp_of_config = toml.load(config_file)
    except toml.TypeError:
        print("When f is an invalid type or is a list containing invalid types")
    except toml.TomlDecodeError:
        print("When an error occurs while decoding the file(s)")

    return dict_resp_of_config
