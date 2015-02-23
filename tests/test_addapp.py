# test adding app as one user and deleting as another user
# test checkbox
# test hidden
# test textbox
# test select

import unittest
from bottle import response
import urllib, urllib2, httplib
import sys, os
# prepend parent directory to path
sys.path = [os.path.join(os.path.dirname(__file__), os.pardir)] + sys.path

URL = 'http://localhost:8081'
APP = 'test-app'

class TestRoutes(unittest.TestCase):

    def setUp(self):
        pass

    def tearDown(self):
        pass

    # test valid name 
    def test_upload1(self):
        url = URL+'/upload'
        values = { 'appname': APP }
        self.post(url,values)
    
    def test_upload2(self):
        url = URL+'/upload/step2'
        values = { 'appname': APP } 
        self.post(url,values)

        # to upload test file
        #http://stackoverflow.com/questions/20080123/testing-file-upload-with-flask-and-python-3
        #import io
        #rv = self.app.post('/add', data=dict(
        #                   file=(io.BytesIO(b"this is a test"), 'test.pdf'),
        #                   ), follow_redirects=True)

    def test_upload3(self):
        url = URL+'/upload/upload_contents'
        values = { 'appname': APP, 'input_format': "namelist" }
        self.post(url,values)
        values = { 'appname': APP, 'input_format': "ini" }
        self.post(url,values)
        values = { 'appname': APP, 'input_format': "xml" }
        self.post(url,values)
    
    def test_upload4(self):
        url = URL+'/upload/parse_input_file'
        values = { 'appname': APP }
        self.post(url,values)

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

