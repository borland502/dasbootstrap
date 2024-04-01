import yaml
from dasbootstrap_actions.resources import Paths,Resources
from sqlite_utils import Database
from dasbootstrap_actions.ansible_actions import Actions
import pyaml,json,tempfile

class DatabaseActions(object):

    def __init__(self):

        # Dump the ansible inventory to get a fresh copy
        Actions().dump_inventory()
        with open(Resources.STATIC_HOSTS, 'r') as in_file, Database(Resources.DASBOOTSTRAP_DB) as db:
            yaml_obj = yaml.safe_load(in_file)
            db['inventory'].insert_all(json.dump(yaml_obj), replace=True)

