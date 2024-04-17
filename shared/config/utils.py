import os

from ansible.inventory.manager import InventoryManager
from ansible.parsing.dataloader import DataLoader
from ansible.template import Templar
from ansible.vars.manager import VariableManager

from .resources.paths import Directories, Inventory, Variables


def find_yaml_files(path):
    """Finds all YAML files recursively under the given path.

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
    return None


def find_playbooks():
    return find_yaml_files(Directories.PBROOT)


def find_host(app_name: str):
    for host in find_hosts():
        if host.startswith(app_name):
            return host
    raise FileNotFoundError


def find_hosts():
    return find_yaml_files(Directories.HVHOME)


# https://stackoverflow.com/questions/66889437/how-to-get-variable-substitution-work-with-ansible-api
def find_host_vars(host_name: str):
    loader = DataLoader()
    loader.set_basedir(Directories.IHOME)

    inventory = InventoryManager(loader=loader, sources=[Inventory.STATIC_HOSTS, "@" + Variables.ALL_SECURE_VARS,
                                                         "@" + Variables.ALL_LXC_VARS,
                                                         "@" + Variables.ALL_VARS])
    variable_manager = VariableManager(loader=loader, inventory=inventory)
    selectedhost = inventory.get_host(host_name)
    hostvars = variable_manager.get_vars(host=selectedhost)
    templar = Templar(loader=loader, variables=hostvars)
    for k, v in hostvars.items():
        if isinstance(v, str):
            hostvars[k] = templar.template(v)
    return hostvars
