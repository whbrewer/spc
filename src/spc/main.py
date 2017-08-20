# web framework
from bottle import template, static_file, request, redirect, app, get, post, run, SimpleTemplate
# python built-ins
import shutil, sys, os, re, cgi, json, time, pickle, traceback

# other local modules
from common import *
import config, process
import scheduler
import apps_reader_writer as apprw

try:
    import psutil
except ImportError:
    print "INFO: /stats page disabled because psutil module not installed"

# data access layer
#from gluino import DAL, Field
from model import *
from user_data import user_dir

### session management configuration ###
from beaker.middleware import SessionMiddleware

USER_ID_SESSION_KEY = 'user_id'
APP_SESSION_KEY = 'app'
NOAUTH_USER = 'guest'

session_opts = {
    'session.type': 'file',
    'session.cookie_expires': True, # delete cookies when browser closed
    'session.data_dir': user_dir,
    'session.auto': True
}

app = SessionMiddleware(app(), session_opts)
# context processors - send to every template
try:    SimpleTemplate.defaults["tab_title"] = config.tab_title
except: SimpleTemplate.defaults["tab_title"] = "SPC"
### end session management configuration ###

# create instance of scheduler
sched = scheduler.Scheduler()

pbuffer = ''

@get('/')
def root():
    authorized()
    redirect('/myapps')

@get('/docker')
def get_docker():
    return template("error", err="This feature not enabled. Install docker-py to activate.")


@get('/static/<filepath:path>')
def server_static(filepath):
    return static_file(filepath, root='static')

@get('/favicon.ico')
def get_favicon():
    return static_file('favicon.ico', root='static')

@post('/check_user')
def check_user(user=""):
    if user == "": user = request.forms.user
    """Server-side AJAX function to check if a username exists in the DB."""
    # return booleans as strings here b/c they get parsed by JavaScript
    if users(user=user.lower()): return 'true'
    else: return 'false'

# this shows a listing of all files and allows the user to pick
# which one to use
#@get('/upload_contents/<appname>/<fn>')
#def select_input_file(appname, fn):
#    path = os.path.join(apprw.apps_dir, appname, fn)
#    params = {'fn': fn, 'contents': slurp_file(path), 'appname': appname }
#    return template('appconfig/step3', params)


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
    try: config.worker
    except: config.worker = "local"

    try: config.auth
    except: config.auth = False

    try: config.np
    except: config.np = 1

    try: config.port
    except: config.port = 8580

    return None

def getuser():
    '''Return the current user, if logged in'''
    authorized()
    return user

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
    # set user session if authentication is disabled
    if not config.auth:
        s = {USER_ID_SESSION_KEY: NOAUTH_USER}
        user = s[USER_ID_SESSION_KEY]
    # load apps into memory
    load_apps()
    # for local workers, start a polling thread to continuously check for queued jobs
    # if worker == "local": sched.poll()
    sched.poll()

    # merge in other routes and modules

    # attempt to mix in docker functionality
    try:
        import container as dockermod
        dockermod.bind(globals())
        app.app.merge(dockermod.dockerMod)
    except (ImportError, Exception):
        exc_type, exc_value, exc_traceback = sys.exc_info()
        print traceback.print_exception(exc_type, exc_value, exc_traceback)
        print "INFO: docker options disabled because docker-py module not installed"

    import plots as plotsmod
    plotsmod.bind(globals())
    app.app.merge(plotsmod.routes)

    import jobs as jobsmod
    jobsmod.bind(globals())
    app.app.merge(jobsmod.routes)

    try:
        import aws as awsmod
        awsmod.bind(globals())
        app.app.merge(awsmod.routes)
    except ImportError:
        print "INFO: disabling AWS menu because boto module not installed"

    import user_data
    user_data.bind(globals())
    app.app.merge(user_data.routes)

    import account
    account.bind(globals())
    app.app.merge(account.routes)

    import admin
    admin.bind(globals())
    app.app.merge(admin.routes)

    import apps as appmod
    appmod.bind(globals())
    app.app.merge(appmod.routes)

    import execute
    execute.bind(globals())
    app.app.merge(execute.routes)

    import util
    util.bind(globals())
    app.app.merge(util.routes)

    # run the app
    try:
        run(server=config.server, app=app, host='0.0.0.0', \
            port=config.port, debug=False)
    except:
        run(app=app, host='0.0.0.0', port=config.port, debug=False)
