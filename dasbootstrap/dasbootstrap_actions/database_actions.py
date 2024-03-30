from dasbootstrap_actions.resources import Paths,Resources
from sqlite_utils import Database

class DatabaseActions:

    def __init__(self):
        self.dbs_db = Database(Resources.DASBOOTSTRAP_DB)
