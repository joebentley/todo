import unittest

import tests.test_item
import tests.test_list

if __name__ == '__main__':
    unittest.TextTestRunner(verbosity=2).run(tests.test_item.suite())
    unittest.TextTestRunner(verbosity=2).run(tests.test_list.suite())

