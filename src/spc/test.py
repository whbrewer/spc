from bottle import Bottle, response, SimpleTemplate
from webtest import TestApp
import importlib, os
from constants import USER_ID_SESSION_KEY, APP_SESSION_KEY, NOAUTH_USER
from user_data import user_dir

# the real webapp
app = Bottle()

### session management configuration ###
from beaker.middleware import SessionMiddleware

# USER_ID_SESSION_KEY = 'user_id'
# APP_SESSION_KEY = 'app'
# NOAUTH_USER = 'guest'

session_opts = {
    'session.type': 'file',
    'session.cookie_expires': True, # delete cookies when browser closed
    'session.data_dir': user_dir,
    'session.auto': True
}

app = SessionMiddleware(app, session_opts)
### end session management configuration ###

# context processors - send to every template
try:    SimpleTemplate.defaults["tab_title"] = config.tab_title
except: SimpleTemplate.defaults["tab_title"] = "SPC"


def main():

    modules = ["account"]

    for module in modules:
        try:
            imported_module = importlib.import_module(os.path.curdir + module, 'spc')
            getattr(imported_module, 'bind')(globals())
            app.app.merge(getattr(imported_module, 'routes'))
        except ImportError:
            print "ERROR importing module " + module

    # for route in app.app.routes:
    #     print route.method + "\t" + route.rule

    test_app = TestApp(app)

    # GET /login
    resp = test_app.get('/login')
    assert resp.status_int == 200

    # POST /login - test correct password
    resp = test_app.post('/login', {'user': 'admin', 'passwd': 'admin'})
    assert resp.status_int == 302 # redirects to /myapps or to referrer

    # POST /login - test incorrect password
    resp = test_app.post('/login', {'user': 'admin', 'passwd': 'xyz'})
    assert resp.status_int == 200 # serves error page




