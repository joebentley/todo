from datetime import datetime
from item import Item

class List:
    """ Todo list, containing the current list of items. """
    def __init__(self, items=[]):
        self.items = items

    def __str__(self):
        res = ''
        for item in self.items:
            res += str(item) + '\n'
        return res

    def __iter__(self):
        return iter(self.items)

    def __len__(self):
        return len(self.items)

    def get_item(self, itemid):
        """ Return the item with id given by itemid raising
            IndexError if item not found. """
        try:
            return filter(lambda x: x.id == itemid, self.items)[0]
        except IndexError:
            raise

    def remove_item(self, itemid, cursor):
        """ Remove the item from list with id given by itemid raising
            IndexError if item not found in list. """
        try:
            deleted = filter(lambda x: x.id == itemid, self.items)[0]
        except IndexError:
            raise

        self.items.remove(deleted)
        deleted.remove(cursor)
        return True

    def next_id(self):
        """ Return the id of the next element. """
        return max(self.items, key=lambda x: x.id).id + 1

    def add(self, item):
        """ Add item to the list. """
        self.items.append(item)

    @staticmethod
    def get_all(cursor):
        """ Return a list of items parsed from the database.

            Keyword arguments:
            cursor -- current sqlite3 database connection cursor """
        # grab the entire table and parse each element
        cursor.execute('SELECT * FROM items')
        raw = cursor.fetchall()
        return list(map(lambda tup: Item.from_tuple(tup), raw))

