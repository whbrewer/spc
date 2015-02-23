import unittest
from bottle import response
import urllib, urllib2, httplib
import sys, os
# prepend parent directory to path
sys.path = [os.path.join(os.path.dirname(__file__), os.pardir)] + sys.path

URL = 'http://localhost:8081'

class TestRoutes(unittest.TestCase):

    def setUp(self):
        pass

    def tearDown(self):
        pass

    #def test_hello_app(self):
    #    url = URL+'/confirm'
    #    values = { 'str': 'test', 'app': 'helloworld' }
    #    self.post(url,values)

    def post(self,url,values):
        data = urllib.urlencode(values)
        req = urllib2.Request(url, data)
        response = urllib2.urlopen(req)
        html = response.read()
        #print html
        #print response.getcode()
        return self.assertEqual(response.getcode(),httplib.OK)

if __name__ == '__main__':
    unittest.main()

