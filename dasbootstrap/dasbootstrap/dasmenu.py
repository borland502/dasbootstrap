import os
from pathlib import Path
from cursesmenu import CursesMenu
from cursesmenu.items import *
from xdg_base_dirs import *
from dasbootstrap_actions.ansible_actions import Actions

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