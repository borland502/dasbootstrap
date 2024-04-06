import os
from xdg_base_dirs import *

def find_yaml_files(path):
    """
    Finds all YAML files recursively under the given path.

    Args:
        path: The base path to search.

    Returns:
        A list of absolute paths to all YAML files found.
    """

    # Initialize an empty list to store file paths
    yaml_files = []

    # Loop through all files and subdirectories in the path
    for root, _, files in os.walk(path):
        for file in files:
            # Check if the file extension is .yaml
            if file.endswith(".yaml") or file.endswith(".yml"):
                # Construct the absolute path to the YAML file
                yaml_path = os.path.join(root, file)
                # Add the path to the list
                yaml_files.append(yaml_path)

    return yaml_files

def find_playbook(app_name: str):
    for playbook in find_playbooks():
        if playbook.startswith(app_name):
            return playbook
    raise FileNotFoundError

def find_playbooks():
    return find_yaml_files()

def find_host(app_name: str):
    for host in find_hosts():
        if host.startswith(app_name):
            return host
    raise FileNotFoundError

def find_hosts():
    return find_yaml_files(HVHOME)
