from __future__ import print_function
from __future__ import absolute_import
import re, sys, hashlib, traceback, smtplib, uuid, argparse as ap
from .model import db, users, user_meta
from .constants import USER_ID_SESSION_KEY, APP_SESSION_KEY, NOAUTH_USER
from . import config

from flask import Flask, Blueprint

account = Blueprint('account', __name__)

def _check_user_passwd(user, passwd):
    """check password against database"""
    u = users(user=user)
    hashpw = _hash_pass(passwd)
    if hashpw == u.passwd:
        return True
    else:
        return False

def _hash_pass(pw):
    return hashlib.sha256(pw).hexdigest()

@account.route('/account')
def get_account():
    user = root.authorized()
    app = request.query.app or root.active_app()
    params = {}
    params['app'] = app
    params['user'] = user
    return template('account', params)

@account.route('/register')
def get_register():
    return template('register')

@account.route('/check_user', methods=['POST'])
def check_user(user=""):
    if user == "": user = request.forms.user
    """Server-side AJAX function to check if a username exists in the DB."""
    # return booleans as strings here b/c they get parsed by JavaScript
    if users(user=user.lower()): return 'true'
    else: return 'false'

@account.route('/register', methods=['POST'])
def post_register():
    valid = True

    user = request.forms.user
    if check_user(user) == 'true': valid = False

    email = request.forms.email
    if re.match(r"(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)", email) is None:
        valid = False

    pw1 = request.forms.password1
    if (any(x.isupper() for x in pw1) and any(x.isdigit() for x in pw1) and len(pw1) >= 7):
        pass
    else:
        valid = False

    pw2 = request.forms.password2
    if pw1 != pw2: valid = False

    if valid:
        hashpw = _hash_pass(pw1)
        try:
            config.default_priority
        except:
            config.default_priority = 3

        # insert into database
        users.insert(user=user.lower(), passwd=hashpw, email=email,
                     priority=config.default_priority, new_shared_jobs=0)
        db.commit()
        # email admin user
        try:
            server = smtplib.SMTP('localhost')
            message = user + " just registered " + email
            admin_email = db(users.user=="admin").select(users.email).first()
            server.sendmail('admin@spc.com', [admin_email], message)
            server.quit()
            redirect('/login')
        except:
            redirect('/login')
    else:
        return "ERROR: there was a problem registering. Please try again...<p>" \
             + "<a href='/register'>Return to registration</a>"

@account.route('/login')
@account.route('/login/<referrer>')
def get_login(referrer=''):
    try:
        return template('login', {'referrer': referrer,
                                  'oauth_client_id': config.oauth_client_id})
    except:
        return template('login', {'referrer': referrer})

@account.route('/login', methods=['POST'])
def post_login():
    if not config.auth:
        return "ERROR: authorization disabled. Change auth setting in config.py to enable"

    s = request.environ.get('beaker.session')
    row = users(user=request.forms.get('user').lower())
    pw = request.forms.passwd
    err = "<p>Login failed: wrong username or password</p>"
    # if password matches, set the USER_ID_SESSION_KEY
    hashpw = hashlib.sha256(pw).hexdigest()

    try:
        if hashpw == row.passwd:
            # set session key
            s[USER_ID_SESSION_KEY] = row.user.lower()
            s.save()
        else:
            return err
    except:
        exc_type, exc_value, exc_traceback = sys.exc_info()
        print(traceback.print_exception(exc_type, exc_value, exc_traceback))
        return err
    # if referred to login from another page redirect to referring page
    referrer = request.forms.referrer
    if referrer: redirect('/'+referrer)
    else: redirect('/myapps')

@account.route('/logout')
def logout():
    s = request.environ.get('beaker.session')
    s.delete()
    try:
        return template('logout',  {'oauth_client_id': config.oauth_client_id})
    except:
        redirect('/login')

@app.route('/account/change_password', methods=['POST'])
def change_password():
    # this is basically the same coding as the register function
    # needs to be DRY'ed out in the future
    user = root.authorized()
    if config.auth and not root.authorized(): redirect('/login')
    opasswd = request.forms.opasswd
    pw1 = request.forms.npasswd1
    pw2 = request.forms.npasswd2
    # check old passwd
    #user = request.forms.user
    if _check_user_passwd(user, opasswd) and pw1 == pw2 and len(pw1) > 0:
        u = users(user=user)
        u.update_record(passwd=_hash_pass(pw1))
        db.commit()
    else:
        return template('error', err="problem with password")
    params = {}
    params['user'] = user
    params['alert'] = "SUCCESS: password changed"
    return template('account', params)

@account.route('/tokensignin', methods=['POST'])
def tokensignin():
    email = request.forms.get('email')
    s = request.environ.get('beaker.session')
    user, _ = email.split('@')
    s[USER_ID_SESSION_KEY] = user

    if not users(user=user.lower()):
       # insert a random password that nobody will be able to guess
       hashpw = _hash_pass(str(uuid.uuid4())[:8])
       users.insert(user=user.lower(), email=email, passwd=hashpw,
                    priority=config.default_priority, new_shared_jobs=0)
       db.commit()

    return user

@account.route('/theme')
def get_theme():
    user = root.authorized()
    uid = users(user=user).id
    return user_meta(uid=uid).theme

@account.route('/theme', methods=['POST'])
def save_theme():
    user = root.authorized()
    uid = users(user=user).id
    print("saving theme:", request.forms.theme)
    user_meta.update_or_insert(user_meta.uid==uid, uid=uid, theme=request.forms.theme)
    db.commit()


