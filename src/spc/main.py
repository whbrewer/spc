from __future__ import absolute_import

import importlib
import os
import sys
import traceback

from flask import Flask, redirect, request, send_from_directory, session
from werkzeug.datastructures import MultiDict

from . import app_reader_writer as apprw
from . import config
from . import scheduler
from .constants import APP_SESSION_KEY, NOAUTH_USER, USER_ID_SESSION_KEY
from .model import apps, db
from .request_shim import RequestShim
from .templating import template


BASE_DIR = os.path.dirname(__file__)


app = Flask(__name__, static_folder=os.path.join(BASE_DIR, 'static'))
app.secret_key = os.environ.get('SPC_SECRET_KEY', '40dd942d0f03108a84db8697e0307802')
sched = scheduler.Scheduler()


@app.before_request
def inject_request_shims():
    req = request._get_current_object()
    req.forms = RequestShim(MultiDict(request.form))
    req.query = RequestShim(MultiDict(request.args))


@app.route('/')
def root():
    authorized()
    return redirect('/myapps')


@app.route('/static/<path:filepath>')
def server_static(filepath):
    return send_from_directory(app.static_folder, filepath)


@app.route('/favicon.ico')
def get_favicon():
    return send_from_directory(app.static_folder, 'favicon.ico')


@app.errorhandler(500)
@app.errorhandler(501)
@app.errorhandler(502)
def error500(error):
    exc = getattr(error, 'original_exception', None)
    msg = str(exc) if exc else "Unknown error"
    status = getattr(error, 'code', '500')
    return template('error', err="{} ({})".format(msg, status), traceback="")


def authorized():
    """Return username if user is already logged in, redirect otherwise."""
    if config.auth:
        username = session.get(USER_ID_SESSION_KEY)
        if username:
            return username
    return NOAUTH_USER


def active_app():
    return session.get(APP_SESSION_KEY)


def set_active(app_name):
    session[APP_SESSION_KEY] = app_name


def init_config_options():
    try:
        config.worker
    except Exception:
        config.worker = "local"

    try:
        config.auth
    except Exception:
        config.auth = False

    try:
        config.np
    except Exception:
        config.np = 1

    try:
        config.port
    except Exception:
        config.port = 8580


def app_instance(input_format, appname, preprocess=0, postprocess=0):
    if input_format == 'namelist':
        myapp = apprw.Namelist(appname, preprocess, postprocess)
    elif input_format == 'ini':
        myapp = apprw.INI(appname, preprocess, postprocess)
    elif input_format == 'xml':
        myapp = apprw.XML(appname, preprocess, postprocess)
    elif input_format == 'json':
        myapp = apprw.JSON(appname, preprocess, postprocess)
    elif input_format == 'yaml':
        myapp = apprw.YAML(appname, preprocess, postprocess)
    elif input_format == 'toml':
        myapp = apprw.TOML(appname, preprocess, postprocess)
    else:
        return 'ERROR: input_format', input_format, 'not supported'
    return myapp


def load_apps():
    """load apps into myapps global dictionary"""
    global myapps, default_app
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
        except Exception:
            exc_type, exc_value, exc_traceback = sys.exc_info()
            print(traceback.print_exception(exc_type, exc_value, exc_traceback))
            print('ERROR: LOADING: %s (ID: %s) FAILED TO LOAD' % (name, appid))
    default_app = name
    return True


def register_routes():
    modules = [
        "account",
        "admin",
        "app_routes",
        "aws",
        "container",
        "execute",
        "jobs",
        "plots",
        "user_data",
        "util",
    ]

    for module in modules:
        try:
            imported_module = importlib.import_module('.' + module, 'spc')
            getattr(imported_module, 'bind')(globals())
            app.register_blueprint(getattr(imported_module, 'routes'))
        except ImportError:
            print("ERROR importing module " + module)


def main():
    init_config_options()
    load_apps()
    sched.poll()
    register_routes()

    if config.server != 'uwsgi':
        app.run(host='0.0.0.0', port=config.port, debug=False)


if config.server == 'uwsgi':
    main()
