import unittest, misc
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

    #@get('/<app>/<cid>/tail')
    #@get('/<app>')
    #@post('/app_exists/<appname>')
    #@get('/apps')
    #@get('/apps/load')
    #@post('/apps/delete/<appid>')
    #@get('/apps/edit/<appid>')

if __name__ == '__main__':
    unittest.main()

