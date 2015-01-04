import sqlite3, os, sys

import commands
from list import List
from item import Item

class App(object):
    """ Main command-line app process class. """
    def __init__(self, app_args=None, path=None):
        path = path or os.path.expanduser("~/.todo.db")

        self.app_args = app_args or []

        self.conn = sqlite3.connect(path)
        self.cursor = self.conn.cursor()

        # create table if it doesn't exist
        self.cursor.execute("""CREATE TABLE IF NOT EXISTS items
                               (id PRIMARY KEY, content TEXT,
                                checked TEXT, date_created TEXT)""")

        self.list = List.get_all(cursor=self.cursor)

        self.commands = {"c": commands.check,
                         "d": commands.delete,
                         "clear": commands.clear }


    def run(self):
        if len(self.app_args) < 2:
            print str(self.list),

