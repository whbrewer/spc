# web framework
from bottle import Bottle, template, static_file, request, redirect, app, get, post, run, delete, SimpleTemplate
# python built-ins
import uuid, shutil, string
import random, subprocess, sys, os, re
import cgi, urllib, urllib2, json, smtplib, time
import pickle
import traceback
try:
    import requests
except:
    print "INFO: not importing requests... only needed for remote workers"
# other local modules
from common import *
import config, process
import scheduler
import apps as appmod
from datetime import datetime, timedelta
from user_data import user_dir, upload_dir

try:
    import psutil
except ImportError:
    print "INFO: /stats page disabled because psutil module not installed"

# data access layer
#from gluino import DAL, Field
from model import *

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
    # cid = random.choice(string.ascii_lowercase) + str(uuid.uuid4())[:5]
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
        request.forms['rel_apps_path'] = (os.pardir + os.sep)*4 + appmod.apps_dir
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
    par_system = request.forms.par_system
    walltime = request.forms.walltime
    desc = request.forms.desc
    #priority = request.forms.priority
    params = {}
    base_dir = os.path.join(user_dir, user, app, cid)

    inputs, _, _ = myapps[app].read_params(user, cid)
    # in addition to supporting input params, also support case id
    if "cid" not in inputs: inputs["cid"] = cid

    # if preprocess is set run the preprocessor
    try:
        if myapps[app].preprocess:
            processed_inputs = process.preprocess(inputs,
                                       myapps[app].preprocess,base_dir)
    except:
        exc_type, exc_value, exc_traceback = sys.exc_info()
        print traceback.print_exception(exc_type, exc_value, exc_traceback)
        return template('error', err="There was an error with the preprocessor")

    cmd = apps(name=app).command

    # for parallel runs
    if np > 1: cmd = config.mpirun + " -np " + str(np) + " " + cmd

    # this is the relative path to the executable from the case directory where
    # the simulation files are stored
    inputs['rel_apps_path'] = (os.pardir + os.sep)*4 + appmod.apps_dir

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

def compute_stats(path):
    """compute statistics on output data"""
    xoutput = ''
    if os.path.exists(path):
        f = open(path,'r')
        output = f.readlines()
        for line in output:
            m = re.search(r'#.*$', line)
            if m:
                xoutput += line
        # app-specific: this is a temporary hack for mendel (remove in future)
        if path[-3:] == "hst":
            xoutput += output[len(output)-1]
    return xoutput

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
    user = authorized()
    redirect('/myapps')

@get('/<app>')
def show_app(app):
    # very similar to start_new_job() consider consolidating
    user = authorized()
    set_active(app)
    # parameters for return template
    if app not in myapps:
        return template('error', err="app %s is not installed" % (app))

    try:
        params = {}
        params.update(myapps[app].params)
        params['cid'] = ''
        params['app'] = app
        params['user'] = user
        params['apps'] = myapps
        return template(os.path.join('apps', app),  params)
    except:
        exc_type, exc_value, exc_traceback = sys.exc_info()
        print traceback.print_exception(exc_type, exc_value, exc_traceback)
        redirect('/app/'+app)

@get('/docker')
def get_docker():
    return template("error", err="This feature not enabled. Install docker-py to activate.")

@get('/stats')
def get_stats():
    user = authorized()
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


@get('/admin/show_users')
def admin_show_users():
    user = authorized()
    if not user == "admin":
        return template("error", err="must be admin to delete")
    result = db().select(users.ALL)
    params = { 'user': user, 'app': active_app() }
    return template('admin/users', params, rows=result)

@post('/admin/delete_user')
def admin_delete_user():
    user = authorized()
    if not user == "admin":
        return template("error", err="must be admin to delete")
    uid = request.forms.uid
    if int(uid) == 0:
        return template("error", err="can't delete admin user")

    if request.forms.del_files == "True":
        path = os.path.join(user_dir, users(uid).user)
        print "deleting files in path:", path
        if os.path.isdir(path): shutil.rmtree(path)

    del db.users[uid]
    db.commit()

    redirect("/admin/show_users")

@post('/check_user')
def check_user(user=""):
    if user == "": user = request.forms.user
    """Server-side AJAX function to check if a username exists in the DB."""
    # return booleans as strings here b/c they get parsed by JavaScript
    if users(user=user.lower()): return 'true'
    else: return 'false'

@post('/app_exists/<appname>')
def app_exists(appname):
    """Server-side AJAX function to check if an app exists in the DB."""
    appname = request.forms.appname
    # return booleans as strings here b/c they get parsed by JavaScript
    if apps(name=appname): return 'true'
    else: return 'false'

@get('/apps')
def showapps():
    user = authorized()
    q = request.query.q
    if not q:
        result = db().select(apps.ALL, orderby=apps.name)
    else:
        result = db(db.apps.name.contains(q, case_sensitive=False) |
                    db.apps.category.contains(q, case_sensitive=False) |
                    db.apps.description.contains(q, case_sensitive=False)).select()

    # find out what apps have already been activated so that a user can't activate twice
    uid = users(user=user).id
    activated = db(app_user.uid == uid).select()
    activated_apps = []
    for row in activated:
        activated_apps.append(row.appid)

    if user == "admin":
        configurable = True
    else:
        configurable = False

    params = { 'configurable': configurable, 'user': user }
    return template('apps', params, rows=result, activated=activated_apps)

@get('/myapps')
def showapps():
    user = authorized()
    uid = users(user=user).id
    app = active_app()

    result = db((apps.id == app_user.appid) & (uid == app_user.uid)).select(orderby=apps.name)
    if user == "admin":
        configurable = True
    else:
        configurable = False
    params = { 'configurable': configurable, 'user': user, 'app': app }
    return template('myapps', params, rows=result)

@get('/apps/load')
def get_load_apps():
    load_apps()
    redirect('/myapps')

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

@post('/app/edit/<appid>')
def app_edit(appid):
    user = authorized()
    if user != 'admin':
        return template('error', err="must be admin to edit app")
    cid = request.forms.cid
    app = request.forms.app
    result = db(apps.name==app).select().first()
    params = {'app': app, 'cid': cid}
    return template('app_edit', params, rows=result)

@post('/app/save/<appid>')
def app_save(appid):
    user = authorized()
    app = request.forms.app
    lang = request.forms.language
    info = request.forms.input_format
    category = request.forms.category
    preprocess = request.forms.preprocess
    postprocess = request.forms.postprocess
    assets = request.forms.assets
    if assets == "None": assets = None
    desc = request.forms.description
    row = db(db.apps.id==appid).select().first()
    row.update_record(language=lang, category=category, description=desc, input_format=info,
                      preprocess=preprocess, postprocess=postprocess, assets=assets)
    db.commit()
    redirect("/app/"+app)

# allow only admin or user to delete apps
@post('/app/delete/<appid>')
def delete_app(appid):
    user = authorized()
    if user != 'admin':
        return template('error', err="must be admin to edit app")
    appname = request.forms.app
    del_app_dir = request.forms.del_app_dir
    del_app_cases = request.forms.del_app_cases

    try:
        if user == 'admin':
            # delete entry in DB
            a = appmod.App()
            if del_app_dir == "on":
                del_files = True
            else:
                del_files = False
            myapps[appname].delete(appid, del_files)
        else:
            return template("error", err="must be admin")
    except:
        exc_type, exc_value, exc_traceback = sys.exc_info()
        print traceback.print_exception(exc_type, exc_value, exc_traceback)
        return template("error", err="failed to delete app... did the app load properly?")

    redirect("/apps")

@get('/app/<app>')
def view_app(app):
    user = authorized()
    if app: set_active(app)
    else: redirect('/myapps')

    if user != 'admin':
        return template('error', err="must be admin to edit app")
    cid = request.query.cid
    result = db(apps.name==app).select().first()
    params = {}
    params['app'] = app
    params['user'] = user
    params['cid'] = cid
    #if request.query.edit:
    #    return template('appedit', params, rows=result)
    #else:
    try:
        return template('app', params, rows=result)
    except:
        exc_type, exc_value, exc_traceback = sys.exc_info()
        print traceback.print_exception(exc_type, exc_value, exc_traceback)
        return template('error', err="there was a problem showing the app template. Check traceback.")


@post('/useapp')
def useapp():
    user = authorized()
    uid = users(user=user).id
    app = request.forms.app
    appid = apps(name=app).id
    print "allowing user", user, uid, "to access app", app, appid
    app_user.insert(uid=uid, appid=appid)
    db.commit()
    redirect('/apps')

@post('/removeapp')
def removeapp():
    user = authorized()
    uid = users(user=user).id
    app = request.forms.app
    appid = apps(name=app).id
    auid = app_user(uid=uid, appid=appid).id
    del app_user[auid]
    print "removing user", user, uid, "access to app", app, appid
    db.commit()
    redirect('/myapps')

@get('/addapp')
def getaddapp():
    user = authorized()
    if user != 'admin':
        return template('error', err="must be admin to add app")
    return template('appconfig/addapp')

@post('/addapp')
def addapp():
    user = authorized()
    if user != 'admin':
        return template('error', err="must be admin to add app")
    appname = request.forms.appname
    input_format = request.forms.input_format
    # ask for app name
    category = request.forms.category
    language = request.forms.language
    description = request.forms.description
    command = request.forms.command
    preprocess = request.forms.preprocess
    postprocess = request.forms.postprocess
    # put in db
    a = appmod.App()
    #print "user:",user
    uid = users(user=user).id
    a.create(appname, description, category, language,
             input_format, command, preprocess, postprocess)
    # load_apps() needs to be called here in case a user wants to delete
    # this app just after it has been created... it is called again after
    # the user uploads a sample input file
    load_apps()
    redirect('/app/'+appname)

@get('/appconfig/status')
def appconfig_status():
    user = authorized()
    status = dict()
    app = request.query.app

    # check db file
    command = apps(name=app).command
    if command:
        status['command'] = 1
    else:
        status['command'] = 0

    # check template file
    if os.path.exists("views/apps/"+app+".tpl"):
        status['template'] = 1
    else:
        status['template'] = 0

    # check inputs file
    extension = {'namelist': '.in', 'ini': '.ini', 'xml': '.xml', 'json': '.json', 'yaml': '.yaml'}
    if os.path.exists(os.path.join(appmod.apps_dir, app,
                      app + extension[myapps[app].input_format])):
        status['inputs'] = 1
    else:
        status['inputs'] = 0

    # check app binary
    if os.path.exists(os.path.join(appmod.apps_dir, app, app)):
        status['binary'] = 1
    else:
        status['binary'] = 0

    # check plots
    appid = apps(name=app).id
    result = db(plots.appid==appid).select().first()
    if result:
        status['plots'] = 1
    else:
        status['plots'] = 0

    return json.dumps(status)

@post('/appconfig/exe/<step>')
def appconfig_exe(step="upload"):
    user = authorized()
    if user != 'admin':
        return template('error', err="must be admin to configure app")
    if step == "upload":
        appname = request.forms.appname
        params = {'appname': appname}
        return template('appconfig/exe_upload', params)
    elif step == "test":
        appname    = request.forms.appname
        upload     = request.files.upload
        if not upload:
            return template('appconfig/error',
                   err="no file selected. press back button and try again")
        name, ext = os.path.splitext(upload.filename)
        # if ext not in ('.exe','.sh','.xml','.json',):
        #     return 'ERROR: File extension not allowed.'
        try:
            save_path_dir = os.path.join(appmod.apps_dir, name)
            if not os.path.exists(save_path_dir):
                os.makedirs(save_path_dir)
            save_path = os.path.join(save_path_dir, name) + ext
            if os.path.isfile(save_path):
                timestr = time.strftime("%Y%m%d-%H%M%S")
                shutil.move(save_path, save_path+"."+timestr)
            upload.save(save_path)
            os.chmod(save_path, 0700)

            # process = subprocess.Popen(["otool -L", save_path], stdout=subprocess.PIPE, stdin=subprocess.PIPE)
            # contents = process.readlines()
            contents = "SUCCESS"

            params = {'appname': appname, 'contents': contents}
            return template('appconfig/exe_test', params)
        except IOError:
            exc_type, exc_value, exc_traceback = sys.exc_info()
            print traceback.print_exception(exc_type, exc_value, exc_traceback)
            return "IOerror:", IOError
        else:
            return "ERROR: must be already a file"

@post('/appconfig/export')
def export():
    user = authorized()
    if user != 'admin':
        return template('error', err="must be admin to use export function")
    app = request.forms.app
    result = db(apps.name==app).select().first()

    data = {}
    data['name'] = result.name
    data['description'] = result.description
    data['category'] = result.category
    data['language'] = result.language
    data['input_format'] = result.input_format
    data['command'] = result.command
    data['preprocess'] = result.preprocess
    data['postprocess'] = result.postprocess

    assets = list()
    if result.assets is not None:
        for asset in result.assets.split(","):
            assets.append(asset.strip())
    data['assets'] = assets

    appid = apps(name=app).id

    myplots = db(plots.appid==appid).select()
    data['plots'] = list()

    for p in myplots:
        thisplot = {}
        thisplot['ptype'] = p.ptype
        thisplot['title'] = p.title
        thisplot['options'] = p.options
        thisplot['datasource'] = list()

        myds = db(datasource.pltid==p.id).select()

        for ds in myds:
            thisds = {}
            thisds['label'] = ds.label
            thisds['filename'] = ds.filename
            thisds['cols'] = ds.cols
            thisds['line_range'] = ds.line_range
            thisds['data_def'] = ds.data_def

            thisplot['datasource'].append(thisds)

        data['plots'].append(thisplot)

    path = os.path.join(appmod.apps_dir, app, 'spc.json')
    with open(path, 'w') as outfile:
        json.dump(data, outfile, indent=3)

    return "spc.json file written to " + path + "<meta http-equiv='refresh' content='2; url=/app/"+app+"'>"

@post('/appconfig/inputs/<step>')
def edit_inputs(step):
    user = authorized()
    if user != 'admin':
        return template('error', err="must be admin to edit app")
    # upload zip file and return a text copy of the input file
    if step == "upload":
        appname = request.forms.appname
        input_format = request.forms.input_format
        params = {'appname': appname, 'input_format': input_format}
        return template('appconfig/inputs_upload', params)
    if step == "parse":
        input_format = request.forms.input_format
        appname    = request.forms.appname
        upload     = request.files.upload
        if not upload:
            return template('appconfig/error',
                   err="no file selected. press back button and try again")
        name, ext = os.path.splitext(upload.filename)
        if ext not in ('.in', '.ini', '.xml', '.json', '.yaml', ):
            return 'ERROR: File extension not allowed.'
        try:
            save_path_dir = os.path.join(appmod.apps_dir, name)
            if not os.path.exists(save_path_dir):
                os.makedirs(save_path_dir)
            save_path = os.path.join(save_path_dir, name) + ext
            if os.path.isfile(save_path):
                timestr = time.strftime("%Y%m%d-%H%M%S")
                shutil.move(save_path, save_path+"."+timestr)
            upload.save(save_path)

            # return the contents of the input file
            # this is just for namelist.input format, but
            # we need to create this dynamically based on input_format
            if input_format == "namelist":
                fn = appname + ".in"
            elif input_format == "ini":
                fn = appname + ".ini"
            elif input_format == "xml":
                fn = appname + ".xml"
            elif input_format == "json":
                fn = appname + ".json"
            elif input_format == "yaml":
                fn = appname + ".yaml"
            else:
                return "ERROR: input_format not valid: ", input_format
            path = os.path.join(appmod.apps_dir, appname, fn)
            # cgi.escape converts HTML chars like > to entities &gt;
            contents = cgi.escape(slurp_file(path))
            params = {'fn': fn, 'contents': contents, 'appname': appname,
                      'input_format': input_format }
            return template('appconfig/inputs_parse', params)
        except IOError:
            exc_type, exc_value, exc_traceback = sys.exc_info()
            print traceback.print_exception(exc_type, exc_value, exc_traceback)
            return "IOerror:", IOError
        else:
            return "ERROR: must be already a file"
    # show parameters with options how to tag and describe each parameter
    elif step == "create_view":
        input_format = request.forms.input_format
        appname = request.forms.appname
        myapp = app_instance(input_format, appname)
        inputs, _, _ = myapp.read_params()
        print "inputs:", inputs
        params = { "appname": appname }
        return template('appconfig/inputs_create_view', params, inputs=inputs,
                                        input_format=input_format)
    # create a template in the views/apps folder
    elif step == "end":
        appname = request.forms.get('appname')
        html_tags = request.forms.getlist('html_tags')
        data_type = request.forms.getlist('data_type')
        descriptions = request.forms.getlist('descriptions')
        bool_rep = request.forms.bool_rep
        keys = request.forms.getlist('keys')
        key_tag = dict(zip(keys, html_tags))
        key_desc = dict(zip(keys, descriptions))
        input_format = request.forms.input_format
        myapp = app_instance(input_format, appname)
        params, _, _ = myapp.read_params()
        if myapp.create_template(html_tags=key_tag, bool_rep=bool_rep, desc=key_desc):
            load_apps()
            params = { "appname": appname, "port": config.port }
            return template('appconfig/inputs_end', params)
        else:
            return "ERROR: there was a problem when creating view"
    else:
        return template('error', err="step not supported")

# this shows a listing of all files and allows the user to pick
# which one to use
#@get('/upload_contents/<appname>/<fn>')
#def select_input_file(appname, fn):
#    path = os.path.join(appmod.apps_dir, appname, fn)
#    params = {'fn': fn, 'contents': slurp_file(path), 'appname': appname }
#    return template('appconfig/step3', params)

@get('/notifications')
def get_notifications():
    user = authorized()
    response = dict()
    response['new_shared_jobs'] = users(user=user).new_shared_jobs
    return json.dumps(response)

def app_instance(input_format, appname, preprocess=0, postprocess=0):
    if(input_format=='namelist'):
        myapp = appmod.Namelist(appname, preprocess, postprocess)
    elif(input_format=='ini'):
        myapp = appmod.INI(appname, preprocess, postprocess)
    elif(input_format=='xml'):
        myapp = appmod.XML(appname, preprocess, postprocess)
    elif(input_format=='json'):
        myapp = appmod.JSON(appname, preprocess, postprocess)
    elif(input_format=='yaml'):
        myapp = appmod.YAML(appname, preprocess, postprocess)
    elif(input_format=='toml'):
        myapp = appmod.TOML(appname, preprocess, postprocess)
    else:
        return 'ERROR: input_format', input_format, 'not supported'
    return myapp

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
    user = authorized()
    return user

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
    except (ImportError, Exception) as e:
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

    # run the app
    try:
        run(server=config.server, app=app, host='0.0.0.0', \
            port=config.port, debug=False)
    except:
        run(app=app, host='0.0.0.0', port=config.port, debug=False)
