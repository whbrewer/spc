# web framework
from bottle import static_file, request, redirect, app, get, run,\
                   SimpleTemplate, error, template

# python built-ins
import os, sys, traceback, importlib

# other local modules
import config, scheduler, app_reader_writer as apprw
from model import db, apps
from user_data import user_dir
from constants import USER_ID_SESSION_KEY, APP_SESSION_KEY, NOAUTH_USER

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

app = SessionMiddleware(app(), session_opts)
### end session management configuration ###

# context processors - send to every template
try:    SimpleTemplate.defaults["tab_title"] = config.tab_title
except: SimpleTemplate.defaults["tab_title"] = "SPC"

# create an instance of the scheduler
sched = scheduler.Scheduler()

# a few generic routes
@get('/')
def root():
    authorized()
    redirect('/myapps')

@get('/static/<filepath:path>')
def server_static(filepath):
    return static_file(filepath, root='static')

@get('/favicon.ico')
def get_favicon():
    return static_file('favicon.ico', root='static')

@error(500)
def error500(error):
    return template('error', err="500. Check log for traceback")

def authorized():
    '''Return True if user is already logged in, redirect otherwise'''
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
    except:
        exc_type, exc_value, exc_traceback = sys.exc_info()
        print traceback.print_exception(exc_type, exc_value, exc_traceback)
        return ''

def set_active(app):
    # set a session variable to keep track of the current app
    s = request.environ.get('beaker.session')
    s[APP_SESSION_KEY] = app

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


## a couple functions for loading the apps

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
            print 'loading: %s (id: %s)' % (name, appid)
            myapps[name] = app_instance(input_format, name, preprocess, postprocess)
            myapps[name].appid = appid
            myapps[name].input_format = input_format
        except:
            exc_type, exc_value, exc_traceback = sys.exc_info()
            print traceback.print_exception(exc_type, exc_value, exc_traceback)
            print 'ERROR: LOADING: %s (ID: %s) FAILED TO LOAD' % (name, appid)
    default_app = name # simple soln - use last app read from DB
    return True


def main():
    init_config_options()
    load_apps()

    # for local workers, start a polling thread to continuously check for queued jobs
    # if worker == "local": sched.poll()
    sched.poll()

    ## merge in other routes and modules

    modules = ["plots", "jobs", "aws", "container", "user_data", "account",
               "admin", "app_routes", "execute", "util"]

    for module in modules:
        try:
            imported_module = importlib.import_module(os.path.curdir + module, 'spc')
            getattr(imported_module, 'bind')(globals())
            app.app.merge(getattr(imported_module, 'routes'))
        except ImportError:
            print "ERROR importing module " + module

    ## start up the web server

    # run the app using server specified in config.py
    try:
        run(server=config.server, app=app, host='0.0.0.0', \
            port=config.port, debug=False)
    # use the Bottle built-in web server
    except:
        run(app=app, host='0.0.0.0', port=config.port, debug=False)
