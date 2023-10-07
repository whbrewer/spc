from __future__ import print_function
from __future__ import absolute_import
# web framework
from flask import Flask, request, redirect, session, render_template, send_from_directory


# python built-ins
import os, sys, traceback, importlib

# other local modules
from . import config, scheduler, app_reader_writer as apprw
from .model import db, Apps
from .user_data import user_dir
from .constants import USER_ID_SESSION_KEY, APP_SESSION_KEY, NOAUTH_USER

app = Flask(__name__)
app.secret_key = '40dd942d0f03108a84db8697e0307802'  # for sessions

### end session management configuration ###

#@app.context_processor
#def inject_tab_title():
#    return dict(tab_title=config.tab_title)

# create an instance of the scheduler
sched = scheduler.Scheduler()

# a few generic routes
@app.route('/')
def hello_world():
    return 'Hello, World!'

#@app.route('/')
#def root():
#    authorized()
#    redirect('/myapps')

@app.route('/static/<path:filepath>')
def server_static(filepath):
    return send_from_directory('static', filepath)

@app.route('/favicon.ico')
def get_favicon():
    return send_from_directory('static', filepath)


@app.errorhandler(500)
@app.errorhandler(501)
@app.errorhandler(502)
def error500(error):
    msg = error.exception.message + " (" + str(error.status_code) + ")"
    trace = error.traceback
    return template('error', err=msg, traceback=trace)

def authorized():
    '''Return username if user is already logged in, redirect otherwise'''
    if config.auth:
        username = session.get(USER_ID_SESSION_KEY)
        if not username:
            redirect('/login')
        else:
            return username
    else:
        return NOAUTH_USER

def active_app():
    s = request.environ.get('beaker.session')
    try:
        return s[APP_SESSION_KEY]
    except:
        return None

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
    result = Apps.select()
    myapps = {}
    for row in result:
        name = row.name
        appid = row.id
        preprocess = row.preprocess
        postprocess = row.postprocess
        input_format = row.input_format
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

def main():
    from . import util

    init_config_options()
    load_apps()

    # for local workers, start a polling thread to continuously check for queued jobs
    # if worker == "local": sched.poll()
    #sched.poll()

    ## merge in other routes and modules

    modules = ["account", "admin", "app_routes", "aws", "container",
               "execute", "jobs", "plots", "user_data", "util"]

    for module in modules:
        try:
            # Import the module
            imported_module = importlib.import_module('.' + module, 'spc')
            
            # Register the blueprint from the imported module
            # Assuming each module has a blueprint named 'routes'
            #app.register_blueprint(imported_module.routes)
            #app.register_blueprint(getattr(imported_module, module))
            
        except ImportError:
            print("ERROR importing module " + module)

    ## Log CPU and Memory history to log files
    # util.MachineStatsLogger(interval=5, function=util.print_machine_stats)
    # util.setup_rotating_handler(1000, 3)

    ## start up the web server

    # run the app using server specified in config.py
    #if config.server != 'uwsgi':
    #app.run(host='0.0.0.0', port=config.port, debug=False)
    app.run()

#if config.server == 'uwsgi': main()


