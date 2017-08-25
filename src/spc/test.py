from bottle import Bottle, response, request, redirect, SimpleTemplate
from webtest import TestApp
import importlib, os
from constants import USER_ID_SESSION_KEY, APP_SESSION_KEY, NOAUTH_USER
from user_data import user_dir
from common import rand_cid
from constants import USER_ID_SESSION_KEY, APP_SESSION_KEY, NOAUTH_USER
from model import users
import config

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
try:    SimpleTemplate.defaults["tab_title"] = config.tab_title
except: SimpleTemplate.defaults["tab_title"] = "SPC"


# DRY this out in the future -- currently in main.py and here
def authorized():
    '''Return username if user is already logged in, redirect otherwise'''
    if config.auth:
        s = request.environ.get('beaker.session')
        s[USER_ID_SESSION_KEY] = s.get(USER_ID_SESSION_KEY, False)
        if not s[USER_ID_SESSION_KEY]:
            redirect('/login')
        else:
            return s[USER_ID_SESSION_KEY]
    else:
        return NOAUTH_USER


def main():

    modules = ["account", "admin"]

    # propagate exceptions through middleware, otherwise difficult to debug
    app.app.catchall = False

    for module in modules:
        try:
            imported_module = importlib.import_module(os.path.curdir + module, 'spc')
            getattr(imported_module, 'bind')(globals())
            app.app.merge(getattr(imported_module, 'routes'))
        except ImportError:
            print "ERROR importing module " + module

    for route in app.app.routes:
        print route.method + "\t" + route.rule

    test_app = TestApp(app)

    # GET /register
    print "GET /register"
    resp = test_app.get('/register')
    assert resp.status_int == 200

    user = rand_cid()
    email = 'test@test.com'
    passwd = 'XYZ1234'

    # POST /check_user - test existing user
    print "POST /check_user user =", 'admin', resp.status
    resp = test_app.post('/check_user', {'user': 'admin'})
    assert resp.status_int == 200 # serves error page
    assert resp.body == "true"

    # POST /check_user - test non-existing user
    print "POST /check_user user =", user, resp.status
    resp = test_app.post('/check_user', {'user': user})
    assert resp.status_int == 200 # serves error page
    assert resp.body == "false"

    print "registering user", user

    # POST /register test new user
    print "POST /register", resp.status
    resp = test_app.post('/register', {'user': user, 'email': email, 'password1': passwd, 'password2': passwd})
    assert resp.status_int == 302 # redirects to /login or to referrer   

    # POST /register test user already exists
    print "POST /register", resp.status
    resp = test_app.post('/register', {'user': user, 'email': email, 'password1': passwd, 'password2': passwd})
    assert resp.status_int == 200 # return error template   

    # POST /register test new user
    npasswd = "Hello1234"
    print "POST /account/change_password", resp.status
    resp = test_app.post('/account/change_password', {'user': user, 'opasswd': passwd, 'npasswd1': npasswd, 'npasswd2': npasswd})
    assert resp.status_int == 302 # redirects to /login or to referrer   

    # GET /login
    print "GET /login", resp.status
    resp = test_app.get('/login')
    assert resp.status_int == 200


    ### Admin

    # POST /login - test incorrect password
    print "POST /login", resp.status
    resp = test_app.post('/login', {'user': 'admin', 'passwd': 'xyz'})
    assert resp.status_int == 200 # serves error page

    # POST /login - test correct password
    print "POST /login", resp.status
    resp = test_app.post('/login', {'user': 'admin', 'passwd': 'admin'})
    assert resp.status_int == 302 # redirects to /myapps or to referrer

    # POST /admin/delete_user
    uid = users(user=user).id
    print "POST /admin/delete_user user =", user, uid, resp.status
    resp = test_app.post('/admin/delete_user', {'uid': uid})
    assert resp.status_int == 302 # serves error page

    # test GET /logout -- this should be the last test
    resp = test_app.get('/logout')
    print "POST /logout", resp.status
    assert resp.status_int == 302
