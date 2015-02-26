import unittest, misc
from bottle import response
import httplib
import sys, os
# prepend parent directory to path
sys.path = [os.path.join(os.path.dirname(__file__), os.pardir)] + sys.path

URL = 'http://localhost:8081'

class TestLogin(unittest.TestCase):

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_login_valid(self):
        url = URL+'/login'
        values = { 'user': 'guest', 'passwd': 'guest' }
        response = misc.post(url,values)
        (code,html) = misc.post(url,values)
        self.assertEqual(code,httplib.OK)
        self.assertNotIn("failed",html)

    def test_login_invalid(self):
        url = URL+'/login'
        values = { 'askjdfas': 'guest', 'passwd': 'guest' }
        response = misc.post(url,values)
        (code,html) = misc.post(url,values)
        self.assertEqual(code,httplib.OK)
        self.assertIn("failed",html)

if __name__ == '__main__':
    unittest.main()
