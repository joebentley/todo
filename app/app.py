import sqlite3, os, sys, argparse

import commands
from list import List
from item import Item

class App(object):
    """ Main command-line app process class. """
    def __init__(self):
        # setup and parse command line args
        parser = argparse.ArgumentParser(description="""
            Todo list application.""")
        parser.add_argument('-f' , metavar='path_to_list', default='',
            help='Path to the database file to use/create.')
        parser.add_argument('-c' , metavar='item_id', type=int, default=None,
            help='Check item with ID')
        parser.add_argument('-d' , metavar='item_id', type=int, default=None,
            help='Delete item with ID')
        parser.add_argument('--clear' , default='', action='store_true',
            help='Clear the database')
        self.args = parser.parse_args()

        # get path (if given) and connect to it
        path = self.args.f or os.path.expanduser("~/.todo.db")
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
        print str(self.list),

