import sys, fire, json
from strip_ansi import strip_ansi
from dasbootstrap.dasmenu import DasMenu, Actions

if __name__ == '__main__':
    fire.Fire(Actions, name="dasbootstrap")
