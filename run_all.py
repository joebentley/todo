import unittest

import tests.test_item
import tests.test_list
import tests.test_app

if __name__ == '__main__':
    unittest.TextTestRunner(verbosity=2).run(tests.test_item.suite())
    unittest.TextTestRunner(verbosity=2).run(tests.test_list.suite())
    unittest.TextTestRunner(verbosity=2).run(tests.test_app.suite())

