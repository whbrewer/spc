import unittest
import logging
import sys, os
# prepend parent directory to path
sys.path = [os.path.join(os.path.dirname(__file__), os.pardir)] + sys.path
from src import apps

class TestApps(unittest.TestCase):

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_namelist(self):
        # this should be existing app in apps dir
        my = apps.Namelist('dna')
        # log= logging.getLogger( "TestApps.test_namelist" )
        # log.debug( my.read_params() )
        self.assertTrue( len(my.read_params()) > 0 )

if __name__ == '__main__':
    logging.basicConfig( stream=sys.stderr )
    logging.getLogger( "TestApps.test_namelist" ).setLevel( logging.DEBUG )
    unittest.main()
