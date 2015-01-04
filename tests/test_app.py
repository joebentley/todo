import unittest, os, sys, StringIO
from app.app import App
from app.list import List
from app.item import Item

class TestApp(unittest.TestCase):
    def setUp(self):
        # redirect stdout to testcase
        self.output = StringIO.StringIO()
        self.saved_stdout = sys.stdout
        sys.stdout = self.output

    def test_should_display_list_when_given_no_args(self):
        path = 'test_database_file'
        app = App(path)

        # add some items to the database
        list = List()
        for n in range(10):
            list.add(Item(id=n, content="hello world"))

        app.list = list

        app.run()

        for line in self.output.getvalue().split('\n'):
            self.assertTrue(line == "hello world")


    def test_given_path_should_create_new_db(self):
        path = 'test_database_file'
        app = App(path)
        self.assertTrue(os.path.exists(path))
        os.remove(path)


    def tearDown(self):
        self.output.close()
        sys.stdout = self.saved_stdout


def suite():
    suite = unittest.TestSuite()
    suite.addTest(TestApp('test_given_path_should_create_new_db'))
    suite.addTest(TestApp('test_should_display_list_when_given_no_args'))
    return suite

