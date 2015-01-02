import unittest, sqlite3
from app.item import Item

class TestItem(unittest.TestCase):
    def setUp(self):
        self.conn = sqlite3.connect(":memory:")
        self.cursor = self.conn.cursor()
        self.cursor.execute("""CREATE TABLE items
                               (id PRIMARY KEY, content TEXT,
                                checked TEXT, date_created TEXT)""")

    def test_saving_item_and_retrieving_it(self):
        item = Item(id=0, content="hello world")
        item.save(self.cursor)
        self.cursor.execute("SELECT * FROM items")
        # retrieve item back from database
        raw = self.cursor.fetchone()
        retrieved_item = Item.from_tuple(raw)

        # check that it is the one we saved
        self.assertEqual(retrieved_item.id, item.id)
        self.assertEqual(retrieved_item.content, item.content)
        self.assertEqual(retrieved_item.date_created, item.date_created)

    def test_checking_item(self):
        item = Item(id=0, content="hello world")

        # ensure the item is unchecked
        item.checked = False

        item.save(self.cursor)
        self.cursor.execute("SELECT * FROM items")
        raw_unchecked = self.cursor.fetchone()
        # now check the item and retrieve it again
        item.check(self.cursor)
        self.cursor.execute("SELECT * FROM items")
        raw_checked = self.cursor.fetchone()

        item_unchecked = Item.from_tuple(raw_unchecked)
        item_checked = Item.from_tuple(raw_checked)

        self.assertFalse(item_unchecked.checked)
        self.assertTrue(item_checked.checked)
        self.assertNotEqual(item_unchecked.checked, item_checked.checked)

    def test_deleting_item(self):
        item = Item(id=0, content="hello world")
        item.save(self.cursor)

        item.delete(self.cursor)
        self.cursor.execute("SELECT * FROM items")
        raw_deleted = self.cursor.fetchone()
        self.assertIsNone(raw_deleted)

    def tearDown(self):
        self.cursor.execute("DROP TABLE items")
        self.conn.close()

def suite():
    suite = unittest.TestSuite()
    suite.addTest(TestItem('test_saving_item_and_retrieving_it'))
    suite.addTest(TestItem('test_checking_item'))
    suite.addTest(TestItem('test_deleting_item'))
    return suite

