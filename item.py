from datetime import datetime

class Item:
    """ Todo list item, holding information about id,
        content, and date created."""

    def __init__(self, id, content, date_created=datetime.now()):
        self.id = int(id)
        self.content = str(content)
        self.date_created = date_created
        self.checked = False

    def __str__(self):
        result = '{0:3d} - {1} - {2}'.format(self.id,
                self.date_created.strftime('%m-%d %H:%M:%S'),
                self.content)

        if self.checked:
            result += ' [CHECKED]'

        return result

    def check(self, cursor):
        """ Check off the todo list item in the database.

            Keyword arguments:
            cursor -- current sqlite3 database connection cursor """
        self.checked = True
        cursor.execute("""UPDATE items SET checked = '1'
                          WHERE id = ?""", (self.id,))

    def remove(self, cursor):
        """ Remove the todo list item from the database.

            Keyword arguments:
            cursor -- current sqlite3 database connection cursor """

        cursor.execute("""DELETE FROM items WHERE id = ?""", (self.id,))

    def save(self, cursor):
        """ Save the todo list item to the database

            Keyword arguments:
            cursor -- current sqlite3 database connection cursor """

        cursor.execute("""INSERT INTO items VALUES
            (?,?,?,?)""", (self.id, self.content, self.checked, self.date_created))

    @staticmethod
    def from_tuple(tup):
        """ Parse a tuple as returned from the database returning an Item object.

            Keyword arguments:
            tup -- Tuple of the form (id, content, checked, date_created)

            checked is '1' for True, '0' for False
            date_created is of format '%Y-%m-%d %H:%M:%S.%f' """

        item = Item(tup[0], tup[1], datetime.strptime(tup[3], '%Y-%m-%d %H:%M:%S.%f'))
        if tup[2] == '1':
            item.checked = True
        return item


