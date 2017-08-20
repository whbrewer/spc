# web framework
from bottle import template, static_file, request, redirect, app, get, post, run, SimpleTemplate
# python built-ins
import shutil, sys, os, re, cgi, json, time, pickle, traceback
try:
    import requests
except:
    print "INFO: not importing requests... only needed for remote workers"
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

@post('/confirm')
def confirm_form():
    user = authorized()
    app = request.forms.app

    # generate a random case id
    # force the first string to be a letter so that the case id
    # will be guaranteed to be a string
    while True:
        cid = rand_cid()
        run_dir = os.path.join(user_dir, user, app, cid)
        # check if this case exists or not, if it exists generate a new case id
        if not os.path.isdir(run_dir): break

    # pass the case_id to be used by the program input parameters,
    # if case_id is defined in the input deck it will be used
    # otherwise it is ignored
    request.forms['case_id'] = cid
    request.forms['cid'] = cid
    request.forms['user'] = user

    try:
        desc = request.forms['desc']
    except:
        desc = "None"
    desc = desc.replace(',', ', ')

    # set config.submit_type to default value if not set in config.py file
    try:    config.submit_type
    except: config.submit_type = "default"

    if config.submit_type == 'remote':

        request.forms['np'] = 1
        request.forms['desc'] = desc
        request.forms['appmod'] = pickle.dumps(myapps[app])

        try:
            print config.remote_worker_url + '/execute'
            resp = requests.post(config.remote_worker_url +'/execute', data=dict(request.forms), verify=False)

        except:
            exc_type, exc_value, exc_traceback = sys.exc_info()
            print traceback.print_exception(exc_type, exc_value, exc_traceback)
            return template('error', err="failed to submit job to SPC worker. " + \
                "Possible solutions: Is a container running? Is Python requests " + \
                "package installed? (pip install requests)")
        else:
            jid = resp.text
            # insert job entry in local DB; scheduler will also insert entry in remote DB
            pry = 1
            uid = users(user=user).id
            db.jobs.insert(uid=uid, app=app, cid=cid, state=jid, description=desc,
                           time_submit=time.asctime(), np=config.np, priority=pry)
            db.commit()
            redirect("/case?app="+app+"&cid="+str(cid)+"&jid="+str(jid))

    elif config.submit_type == 'noverify':
        # "noverify" means don't echo the parameters back to the user before running
        # the simulation.  Just run the simulation when user submits the parameters

        # replace placeholder tags in the command line, e.g. <cid> with appropriate params
        request.forms['rel_apps_path'] = (os.pardir + os.sep)*4 + apprw.apps_dir
        myapps[app].write_params(request.forms, user)

        cmd = apps(name=app).command
        cmd = replace_tags(cmd, request.forms)
        outfn = app + ".out"
        cmd = cmd + ' > ' + outfn + ' 2>&1 '
        print "cmd:", cmd
        # following two params are temporary solutions
        np = 1
        walltime = 60
        uid = users(user=user).id
        priority = db(users.user==user).select(users.priority).first().priority
        jid = sched.qsub(app, cid, uid, cmd, np, priority, walltime, desc)
        redirect("/case?app="+app+"&cid="+str(cid)+"&jid="+str(jid))

    else:

        run_dir = os.path.join(user_dir, user, myapps[app].appname, cid)
        fn = os.path.join(run_dir, myapps[app].simfn)

        # this app-specific code should be removed in future
        # this writes a customized forsim script needed to run the simulation
        if app == "forsim":
            inputs = request.forms.script.decode('utf-8')
            inputs = inputs.replace(u'\r\n', '\n')
            if not os.path.exists(run_dir): os.makedirs(run_dir)
            thisfn = os.path.join(run_dir, "input.sim")
            with open(thisfn, 'w') as f: f.write(inputs)

        myapps[app].write_params(request.forms, user)

        # read the file
        inputs = slurp_file(fn)

        # convert html tags to entities (e.g. < to &lt;)
        inputs = cgi.escape(inputs)

        # attempt to get number of procs from forms inputs
        if 'num_procs' in request.forms:
            np = request.forms.num_procs
        else:
            np = 1

        params = { 'cid': cid, 'inputs': inputs, 'app': app,
                   'user': user, 'nap': config.np, 'np': np, 'desc': desc }
        # try:
        return template('confirm', params)
        # except:
        #     return 'ERROR: failed to write parameters to file'

@post('/execute')
def execute():
    user = authorized()
    app = request.forms.app
    cid = request.forms.cid
    np = int(request.forms.np) or 1
    walltime = request.forms.walltime
    desc = request.forms.desc
    #priority = request.forms.priority
    params = {}
    # base_dir = os.path.join(user_dir, user, app, cid)

    inputs, _, _ = myapps[app].read_params(user, cid)
    # in addition to supporting input params, also support case id
    if "cid" not in inputs: inputs["cid"] = cid

    # if preprocess is set run the preprocessor
    # try:
    #     if myapps[app].preprocess:
    #         processed_inputs = process.preprocess(inputs,
    #                                    myapps[app].preprocess,base_dir)
    # except:
    #     exc_type, exc_value, exc_traceback = sys.exc_info()
    #     print traceback.print_exception(exc_type, exc_value, exc_traceback)
    #     return template('error', err="There was an error with the preprocessor")

    cmd = apps(name=app).command

    # for parallel runs
    if np > 1: cmd = config.mpirun + " -np " + str(np) + " " + cmd

    # this is the relative path to the executable from the case directory where
    # the simulation files are stored
    inputs['rel_apps_path'] = (os.pardir + os.sep)*4 + apprw.apps_dir

    # replace placeholder tags in the command line, e.g. <cid> with appropriate params
    cmd = replace_tags(cmd, inputs)

    outfn = app + ".out"
    cmd = cmd + ' > ' + outfn + ' 2>&1 '
    print "cmd:", cmd

    # submit job to queue
    try:
        params['cid'] = cid
        params['app'] = app
        params['user'] = user
        priority = db(users.user==user).select(users.priority).first().priority
        uid = users(user=user).id
        jid = sched.qsub(app, cid, uid, cmd, np, priority, walltime, desc)
        redirect("/case?app="+app+"&cid="+cid+"&jid="+jid)
    except OSError, e:
        exc_type, exc_value, exc_traceback = sys.exc_info()
        print traceback.print_exception(exc_type, exc_value, exc_traceback)
        print >> sys.stderr, "Execution failed:", e
        params = { 'cid': cid, 'output': pbuffer, 'app': app, 'user': user, 'err': e }
        return template('error', params)

@get('/<app>/<cid>/tail')
def tail(app, cid):
    user = authorized()
    # submit num_lines as form parameter
    num_lines = int(request.query.num_lines) or 24
    progress = 0
    complete = 0
    if config.worker == 'remote':
        myparams = {'user': user, 'app': app, 'cid': cid}
        resp = requests.get(config.remote_worker_url +'/output', params=myparams)
        output = resp.text
        myoutput = output #[len(output)-num_lines:]
        # xoutput = ''.join(myoutput)
        xoutput = myoutput
        ofn = 'remote'
    else:
        run_dir = os.path.join(user_dir, user, myapps[app].appname, cid)
        ofn = os.path.join(run_dir, myapps[app].outfn)
        if os.path.exists(ofn):
            f = open(ofn,'r')
            output = f.readlines()
            # custom mendel mods for progress bar
            for line in output:
                m = re.search("num_generations\s=\s*(\d+)", line)
                if m:
                    complete = int(m.group(1))
                if complete > 0:
                    m = re.match("generation\s=\s*(\d+)", line)
                    if m: progress = int(float(m.group(1))/float(complete)*100)
            # end mendel mods
            start_position = len(output) - num_lines
            if start_position > 0:
                myoutput = output[start_position:]
            else:
                myoutput = output
            xoutput = ''.join(myoutput)
            f.close()
        elif os.path.exists(os.path.join(run_dir, myapps[app].simfn)):
            xoutput = 'waiting to start...'
        else:
            xoutput = 'Oops! It appears that the directory does not exist.  Possibly it has been deleted'

    params = { 'cid': cid, 'contents': xoutput, 'app': app,
               'user': user, 'fn': ofn, 'progress': progress }
    return template('more_contents', params)

@get('/')
def root():
    authorized()
    redirect('/myapps')

@get('/docker')
def get_docker():
    return template("error", err="This feature not enabled. Install docker-py to activate.")

@get('/stats')
def get_stats():
    authorized()
    params = {}

    # number of jobs in queued, running, and completed states
    params['nq'] = db(jobs.state=='Q').count()
    params['nr'] = db(jobs.state=='R').count()
    params['nc'] = db(jobs.state=='C').count()

    params['cpu'] = psutil.cpu_percent()
    params['vm'] = psutil.virtual_memory()
    params['disk'] = psutil.disk_usage('/')
    params['cid'] = request.query.cid
    params['app'] = request.query.app

    return template("stats", params)

@get('/stats/mem')
def get_stats_mem():
    res = {}
    try:
        res['mem'] = psutil.virtual_memory().percent
        res['cpu'] = psutil.cpu_percent()
        return json.dumps(res)
    except:
        exc_type, exc_value, exc_traceback = sys.exc_info()
        print traceback.print_exception(exc_type, exc_value, exc_traceback)
        pass


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

@get('/notifications')
def get_notifications():
    user = authorized()
    response = dict()
    response['new_shared_jobs'] = users(user=user).new_shared_jobs
    return json.dumps(response)

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

    # run the app
    try:
        run(server=config.server, app=app, host='0.0.0.0', \
            port=config.port, debug=False)
    except:
        run(app=app, host='0.0.0.0', port=config.port, debug=False)
