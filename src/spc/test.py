from bottle import Bottle, Jinja2Template, TEMPLATE_PATH, redirect, request, response
from webtest import TestApp
import importlib
import os
import sys
import traceback

from . import app_reader_writer as apprw
from . import config
from .common import rand_cid
from .constants import APP_SESSION_KEY, NOAUTH_USER, USER_ID_SESSION_KEY
from .model import apps, db, users
from .user_data import user_dir

BASE_DIR = os.path.dirname(__file__)
TEMPLATE_PATH.insert(0, os.path.join(BASE_DIR, 'templates'))

# the real webapp
app = Bottle()

### session management configuration ###
from beaker.middleware import SessionMiddleware

session_opts = {
    'session.type': 'file',
    'session.cookie_expires': True, # delete cookies when browser closed
    'session.data_dir': user_dir,
    'session.auto': True
}

app = SessionMiddleware(app, session_opts)
### end session management configuration ###

# context processors - send to every template
try:
    Jinja2Template.defaults["tab_title"] = config.tab_title
except Exception:
    Jinja2Template.defaults["tab_title"] = "SPC"


# DRY this out in the future -- currently in main.py and here
def authorized():
    '''for testing purposes, don't maintain sessions, just return the user
       somehow it has been problematic to work with in the testing environment'''
    return user
    # see main.py for how this is used in production

def init_config_options():
    """set default options for missing config file settings"""

    try: config.worker
    except: config.worker = "local"

    try: config.auth
    except: config.auth = False

    try: config.np
    except: config.np = 1

    try: config.port
    except: config.port = 8580

    return None


def app_instance(input_format, appname, preprocess=0, postprocess=0):
    if(input_format=='namelist'):
        myapp = apprw.Namelist(appname, preprocess, postprocess)
    elif(input_format=='ini'):
        myapp = apprw.INI(appname, preprocess, postprocess)
    elif(input_format=='xml'):
        myapp = apprw.XML(appname, preprocess, postprocess)
    elif(input_format=='json'):
        myapp = apprw.JSON(appname, preprocess, postprocess)
    elif(input_format=='yaml'):
        myapp = apprw.YAML(appname, preprocess, postprocess)
    elif(input_format=='toml'):
        myapp = apprw.TOML(appname, preprocess, postprocess)
    else:
        return 'ERROR: input_format', input_format, 'not supported'
    return myapp


def load_apps():
    """load apps into myapps global dictionary"""
    global myapps, default_app
    # Connect to DB
    result = db().select(apps.ALL)
    myapps = {}
    for row in result:
        name = row['name']
        appid = row['id']
        preprocess = row['preprocess']
        postprocess = row['postprocess']
        input_format = row['input_format']
        try:
            print('loading: %s (id: %s)' % (name, appid))
            myapps[name] = app_instance(input_format, name, preprocess, postprocess)
            myapps[name].appid = appid
            myapps[name].input_format = input_format
        except:
            exc_type, exc_value, exc_traceback = sys.exc_info()
            print(traceback.print_exception(exc_type, exc_value, exc_traceback))
            print('ERROR: LOADING: %s (ID: %s) FAILED TO LOAD' % (name, appid))
    default_app = name # simple soln - use last app read from DB
    return True


def set_active(app):
    # set a session variable to keep track of the current app
    s = request.environ.get('beaker.session')
    s[APP_SESSION_KEY] = app


def main():
    global user

    init_config_options()
    config.auth = True
    load_apps()

    modules = ["account", "admin", "app_routes", "aws", "container",
               "execute", "jobs", "plots", "user_data", "util"]

    # propagate exceptions through middleware, otherwise difficult to debug
    app.app.catchall = False

    for module in modules:
        try:
            imported_module = importlib.import_module('.' + module, 'spc')
            getattr(imported_module, 'bind')(globals())
            app.app.merge(getattr(imported_module, 'routes'))
        except ImportError:
            print("ERROR importing module " + module)

    # list all routes
    # for route in app.app.routes:
    #     print route.method + "\t" + route.rule

    print()

    test_app = TestApp(app)

    # GET /register
    print("GET /register")
    resp = test_app.get('/register')
    assert resp.status_int == 200

    user = rand_cid()
    email = 'test@test.com'
    passwd = 'XYZ1234'

    # POST /check_user - test existing user
    print("POST /check_user user =", 'admin', resp.status)
    resp = test_app.post('/check_user', {'user': 'admin'})
    assert resp.status_int == 200 # serves error page
    assert resp.text == "true"

    # POST /check_user - test non-existing user
    print("POST /check_user user =", user, resp.status)
    resp = test_app.post('/check_user', {'user': user})
    assert resp.status_int == 200 # serves error page
    assert resp.text == "false"

    print("registering user", user)

    # POST /register test new user
    print("POST /register")
    resp = test_app.post('/register', {'user': user, 'email': email, 'password1': passwd, 'password2': passwd})
    assert resp.status_int == 302 # redirects to /login or to referrer   

    # POST /register test user already exists
    print("POST /register")
    resp = test_app.post('/register', {'user': user, 'email': email, 'password1': passwd, 'password2': passwd})
    assert resp.status_int == 200 # return error template   

    # POST /register test new user
    npasswd = "Hello1234"
    print("POST /account/change_password")
    resp = test_app.post('/account/change_password', {'user': user, 'opasswd': passwd, 'npasswd1': npasswd, 'npasswd2': npasswd})
    assert resp.status_int == 200 # returns account.tpl

    # GET /login
    print("GET /login")
    resp = test_app.get('/login')
    assert resp.status_int == 200

    # POST /login -- login as user for testing other routes
    print("POST /login")
    resp = test_app.post('/login', {'user': user, 'passwd': npasswd})
    assert resp.status_int == 302 # redirect to /myapps

    ### Test app.routes
    print("\n### Test /app routes")

    # test GET /logout -- this should be the last test
    # note: this test will fail if dna has been removed
    # need to probably add a test app
    appname = 'dna'
    print("GET /<app> app is:" + appname)
    resp = test_app.get('/' + appname)
    assert resp.status_int == 200

    print("GET /app_exists/<appname>")
    resp = test_app.get('/app_exists/'+ appname)
    assert resp.status_int == 200 
    assert resp.text == "true"

    ### Admin

    # POST /login - test incorrect password
    print("POST /login")
    resp = test_app.post('/login', {'user': 'admin', 'passwd': 'xyz'})
    assert resp.status_int == 200 # serves error page

    # POST /login - test correct password
    print("POST /login")
    resp = test_app.post('/login', {'user': 'admin', 'passwd': 'admin'})
    assert resp.status_int == 302 # redirects to /myapps or to referrer

    # POST /admin/delete_user
    uid = users(user=user).id
    print("POST /admin/delete_user user =", user, uid, resp.status)
    user = 'admin' # switch user to admin b/c only admin can delete users
    resp = test_app.post('/admin/delete_user', {'uid': uid})
    assert resp.status_int == 302 # serves error page

    # test GET /logout -- this should be the last test
    print("POST /logout")
    resp = test_app.get('/logout')
    assert resp.status_int == 302
