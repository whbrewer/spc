from bottle import Bottle, response
from webtest import TestApp
import importlib, os

# the real webapp
app = Bottle()

# @app.get('/rest/<name>')
# def root(name):
#     '''Simple example to demonstrate how to test Bottle routes'''
#     response.content_type = 'text/plain'
#     return ['you requested "{}"'.format(name)]


def test_root():
    '''Test GET /'''

    # wrap the real app in a TestApp object
    test_app = TestApp(app)

    # simulate a call (HTTP GET)
    resp = test_app.get('/rest/roger')

    # validate the response
    assert resp.body == 'you requested "roger"'
    assert resp.content_type == 'text/plain'

def main():

    modules = ["account"]

    for module in modules:
        try:
            imported_module = importlib.import_module(os.path.curdir + module, 'spc')
            getattr(imported_module, 'bind')(globals())
            app.merge(getattr(imported_module, 'routes'))
        except ImportError:
            print "ERROR importing module " + module

    # print app.routes

    test_root()

