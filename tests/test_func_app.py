import unittest, misc
from bottle import response
import urllib, urllib2, httplib
import sys, os, time
# prepend parent directory to path
sys.path = [os.path.join(os.path.dirname(__file__), os.pardir)] + sys.path

class TestRoutes(unittest.TestCase):

    def setUp(self):
        pass

    def tearDown(self):
        pass

    #@unittest.skip("skipping test...")
    def test_dna(self):
        """test /dna route"""
        # submit parameters
        app = 'dna'
        url = misc.URL+'/confirm'
        dna = 'GATCACAGGTCTATCACCCTATTAACCACTCACGGGA'
        values = { 'app': app, 'cid': '', 'dna': dna }
        (code, html) = misc.post(url,values)
        self.assertEqual(code,httplib.OK)
        self.assertIn("Execute simulation",html)
        loc = html.find("cid:")
        cid = html[loc+4:loc+10]
        # test if input file was written
        assert os.path.exists('user_data/guest/dna/'+cid+'/dna.in') == 1

        # submit for execution
        app = 'dna'
        url = misc.URL+'/execute'
        np = "1"
        values = { 'app': app, 'cid': cid, 'np': np } 
        (code, html) = misc.post(url,values)
        self.assertEqual(code,httplib.OK)
        # wait a second for scheduler to start job
        # this may need to be increased to 2 or 3 seconds
        time.sleep(1) 
        # test if output file was written
        assert os.path.exists('user_data/guest/dna/'+cid+'/dna.out') == 1

if __name__ == '__main__':
    unittest.main()

