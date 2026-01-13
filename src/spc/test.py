from __future__ import absolute_import

from . import config
from .common import rand_cid
from . import main as spc_main
from .model import users


def main():
    spc_main.init_config_options()
    config.auth = True
    spc_main.load_apps()
    spc_main.register_routes()

    spc_main.app.testing = True
    client = spc_main.app.test_client()

    # GET /register
    print("GET /register")
    resp = client.get('/register')
    assert resp.status_code == 200

    user = rand_cid()
    email = 'test@test.com'
    passwd = 'XYZ1234'

    # POST /check_user - test existing user
    print("POST /check_user user = admin", resp.status)
    resp = client.post('/check_user', data={'user': 'admin'})
    assert resp.status_code == 200
    assert resp.get_data(as_text=True) == "true"

    # POST /check_user - test non-existing user
    print("POST /check_user user =", user, resp.status)
    resp = client.post('/check_user', data={'user': user})
    assert resp.status_code == 200
    assert resp.get_data(as_text=True) == "false"

    print("registering user", user)

    # POST /register test new user
    print("POST /register")
    resp = client.post('/register', data={'user': user, 'email': email, 'password1': passwd, 'password2': passwd})
    assert resp.status_code == 302

    # POST /register test user already exists
    print("POST /register")
    resp = client.post('/register', data={'user': user, 'email': email, 'password1': passwd, 'password2': passwd})
    assert resp.status_code == 200

    # POST /register test new user
    npasswd = "Hello1234"
    print("POST /account/change_password")
    resp = client.post('/account/change_password', data={'user': user, 'opasswd': passwd, 'npasswd1': npasswd, 'npasswd2': npasswd})
    assert resp.status_code == 200

    # GET /login
    print("GET /login")
    resp = client.get('/login')
    assert resp.status_code == 200

    # POST /login -- login as user for testing other routes
    print("POST /login")
    resp = client.post('/login', data={'user': user, 'passwd': npasswd})
    assert resp.status_code == 302

    ### Test app.routes
    print("\n### Test /app routes")

    appname = 'dna'
    print("GET /<app> app is:" + appname)
    resp = client.get('/' + appname)
    assert resp.status_code == 200

    print("GET /app_exists/<appname>")
    resp = client.get('/app_exists/' + appname)
    assert resp.status_code == 200
    assert resp.get_data(as_text=True) == "true"

    ### Admin
    print("POST /login")
    resp = client.post('/login', data={'user': 'admin', 'passwd': 'xyz'})
    assert resp.status_code == 200

    print("POST /login")
    resp = client.post('/login', data={'user': 'admin', 'passwd': 'admin'})
    assert resp.status_code == 302

    uid = users(user=user).id
    print("POST /admin/delete_user user =", user, uid, resp.status)
    resp = client.post('/admin/delete_user', data={'uid': uid})
    assert resp.status_code == 302

    print("POST /logout")
    resp = client.get('/logout')
    assert resp.status_code == 200
