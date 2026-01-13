from __future__ import absolute_import

import importlib
import os
import sys
import traceback

from bottle import Jinja2Template, TEMPLATE_PATH, app, error, get, jinja2_template as template, redirect, request, run, static_file
from beaker.middleware import SessionMiddleware

from . import app_reader_writer as apprw
from . import config
from . import scheduler
from .constants import APP_SESSION_KEY, NOAUTH_USER, USER_ID_SESSION_KEY
from .model import apps, db
from .user_data import user_dir


BASE_DIR = os.path.dirname(__file__)
TEMPLATE_PATH.insert(0, os.path.join(BASE_DIR, 'templates'))

session_opts = {
    'session.type': 'file',
    'session.cookie_expires': True,
    'session.data_dir': user_dir,
    'session.auto': True,
}

app = SessionMiddleware(app(), session_opts)

try:
    Jinja2Template.defaults["tab_title"] = config.tab_title
except Exception:
    Jinja2Template.defaults["tab_title"] = "SPC"

sched = scheduler.Scheduler()


@get('/')
def root():
    authorized()
    redirect('/myapps')


@get('/static/<filepath:path>')
def server_static(filepath):
    return static_file(filepath, root=os.path.join(BASE_DIR, 'static'))


@get('/favicon.ico')
def get_favicon():
    return static_file('favicon.ico', root=os.path.join(BASE_DIR, 'static'))


@error(500)
@error(501)
@error(502)
def error500(error):
    exc = getattr(error, 'exception', None)
    msg = str(exc) if exc else "Unknown error"
    status = getattr(error, 'status_code', '500')
    trace = getattr(error, 'traceback', '')
    return template('error', err="{} ({})".format(msg, status), traceback=trace)


def authorized():
    """Return username if user is already logged in, redirect otherwise."""
    if config.auth:
        s = request.environ.get('beaker.session')
        s[USER_ID_SESSION_KEY] = s.get(USER_ID_SESSION_KEY, False)
        if not s[USER_ID_SESSION_KEY]:
            redirect('/login')
        else:
            return s[USER_ID_SESSION_KEY]
    else:
        return NOAUTH_USER


def active_app():
    s = request.environ.get('beaker.session')
    try:
        return s[APP_SESSION_KEY]
    except Exception:
        return None


def set_active(app_name):
    s = request.environ.get('beaker.session')
    s[APP_SESSION_KEY] = app_name


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


def main():
    from . import util

    init_config_options()
    load_apps()

    sched.poll()

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
            app.app.merge(getattr(imported_module, 'routes'))
        except ImportError:
            print("ERROR importing module " + module)

    if config.server != 'uwsgi':
        run(
            server=config.server,
            app=app,
            host='0.0.0.0',
            port=config.port,
            debug=False,
        )


if config.server == 'uwsgi':
    main()
