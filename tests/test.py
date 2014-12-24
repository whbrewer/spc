import unittest
import sys
sys.path.insert(0, '../')

import scipaas
#import bottle
#import bottle.ext.sqlite

class SciPaasTest(unittest.TestCase):
    def test_overview(self):
        print scipaas.overview()
