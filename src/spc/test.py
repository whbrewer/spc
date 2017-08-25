from bottle import Bottle, response, SimpleTemplate
from webtest import TestApp
import importlib, os
from constants import USER_ID_SESSION_KEY, APP_SESSION_KEY, NOAUTH_USER
from user_data import user_dir
from common import rand_cid

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

    modules = ["account", "admin"]

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
    resp = test_app.get('/register')
    assert resp.status_int == 200

    user = rand_cid()
    email = 'test@test.com'
    passwd = 'XYZ1234'

    # POST /check_user - test existing user
    resp = test_app.post('/check_user', {'user': 'admin'})
    print "POST /check_user user =", 'admin', resp.status
    assert resp.status_int == 200 # serves error page
    assert resp.body == "true"

    # POST /check_user - test non-existing user
    resp = test_app.post('/check_user', {'user': user})
    print "POST /check_user user =", user, resp.status
    assert resp.status_int == 200 # serves error page
    assert resp.body == "false"

    print "registering user", user

    # POST /register test new user
    resp = test_app.post('/register', {'user': user, 'email': email, 'password1': passwd, 'password2': passwd})
    print "POST /register", resp.status
    assert resp.status_int == 302 # redirects to /login or to referrer   

    # POST /register test user already exists
    resp = test_app.post('/register', {'user': user, 'email': email, 'password1': passwd, 'password2': passwd})
    print "POST /register", resp.status
    assert resp.status_int == 200 # return error template   

    # POST /register test new user
    # npasswd = "Hello1234"
    # resp = test_app.post('/account/change_password', {'user': user, 'opasswd': passwd, 'npasswd1': npasswd, 'npasswd2': npasswd})
    # print "POST /account/change_password", resp.status
    # assert resp.status_int == 302 # redirects to /login or to referrer   

    # GET /login
    resp = test_app.get('/login')
    print "GET /login", resp.status
    assert resp.status_int == 200


    ### Admin

    # POST /login - test incorrect password
    resp = test_app.post('/login', {'user': 'admin', 'passwd': 'xyz'})
    print "POST /login", resp.status
    assert resp.status_int == 200 # serves error page

    # POST /login - test correct password
    resp = test_app.post('/login', {'user': 'admin', 'passwd': 'admin'})
    print "POST /login", resp.status
    assert resp.status_int == 302 # redirects to /myapps or to referrer

    # POST /admin/delete_user
    # resp = test_app.post('/admin/delete_user', {'user': user})
    # print "POST /admin/delete_user user =", user, resp.status
    # assert resp.status_int == 302 # serves error page

    # test GET /logout -- this should be the last test
    resp = test_app.get('/logout')
    print "POST /logout", resp.status
    assert resp.status_int == 302



