from simple_term_menu import TerminalMenu

class DasMenu:

    def __init__(self):
        self.options = ["init", "build", "setup", "update"]
        self.terminal_menu = TerminalMenu(self.options)

    def create_menu(self):
        self.menu_entry_index = self.terminal_menu.show()
        print(f"You have selected {self.options[self.menu_entry_index]}!")

if __name__ == '__main__':
    das_menu = DasMenu()
    das_menu.create_menu()