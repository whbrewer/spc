from bottle import Bottle, response, SimpleTemplate
from webtest import TestApp
import importlib, os

# the real webapp
app = Bottle()

# context processors - send to every template
try:    SimpleTemplate.defaults["tab_title"] = config.tab_title
except: SimpleTemplate.defaults["tab_title"] = "SPC"

def main():

    modules = ["account"]

    for module in modules:
        try:
            imported_module = importlib.import_module(os.path.curdir + module, 'spc')
            getattr(imported_module, 'bind')(globals())
            app.merge(getattr(imported_module, 'routes'))
        except ImportError:
            print "ERROR importing module " + module

    print app.routes

    test_app = TestApp(app)

    resp = test_app.get('/login')
    # assert resp.status == '200 OK'
    assert resp.status_int == 200

