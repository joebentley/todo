import unittest, sqlite3
from datetime import datetime
from app.list import List
from app.item import Item

class TestList(unittest.TestCase):
    def setUp(self):
        self.conn = sqlite3.connect(":memory:")
        self.cursor = self.conn.cursor()
        self.cursor.execute("""CREATE TABLE items
                               (id PRIMARY KEY, content TEXT,
                                checked TEXT, date_created TEXT)""")

    def test_equality(self):
        list_equal1 = List()
        list_equal2 = List()
        list_unequal = List()

        for n in range(10):
            time = datetime.now()
            list_equal1.add(Item(id=n, content="equal", date_created=time))
            list_equal2.add(Item(id=n, content="equal", date_created=time))
            list_unequal.add(Item(id=n, content="not equal", date_created=time))

        self.assertEqual(list_equal1, list_equal2)
        self.assertNotEqual(list_equal1, list_unequal)
        self.assertNotEqual(list_equal2, list_unequal)


    def test_saving_list_and_retrieving_it(self):
        list = List()

        for n in range(10):
            list.add(Item(id=n, content="hello world"))

        self.assertEqual(len(list), 10)

        for item in list:
            item.save(self.cursor)

        list_retrieved = List.get_all(self.cursor)

        self.assertEqual(len(list_retrieved), 10)
        self.assertEqual(list, list_retrieved)


    def tearDown(self):
        self.cursor.execute("DROP TABLE items")
        self.conn.close()

def suite():
    suite = unittest.TestSuite()
    suite.addTest(TestList('test_equality'))
    suite.addTest(TestList('test_saving_list_and_retrieving_it'))
    return suite

