import unittest
import sys, os
# prepend parent directory to path
sys.path = [os.path.join(os.path.dirname(__file__), os.pardir)] + sys.path
from scipaas import apps

class TestScheduler(unittest.TestCase):

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_namelist(self):
        # this should be existing app in apps dir
        my = apps.namelist('terra')
        print my.read_params()

if __name__ == '__main__':
    unittest.main()
