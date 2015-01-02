import curses, sqlite3, sys, os

import commands
from list import List
from item import Item

class App:
    """ Main app process class. """
    def __init__(self):
        if len(sys.argv) > 1:
            path = sys.argv[1]
        else:
            path = os.path.expanduser("~/.todo.db")

        self.conn = sqlite3.connect(path)
        self.cursor = self.conn.cursor()

        # create table if it doesn't exist
        self.cursor.execute("""CREATE TABLE IF NOT EXISTS items
                               (id PRIMARY KEY, content TEXT,
                                checked TEXT, date_created TEXT)""")

        self.win = curses.initscr()

        self.list = List.get_all(cursor=self.cursor)

        self.commands = {":c": commands.check,
                         ":d": commands.delete,
                         ":clear": commands.clear }

    def run(self):
        """ Runs app in infinite loop until exited by user. """
        while True:
            try:
                result = self.update()
            except:
                # always clean up curses before throwing an error
                self.cleanup()
                raise

            if result == "quit":
                self.cleanup()
                break

    def update(self):
        """ Update called each time user inputs a command. """
        self.win.refresh()
        self.win.clear()
        self.win.move(3, 0)

        # print in decending order
        for item in reversed(list(self.list)):
            self.win.addstr(str(item) + '\n')

        self.win.move(0, 0)

        try:
            input_str = self.win.getstr()
        except KeyboardInterrupt:
            # don't allow keyboard interrupts
            return

        # if input starts with a colon, it's a command, not an item to add
        if input_str and input_str[0] != ":":
            item = Item(id=self.list.next_id(), content=input_str)
            item.save(cursor=self.cursor)
            self.list.add(item)
            self.conn.commit()

        if input_str.startswith(":q"):
            return 'quit'

        # get command that corresponds to user input and execute it
        for command, func in self.commands.iteritems():
            if input_str.startswith(command):
                func(app=self, input_str=input_str)
                return

    def error(self, message):
        """ Display error message on to screen and wait for the user
            to press any key. """
        self.win.move(1, 0)
        self.win.addstr(message)
        self.win.getch()

    def cleanup(self):
        """ Cleanup curses and database connection. """
        self.conn.close()
        curses.endwin()

