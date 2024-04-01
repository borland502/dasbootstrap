import os
from pathlib import Path
from cursesmenu import CursesMenu
from cursesmenu.items import *
from xdg_base_dirs import *
from dasbootstrap_actions.ansible_actions import Actions

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

def find_playbooks():
    return find_yaml_files(Path.joinpath(xdg_data_home(), 'dasbootstrap/ansible/playbooks'))

def find_hosts():
    hosts = find_yaml_files(HVHOME)




class DasMenu():

    def __init__(self):
        self.actions = Actions()
        self.cursesmenu = CursesMenu("Dasbootstrap", "Ansible Playbook Manager")

        self.submenu = CursesMenu("This is the submenu")
        self.submenu_item = SubmenuItem("Show a submenu", self.submenu, menu=self.cursesmenu)

        #TODO: Need an intermediary object to wait on return
        self.inventory_cmd = FunctionItem("Dump Inventory to hosts.yaml",
                                          self.actions.dump_inventory())
        self.submenu.items.append(self.inventory_cmd)

        self.setup_menu = CursesMenu("Setup an LXC container with an application")
        self.setup_menu_item = SubmenuItem("Setup", submenu=self.setup_menu, menu=self.cursesmenu)
        self.setup_menu_new = CommandItem(text="Create new LXC",command="ls", arguments="-lha", menu=self.setup_menu,
                                          should_exit=True)
        self.setup_menu.items.append(self.setup_menu_new)
        self.cursesmenu.items.append(self.submenu_item)
        self.cursesmenu.items.append(self.setup_menu_item)

        self.cursesmenu.show()

if __name__ == '__main__':
    das_menu = DasMenu()