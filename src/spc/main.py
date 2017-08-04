# web framework
from bottle import Bottle, template, static_file, request, redirect, app, get, post, run, delete, SimpleTemplate
# python built-ins
import uuid, hashlib, shutil, string
import random, subprocess, sys, os, re
import cgi, urllib, urllib2, json, smtplib, time
import pickle
import traceback
try:
    import requests
except:
    print "INFO: not importing requests... only needed for remote workers"
# other local modules
from common  import *
import config, process
import scheduler
import apps as appmod
import plots as plotmod
from datetime import datetime, timedelta
from user_data import user_dir, upload_dir

# requires boto
try:
    import aws as awsmod
except ImportError:
    print "INFO: disabling AWS menu because boto module not installed"

# requires docker-py
try:
    import container as dockermod
except ImportError:
    print "INFO: docker options disabled because docker-py module not installed"

#
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

@get('/more')
def more():
    """given a form with the attribute plotpath,
       output the file to the browser"""
    user = authorized()
    app = request.query.app
    cid = request.query.cid
    filepath = request.query.filepath
    contents = slurp_file(filepath)
    # convert html tags to entities (e.g. < to &lt;)
    contents = cgi.escape(contents)
    params = { 'cid': cid, 'contents': contents, 'app': app, 'user': user, 'fn': filepath }
    return template('more', params)

@get('/case')
def case():
    user = authorized()
    app = request.query.app
    set_active(app)
    cid = request.query.cid
    jid = request.query.jid

    # note: eventually need to merge the following two into one
    if re.search("/", cid):
        (owner, c) = cid.split("/")
        state = jobs(cid=c).state
        sid = request.query.sid # id of item in shared
        run_dir = os.path.join(user_dir, owner, myapps[app].appname, c)
        fn = os.path.join(run_dir, myapps[app].outfn)
        output = slurp_file(fn)

        params = { 'cid': cid, 'app': app, 'contents': output,
                   'sid': sid, 'user': user, 'fn': fn, 'state': state, 'owner': owner }

        if jid: params['jid'] = jid

        return template('case_public', params)

    else:
        owner = user
        state = jobs(cid=cid).state
        run_dir = os.path.join(user_dir, user, myapps[app].appname, cid)
        fn = os.path.join(run_dir, myapps[app].outfn)
        result = db(jobs.cid==cid).select().first()
        desc = result['description']
        shared = result['shared']

        params = { 'cid': cid, 'app': app, 'jid': jid,
                   'user': user, 'fn': fn, 'description': desc, 'shared': shared,
                   'state': state, 'owner': owner }

        if jid: params['jid'] = jid

        return template('case', params)

@get('/output')
def output():
    user = authorized()
    app = request.query.app
    cid = request.query.cid
    jid = request.query.jid
    print "jid:", jid


    try:
        if re.search("/", cid):
            (owner, c) = cid.split("/")
        else:
            owner = user
            c = cid

        run_dir = os.path.join(user_dir, owner, myapps[app].appname, c)
        fn = os.path.join(run_dir, myapps[app].outfn)

        if config.worker == 'remote':

            params = {'user': user, 'app': app, 'cid': cid}
            resp = requests.get(config.remote_worker_url +'/output', params=params)
            output = resp.text

        else:

            output = slurp_file(fn)
            # the following line will convert HTML chars like > to entities &gt;
            # this is needed so that XML input files will show paramters labels
            output = cgi.escape(output)

        desc = jobs(cid=c).description

        params = { 'cid': cid, 'contents': output, 'app': app,
                   'user': owner, 'owner': owner, 'fn': fn, 'description': desc }

        if jid: params['jid'] = jid

        return template('more', params)

    except:
        params = { 'app': app, 'err': "Couldn't read input file. Check casename." }
        exc_type, exc_value, exc_traceback = sys.exc_info()
        print traceback.print_exception(exc_type, exc_value, exc_traceback)
        return template('error', params)

@get('/inputs')
def inputs():
    user = authorized()
    app = request.query.app
    cid = request.query.cid
    try:
        if re.search("/", cid):
            (owner, c) = cid.split("/")
        else:
            owner = user
            c = cid
        run_dir = os.path.join(user_dir, owner, myapps[app].appname, c)
        fn = os.path.join(run_dir, myapps[app].simfn)
        inputs = slurp_file(fn)
        # the following line will convert HTML chars like > to entities &gt;
        # this is needed so that XML input files will show paramters labels
        inputs = cgi.escape(inputs)

        desc = jobs(cid=c).description

        params = { 'cid': cid, 'contents': inputs, 'app': app, 'user': owner,
                   'fn': fn, 'description': desc }
        return template('more', params)
    except:
        params = { 'app': app, 'err': "Couldn't read input file. Check casename." }
        exc_type, exc_value, exc_traceback = sys.exc_info()
        print traceback.print_exception(exc_type, exc_value, exc_traceback)
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

@get('/jobs')
def show_jobs():
    user = authorized()
    #if app not in myapps: redirect('/apps')
    cid = request.query.cid
    app = request.query.app or active_app()
    n = int(request.query.n or config.jobs_num_rows)
    q = request.query.q
    starred = request.query.starred
    shared = request.query.shared
    uid = users(user=user).id

    if starred:
        result = db((jobs.uid==uid) & (jobs.starred=="True")).select(orderby=~jobs.id)[:n]
    elif shared:
        result = db(jobs.shared=="True").select(orderby=~jobs.id)[:n]
    elif q:
        query_array = [ tuple(qa.strip().split(":")) for qa in q.strip().split() ]

        if len(query_array) == 1:

            if len(query_array[0]) == 1: # for general case search 3 main fields: cid, app, labels
                result = db((jobs.uid==uid) & \
                           ((db.jobs.cid.contains(q.encode('utf8'), case_sensitive=False)) |
                            (db.jobs.app.contains(q.encode('utf8'), case_sensitive=False)) |
                            (db.jobs.description.contains(q.encode('utf8'), case_sensitive=False)))).select(orderby=~jobs.id)

            else: # in the case of specific tag searching, e.g. app:mendel
                key = query_array[0][0]
                query = query_array[0][1]

                if key == "user" and user == "admin":
                    if query == "all":
                        result = db().select(jobs.ALL, orderby=~jobs.id)[:n]
                    else:
                        this_id = users(user=query).id
                        result = db(jobs.uid==this_id).select(orderby=~jobs.id)[:n]
                elif key == "cid":
                    result = db((jobs.uid==uid) & \
                        (db.jobs.cid.contains(query, case_sensitive=False))).select(orderby=~jobs.id)
                elif key == "app":
                    result = db((jobs.uid==uid) & (jobs.app==query)).select(orderby=~jobs.id)
                elif key =="np":
                    result = db((jobs.uid==uid) & (jobs.np==query)).select(orderby=~jobs.id)
                elif key == "is":
                    if query == "starred":
                        result = db((jobs.uid==uid) & (jobs.starred=="True")).select(
                                 orderby=~jobs.id)[:n]
                    elif query == "shared":
                        result = db(jobs.shared=="True").select(orderby=~jobs.id)[:n]
                elif key == "state":
                    result = db((jobs.uid==uid) & (db.jobs.state==query)).select(orderby=~jobs.id)
                elif key == "label":
                    result = db((db.jobs.uid==uid) & (db.jobs.description.contains(
                                 query, case_sensitive=False))).select(orderby=~jobs.id)
                elif key == "after" or key == "before":
                    if len(query) != 8:
                        return template('error', err="date format must be YY/MM/DD, e.g. after:16/12/01")
                    rows = db(jobs.uid==uid).select(orderby=~jobs.id)
                    result = []
                    for row in rows:
                        a = datetime.strptime(row.time_submit, "%a %b %d %H:%M:%S %Y")
                        b = datetime.strptime(query, "%y/%m/%d")
                        if key == "after":
                            if a-b > timedelta(days=0): result.append(row)
                        else:
                            if a-b < timedelta(days=0): result.append(row)
                else:
                    return template('error', err="search key not supported: "+key)

        elif len(query_array) == 2: # the case when user search with both after and before dates
            key1, query1 = query_array[0][0], query_array[0][1]
            key2, query2 = query_array[1][0], query_array[1][1]
            if len(query1) != 8 or len(query2) != 8:
                return template('error', err="date format must be YY/MM/DD, e.g. after:16/12/01")
            if key1 == "after" and key2 == "before" or key1 == "before" and key2 == "after":
                rows = db(jobs.uid==uid).select(orderby=~jobs.id)
                result = []
                for row in rows:
                    a = datetime.strptime(row.time_submit, "%a %b %d %H:%M:%S %Y")
                    b = datetime.strptime(query1, "%y/%m/%d")
                    c = datetime.strptime(query2, "%y/%m/%d")
                    if key1 == "after":
                        if a-b > timedelta(days=0) and a-c < timedelta(days=0): result.append(row)
                    else:
                        if a-c > timedelta(days=0) and a-b < timedelta(days=0): result.append(row)
            else:
                return template('error', err="search type not supported")

        else:
            return template('error', err="search type not supported")
    else:
        result = db(jobs.uid==uid).select(orderby=~jobs.id)[:n]

    # number of jobs in queued state
    params = {}
    params['q'] = q
    params['cid'] = cid
    params['app'] = app
    params['user'] = user
    params['np'] = config.np
    params['n'] = n
    params['status'] = "showing " + str(len(result)) + " cases"
    params['num_rows'] = config.jobs_num_rows
    return template('jobs', params, rows=result)

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

@get('/jobs/new')
def start_new_job():
    user = authorized()
    app = request.query.app or active_app()

    if app: set_active(app)
    else: redirect('/myapps')

    if config.auth and not authorized(): redirect('/login')
    if myapps[app].appname not in myapps: redirect('/apps')
    cid = request.query.cid
    if re.search("/", cid):
        owner, cid = cid.split("/")
    else:
        owner = user

    # read default params... this ensures no 500 error when restarting
    # in case params are missing
    params = {}
    params.update(myapps[app].params)
    # pass by value not by reference to avoid apps templates modifying
    # the myapps dictionary

    # if restarting from old case
    if re.search("[a-z]", cid):
        params, _, _ = myapps[app].read_params(owner, cid)
        if user == owner:
            params['tags'] = cid
        else:
            params['tags'] = os.path.join(owner, cid)

    params['cid'] = cid
    params['app'] = app
    params['user'] = user
    params['apps'] = myapps
    try:
        return template('apps/' + myapps[app].appname, params)
    except:
        exc_type, exc_value, exc_traceback = sys.exc_info()
        print traceback.print_exception(exc_type, exc_value, exc_traceback)
        return template('error', err="there was a problem with the template. Check traceback.")

@get('/jobs/diff')
def diff_jobs():
    user = authorized()
    app = active_app()

    selected_cases = request.query.selected_diff_cases
    cases = selected_cases.rstrip(':').split(':')

    cids = list()
    contents = list()
    for jid in cases:
        cid = jobs(jid).cid
        cids.append(cid)
        app = jobs(jid).app
        base_dir = os.path.join(user_dir, user, myapps[app].appname)
        fn = os.path.join(base_dir, cid, myapps[app].simfn)
        content = slurp_file(fn).splitlines(1)
        contents.append(content)

    inputs = slurp_file(fn)
    import difflib
    d = difflib.Differ()
    result = list(d.compare(contents[0], contents[1]))
    title = "diff " + cids[0] + " " + cids[1]

    params = { 'cid': cid, 'contents': ' '.join(result), 'app': app, 'user': user, 'fn': title }
    return template('more', params)

@get('/docker')
def get_docker():
    return template("error", err="This feature not enabled. Install docker-py to activate.")

@get('/aws')
def get_aws():
    user = authorized()
    cid = request.query.cid
    app = request.query.app or active_app()
    uid = db(users.user==user).select(users.id).first()
    #creds = db().select(db.aws_creds.ALL)
    creds = db(aws_creds.uid==uid).select()
    # look for aws instances registered by the current user
    # which means first need to get the uid
    instances = db(aws_instances.uid==uid).select()
    params = {}
    params['cid'] = cid
    params['app'] = app
    params['user'] = user
    if request.query.status:
        params['status'] = request.query.status
    return template('aws', params, creds=creds, instances=instances)

@post('/aws/creds')
def post_aws_creds():
    user = authorized()
    a = request.forms.account_id
    s = request.forms.secret
    k = request.forms.key
    uid = users(user=user).id
    db.aws_creds.insert(account_id=a, secret=s, key=k, uid=uid)
    db.commit()
    redirect('/aws')

@delete('/aws/creds/<id>')
def aws_cred_del(id):
    user = authorized()
    del db.aws_creds[id]
    db.commit()
    redirect('/aws')

@post('/aws/instance')
def create_instance():
    """create instance"""
    user = authorized()
    instance = request.forms.instance
    itype = request.forms.itype
    region = request.forms.region
    rate = request.forms.rate
    uid = users(user=user).id
    db.aws_instances.insert(instance=instance, itype=itype, region=region, rate=rate, uid=uid)
    db.commit()
    redirect('/aws')

@delete('/aws/instance/<aid>')
def del_instance(aid):
    user = authorized()
    try:
        del aws_instances[aid]
        db.commit()
        return "true"
    except:
        exc_type, exc_value, exc_traceback = sys.exc_info()
        print traceback.print_exception(exc_type, exc_value, exc_traceback)
        return "false"

def aws_conn(id):
    """create a connection to the EC2 machine and return the handle"""
    user = authorized()
    uid = users(user=user).id
    creds = db(db.aws_creds.uid==uid).select().first()
    account_id = creds['account_id']
    secret = creds['secret']
    key = creds['key']
    instances = db(db.aws_instances.id==id).select().first()
    instance = instances['instance']
    region = instances['region']
    rate = instances['rate'] or 0.
    return awsmod.EC2(key, secret, account_id, instance, region, rate)

@get('/aws/status/<aid>')
def aws_status(aid):
    user = authorized()
    cid = request.query.cid
    app = request.query.app
    params = {}
    params['aid'] = aid
    params['cid'] = cid
    params['app'] = app
    params['user'] = user
    params['port'] = config.port
    if awsmod:
        a = aws_conn(aid)
    else:
        return template('error', err="To use this feature, you need to install the Python boto libs see <a href=\"https://pypi.python.org/pypi/boto/\">https://pypi.python.org/pypi/boto/</a>")
    try:
        astatus = a.status()
        if astatus['state'] == "running":
            astatus['uptime'] = a.uptime(astatus['launch_time'])
            astatus['charge since last boot'] = a.charge(astatus['uptime'])
        return template('aws_status', params, astatus=astatus)
    except:
        exc_type, exc_value, exc_traceback = sys.exc_info()
        print traceback.print_exception(exc_type, exc_value, exc_traceback)
        return template('error', err="There was a problem connecting to the AWS machine. Check the credentials and make sure the machine is running.")

@post('/aws/<aid>')
def aws_start(aid):
    user = authorized()
    a = aws_conn(aid)
    a.start()
    # takes a few seconds for the status to change on the Amazon end
    time.sleep(15)

@delete('/aws/<aid>')
def aws_stop(aid):
    user = authorized()
    a = aws_conn(aid)
    a.stop()
    # takes a few seconds for the status to change on the Amazon end
    time.sleep(10)

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

@get('/account')
def get_account():
    user = authorized()
    app = request.query.app or active_app()
    params = {}
    params['app'] = app
    params['user'] = user
    uid = users(user=user).id
    return template('account', params)

@post('/jobs/annotate')
def annotate_job():
    user = authorized()
    app = request.forms.app
    cid = request.forms.cid
    # jid = request.forms.jid
    desc = request.forms.description
    desc = desc.replace(',', ', ')
    jobs(cid=cid).update_record(description=desc)
    db.commit()
    redirect('/jobs')

@post('/jobs/star')
def star_case():
    user = authorized()
    jid = request.forms.jid
    jobs(id=jid).update_record(starred="True")
    db.commit()
    redirect('/jobs')

@post('/jobs/unstar')
def unstar_case():
    user = authorized()
    jid = request.forms.jid
    jobs(id=jid).update_record(starred="False")
    db.commit()
    redirect('/jobs')

@post('/jobs/share')
def share_case():
    user = authorized()
    app = request.forms.app
    cid = request.forms.cid
    jid = request.forms.jid
    jobs(id=jid).update_record(shared="True")
    db.commit()
    # increase count in database for every user
    for u in db().select(users.ALL):
        nmsg = users(user=u.user).new_shared_jobs or 0
        users(user=u.user).update_record(new_shared_jobs=nmsg+1)
    db.commit()
    redirect('/jobs')

@post('/jobs/unshare')
def unshare_case():
    user = authorized()
    app = request.forms.app
    cid = request.forms.cid
    jid = request.forms.jid
    jobs(id=jid).update_record(shared="False")
    db.commit()
    redirect('/jobs')

@get('/jobs/all')
def get_all_jobs():
    user = authorized()
    if not user == "admin":
        return template("error", err="must be admin to use this feature")
    cid = request.query.cid
    app = request.query.app or active_app()
    n = request.query.n
    if not n:
        n = config.jobs_num_rows
    else:
        n = int(n)
    # sort by descending order of jobs.id
    result = db((db.jobs.uid==users.id)).select(orderby=~jobs.id)[:n]

    # clear notifications
    users(user=user).update_record(new_shared_jobs=0)
    db.commit()

    params = {}
    params['cid'] = cid
    params['app'] = app
    params['user'] = user
    params['n'] = n
    params['num_rows'] = config.jobs_num_rows
    return template('shared', params, rows=result)

@get('/jobs/shared')
def get_shared():
    """Return the records from the shared table."""
    user = authorized()
    cid = request.query.cid
    app = request.query.app or active_app()
    n = request.query.n
    if not n:
        n = config.jobs_num_rows
    else:
        n = int(n)
    # sort by descending order of jobs.id
    result = db((db.jobs.shared=="True") & (db.jobs.uid==users.id)).select(orderby=~jobs.id)[:n]
    # result = db((db.jobs.shared=="True") &
    #             (jobs.gid == users.gid)).select(orderby=~jobs.id)[:n]

    # clear notifications
    users(user=user).update_record(new_shared_jobs=0)
    db.commit()

    params = {}
    params['cid'] = cid
    params['app'] = app
    params['user'] = user
    params['n'] = n
    params['num_rows'] = config.jobs_num_rows
    return template('shared', params, rows=result)

@post('/jobs/delete/<jid>')
def delete_job(jid):
    user = authorized()
    app = request.forms.app
    cid = request.forms.cid
    state = jobs(jid).state

    if re.search("/", cid):
        return template("error", err="only possible to delete cases that you own")

    if state != "R":
        path = os.path.join(user_dir, user, app, cid)
        if os.path.isdir(path): shutil.rmtree(path)
        sched.stop(jid)
        sched.qdel(jid)
    else:
        return template("error", err="cannot delete while job is still running")
    redirect("/jobs")

@post('/jobs/merge/<rtype>')
def merge(rtype):
    user = authorized()
    selected_cases = request.forms.selected_merge_cases
    jids = selected_cases.rstrip(':').split(':')
    cases = list()
    output = dict()

    for jid in jids:
        app = jobs(id=jid).app
        cid = jobs(id=jid).cid
        cases.append(cid)
        relpath = os.path.join(app, cid)
        fn = replace_tags(request.forms.file_pattern, {'cid': cid})
        path = os.path.join(user_dir, user, app, cid, fn)

        with open(path, "r") as infile:
            # Loop over lines in each file
            for line in infile:
                line = str(line)
                # Skip comment lines
                if not re.search('^#', line):
                    items = line.split()
                    # If a line matching this one has been encountered in a previous
                    # file, add the column values
                    if len(items) > 0:
                        currkey = int(items[0])
                        if currkey in output.keys():
                            for ii in range(len(output[currkey])):
                                output[currkey][ii] += float(items[ii+1])
                        # Otherwise, add a new key to the output and create the columns
                        else:
                            output[currkey] = list(map(float, items[1:]))

    # Get total number of files for calculating average
    if rtype == "sum":
       nfile = 1
    elif rtype == "avg":
       nfile = len(cases)
    else:
       raise ValueError(rtype + " operation no supported")
    print "nfile:", nfile, selected_cases

    # generate new case_id for outputtinging merged files
    while True:
        ocid = rand_cid()
        run_dir = os.path.join(user_dir, user, app, ocid)
        # check if this case exists or not, if it exists generate a new case id
        if not os.path.exists(run_dir):
            os.makedirs(run_dir)
            break

    # write a default input file b/c SPC requires a file in each job dir
    myapps[app].params['case_id'] = ocid
    myapps[app].write_params(myapps[app].params, user)

    # Sort the output keys
    skey = sorted(output.keys())
    lines = list()
    # Loop through sorted keys and print each averaged column to stdout
    for key in skey:
        outline = str(int(key))
        for item in output[key]:
            outline += ' ' + str("{0:.3e}".format(item/nfile,3))
        lines.append(outline)

    ofn = replace_tags(request.forms.file_pattern, {'cid': ocid})
    with open(os.path.join(run_dir, ofn), 'w') as f:
        f.writelines("%s\n" % l for l in lines)

    # save case to DB
    uid = users(user=user).id
    desc = "merge " + rtype + " cases " + str(cases)
    db.jobs.insert(uid=uid, app=app, cid=ocid, state='C', description=desc,
                   time_submit=time.asctime(), np=config.np, priority=1)
    db.commit()

    return "merged file written to " + run_dir + "<meta http-equiv='refresh' content='2; url=/jobs'>"

@post('/jobs/delete_selected_cases')
def delete_jobs():
    user = authorized()
    selected_cases = request.forms.selected_cases
    cases = selected_cases.rstrip(':').split(':')
    # in case someone selected elements twice, get unique cases
    cases = list(set(cases))
    for jid in cases:
        cid = jobs(id=jid).cid
        app = jobs(id=jid).app
        path = os.path.join(user_dir, user, app, cid)
        if cid is not None:
            print "removing path:", path
            if os.path.isdir(path): shutil.rmtree(path)
            sched.stop(jid)
            sched.qdel(jid)
        else:
            print "ERROR: not removing path:", path, "because cid missing"
    redirect("/jobs")

@post('/jobs/stop')
def stop_job():
    user = authorized()
    app = request.forms.app
    cid = request.forms.cid
    jid = request.forms.jid

    if re.search("/", cid):
        return template("error", err="only possible to stop cases that you own")

    sched.stop(jid)
    time.sleep(0.1)
    jobs(jid).update_record(state="X")
    db.commit()
    redirect("/case?app="+app+"&cid="+cid+"&jid="+jid)

@get('/login')
@get('/login/<referrer>')
def get_login(referrer=''):
    try:
        return template('login', {'referrer': referrer,
                                  'oauth_client_id': config.oauth_client_id})
    except:
        return template('login', {'referrer': referrer})

@get('/logout')
def logout():
    s = request.environ.get('beaker.session')
    s.delete()
    try:
        return template('logout',  {'oauth_client_id': config.oauth_client_id})
    except:
        redirect('/login')

@get('/static/<filepath:path>')
def server_static(filepath):
    return static_file(filepath, root='static')

@get('/user_data/<filepath:path>')
def user_data(filepath):
    user = authorized()
    return static_file(filepath, root='user_data')

@get('/theme')
def get_theme():
    user = authorized()
    uid = users(user=user).id
    return user_meta(uid=uid).theme

@post('/theme')
def save_theme():
    user = authorized()
    uid = users(user=user).id
    u = user_meta(uid=uid)
    print "saving theme:", request.forms.theme
    user_meta.update_or_insert(user_meta.uid==uid, uid=uid, theme=request.forms.theme)
    db.commit()

@get('/download/<filepath:path>')
def download(filepath):
    user = authorized()
    return static_file(filepath, root='download', download=filepath)

@get('/favicon.ico')
def get_favicon():
    return static_file('favicon.ico', root='static')

@post('/login')
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
            user = s[USER_ID_SESSION_KEY] = row.user.lower()
        else:
            return err
    except:
        exc_type, exc_value, exc_traceback = sys.exc_info()
        print traceback.print_exception(exc_type, exc_value, exc_traceback)
        return err
    # if referred to login from another page redirect to referring page
    referrer = request.forms.referrer
    if referrer: redirect('/'+referrer)
    else: redirect('/myapps')

@post('/tokensignin')
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

@post('/account/change_password')
def change_password():
    # this is basically the same coding as the register function
    # needs to be DRY'ed out in the future
    user = authorized()
    if config.auth and not authorized(): redirect('/login')
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
    params['status'] = "password changed"
    return template('account', params)

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

@get('/register')
def get_register():
    return template('register')

@post('/register')
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
    cmd = request.forms.command
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
                      preprocess=preprocess, postprocess=postprocess, command=cmd, assets=assets)
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

@get('/files')
def list_files():
    import glob
    user = authorized()
    cid = request.query.cid
    app = request.query.app
    path = request.query.path

    params = dict()
    params['cid'] = cid
    params['app'] = app
    params['user'] = user

    q = request.query.q
    if "." not in q or q == "*.*": q = ""

    if re.search("/", cid):
        owner, cid = cid.split("/")
    else:
        owner = user
    if not path:
        path = os.path.join(user_dir, owner, app, cid)

    params['path'] = path
    if q:
        _, ext = q.split('.')
        params['files'] = sorted([ fn for fn in os.listdir(path) if fn.endswith(ext) ])
    else:
        q = ""
        params['files'] = sorted(os.listdir(path))
    params['q'] = q

    num_files = len(params['files'])
    params['status'] = "listing " + str(num_files) + " files"
    params['description'] = jobs(cid=cid).description

    return template('files', params)

@post('/files/delete_selected')
def delete_f():
    user = authorized()
    app = request.forms.app
    cid = request.forms.cid
    selected_files = request.forms.selected_files
    files = selected_files.rstrip(':').split(':')
    for file in files:
        path = os.path.join(user_dir, user, app, cid, file)
        if cid is not None:
            if os.path.isfile(path):
                print "removing file:", path
                os.remove(path)
            elif os.path.isdir(path):
                print "removing path:", path
                shutil.rmtree(path)
        else:
            print "ERROR: not removing path:", path, "because cid missing"
    redirect("/files?cid="+cid+"&app="+app)

@post('/files/modify/<operation>')
def modify_selected_files(operation):
    user = authorized()
    app = request.forms.app
    cid = request.forms.cid
    factor = request.forms.factor or 1.0
    factor = float(factor)
    columns = request.forms.columns or 1
    cols = list(map(int, columns.split(':')))

    import operator
    ops = {'add': operator.add, 'sub': operator.sub,
           'mul': operator.mul, 'div': operator.div}
    op = ops[operation]

    selected_files = request.forms.selected_files_mod
    files = selected_files.rstrip(':').split(':')

    for file in files:
        print file
        path = os.path.join(user_dir, user, app, cid, file)

        out = list()
        with open(path, "r") as infile:
            # Loop over lines in each file
            for line in infile:
                line = str(line)
                # Skip comment lines
                if not re.search('^#', line):
                    items = line.split()
                    if len(items) > 0:
                        # execute operation on user-specified columns
                        for col in cols:
                            items[col-1] = str(op(float(items[col-1]), factor))
                    out.append('\t'.join(items)+'\n')
                else:
                    out.append(line)

        with open(path, "w") as outfile:
            outfile.writelines(out)
            outfile.write("# modifications to file: cols = " + str(cols) + ", operation = " + operation + ", factor = " + str(factor) + "\n")

    redirect("/files?cid="+cid+"&app="+app)

@post('/files/zip_selected')
def zip_selected_files():
    user = authorized()
    import zipfile
    app = request.forms.app
    cid = request.forms.cid

    selected_files = request.forms.selected_files_zip
    files = selected_files.rstrip(':').split(':')

    for file in files:
        path = os.path.join(user_dir, user, app, cid, file)
        print "attempting to zip:", path
        zf = zipfile.ZipFile(path+".zip", mode='w', compression=zipfile.ZIP_DEFLATED)
        zf.write(path)
        zf.close()
        # remove the original file if the zipfile now exists
        if os.path.isfile(path+".zip"): os.remove(path)

    redirect("/files?cid="+cid+"&app="+app)

@get('/plots/edit')
def editplotdefs():
    user = authorized()
    if user != 'admin':
        return template('error', err="must be admin to edit plots")
    app = request.query.app
    if config.auth and not authorized(): redirect('/login')
    if app not in myapps: redirect('/apps')
    query = (apps.id==plots.appid) & (apps.name==app)
    result = db(query).select()
    params = { 'app': app, 'user': user }
    return template('plots/plotdefs', params, rows=result)

@get('/plots/edit/<pltid>')
def editplotdef(pltid):
    user = authorized()
    app = request.forms.app
    result = db(plots.id==pltid).select().first()
    params = { 'app': app, 'user': user }
    return template('plots/edit_plot', params, row=result)

@post('/plots/edit/<pltid>')
def editplot(pltid):
    user = authorized()
    app = request.forms.app
    title = request.forms.title
    ptype = request.forms.ptype
    options = request.forms.options
    print "updating plot ", pltid, "for app", app
    plots(pltid).update_record(title=title, ptype=ptype, options=options)
    db.commit()
    redirect('/plots/edit?app='+app)


@get('/plots/delete/<pltid>')
def delete_plot(pltid):
    user = authorized()
    app = request.query.app
    del db.plots[pltid]
    db.commit()
    redirect ('/plots/edit?app='+app)

@get('/plots/<pltid>/datasources')
def get_datasource(pltid):
    """get list of datasources for given plot"""
    user = authorized()
    app = request.query.app
    cid = request.query.cid
    if myapps[app].appname not in myapps: redirect('/apps')
    if config.auth and not authorized(): redirect('/login')
    result = db(datasource.pltid==pltid).select()
    title = plots(pltid).title
    params = { 'app': app, 'cid': cid, 'user': user, 'pltid': pltid, 'rows': result, 'title': title}
    return template('plots/datasources', params, rows=result)

@post('/plots/<pltid>/datasources')
def add_datasource(pltid):
    """create a new datasource for given plot"""
    user = authorized()
    app = request.forms.app
    r = request.forms
    datasource.insert(pltid=pltid, label=r['label'],  filename=r['fn'], cols=r['cols'],
                      line_range=r['line_range'], data_def=r['data_def'])
    db.commit()
    redirect ('/plots/' + str(pltid) + '/datasources?app='+app)

@get('/plots/<pltid>/datasources/<dsid>')
def edit_datasource(pltid, dsid):
    """create a new datasource for given plot"""
    user = authorized()
    app = request.query.app
    query = (datasource.id==dsid)
    result = db(query).select().first()
    params = {'app': app, 'pltid': pltid, 'dsid': dsid}
    return template('plots/edit_datasource', params, row=result)

@post('/plots/<pltid>/datasources/<dsid>')
def edit_datasource_post(pltid, dsid):
    """update datasource for given plot"""
    user = authorized()
    app = request.forms.get('app')
    r = request.forms
    datasource(id=dsid).update_record(label=r['label'], pltid=pltid, filename=r['fn'], cols=r['cols'],
                                      line_range=r['line_range'], data_def=r['data_def'])
    db.commit()
    redirect ('/plots/' + str(pltid) + '/datasources?app='+app)
    params = {'app': app, 'pltid': pltid, 'dsid': dsid}
    return template('plots/edit_datasource', params)

@post('/plots/datasource_delete')
def delete_plot():
    user = authorized()
    app = request.forms.get('app')
    pltid = request.forms.get('pltid')
    dsid = request.forms.get('dsid')
    del db.datasource[dsid]
    db.commit()
    redirect ('/plots/' + str(pltid) + '/datasources?app='+app)

@post('/plots/create')
def create_plot():
    user = authorized()
    app = request.forms.get('app')
    r = request
    plots.insert(appid=myapps[app].appid, ptype=r.forms['ptype'],
                 title=r.forms['title'], options=r.forms['options'])
    db.commit()
    redirect ('/plots/edit?app='+app)

@get('/plot/<pltid>')
def plot_interface(pltid):
    user = authorized()
    app = request.query.app
    cid = request.query.cid
    jid = request.query.jid
    params = dict()

    if not cid:
        params['err'] = "No case id specified. First select a case id from the list of jobs."
        return template('error', params)

    if re.search("/", cid):
        (owner, c) = cid.split("/")
    else:
        owner = user
        c = cid

    inputs, _, _ = myapps[app].read_params(owner, c)
    sim_dir = os.path.join(user_dir, owner, app, c)

    # use pltid of 0 to trigger finding the first pltid for the current app
    if int(pltid) == 0:
        query = (apps.id==plots.appid) & (apps.name==app)
        result = db(query).select().first()
        if result: pltid = result['plots']['id']

    p = plotmod.Plot()

    # get the data for the pltid given
    try:
        result = db(plots.id==pltid).select().first()
        plottype = result['ptype']
        if result['options']:
            options = replace_tags(result['options'], inputs)
        else:
            options = ''
        plot_title = result['title']
    except:
        exc_type, exc_value, exc_traceback = sys.exc_info()
        print traceback.print_exception(exc_type, exc_value, exc_traceback)
        redirect ('/plots/edit?app='+app+'&cid='+cid)

    # if plot not in DB return error
    if plottype is None:
        params = { 'cid': cid, 'app': app, 'user': user }
        params['err'] = "Sorry! This app does not support plotting capability"
        return template('error', params)

    # determine which view template to use
    if plottype == 'flot-cat':
        tfn = 'plots/flot-cat'
    elif plottype == 'flot-scatter':
        tfn = 'plots/flot-scatter'
    elif plottype == 'flot-scatter-animated':
        tfn = 'plots/flot-scatter-animated'    # for backwards compatability
    elif plottype == 'flot-line':
        tfn = 'plots/flot-scatter'
    elif plottype == 'plotly-hist':
        tfn = 'plots/plotly-hist'
    elif plottype == 'mpl-line' or plottype == 'mpl-bar':
        redirect('/mpl/'+pltid+'?app='+app+'&cid='+cid)
    elif plottype == 'handson':
        tfn = 'plots/handson'
    else:
        return template("error", err="plot type not supported: " + plottype)

    # get list of all plots for this app
    query = (apps.id==plots.appid) & (apps.name==app)
    list_of_plots = db(query).select()

    # extract data from files
    data = []
    ticks = []
    plotpath = ''
    result = db(datasource.pltid==pltid).select()

    datadef = ""
    for r in result:
        plotfn = r['filename']

        # in addition to supporting input params, also support case id
        if "cid" not in inputs: inputs["cid"] = c

        # replace <cid>.dat with xyz123.dat
        plotfn = replace_tags(plotfn, inputs)
        plotpath = os.path.join(sim_dir, plotfn)

        # handle CSV data
        _, file_extension = os.path.splitext(plotfn)
        if file_extension == '.csv':
            data = p.get_csv_data(plotpath)
            stats = ''

        # handle X, Y columnar data
        else:
            cols = r['cols']
            line_range = r['line_range']
            try:
                datadef += r['data_def'] + ", "
            except:
                exc_type, exc_value, exc_traceback = sys.exc_info()
                print traceback.print_exception(exc_type, exc_value, exc_traceback)
                datadef = ""

            if cols.find(":") > 0: # two columns
                num_fields = 2
                (col1str, col2str) = cols.split(":")
                col1 = int(col1str); col2 = int(col2str)
            else: # single column
                num_fields = 1
                col1 = int(cols)

            # do some postprocessing
            if line_range is not None:
                # to prevent breaking current spc apps, still support
                # expressions like 1:1000, but in the future this should
                # be changed to a range 1-1000.  Therefore, using : is deprecated
                # and will be removed in the future.
                (line1str, line2str) = re.split("[-:]", line_range)
                line1 = int(line1str)
                ## there is a problem with the following statement
                ## shows up in mendel app
                # if myapps[app].postprocess > 0:
                #    dat = process.postprocess(plotpath, line1, line2)
                # else:
                try: # if line2 is specified
                    line2 = int(line2str)
                    dat = p.get_data(plotpath, col1, col2, line1, line2)
                except: # if line2 not specified
                    exc_type, exc_value, exc_traceback = sys.exc_info()
                    print traceback.print_exception(exc_type, exc_value, exc_traceback)
                    if num_fields == 2:
                        dat = p.get_data(plotpath, col1, col2, line1)
                    else: # single column of data
                        dat = p.get_data(plotpath, col1)
                # remove this app-specific code in future
                if app == "fpg":
                    dat = process.postprocess(plotpath, line1, line2)
            else:
                dat = p.get_data(plotpath, col1, col2)

            if dat == -1:
                stats = "ERROR: Could not read data file"
            elif dat == -2:
                stats = "ERROR: file exists, but problem parsing data. Are column and line ranges setup properly? Is all the data there?"
            else:
                stats = compute_stats(plotpath)
            # [[1,2,3]] >>> [1,2,3]

            # clean data
            #dat = [d.replace('?', '0') for d in dat]
            data.append(dat)

            if num_fields == 1: data = data[0]

            if plottype == 'flot-cat':
                ticks = p.get_ticks(plotpath, col1, col2)

    desc = jobs(cid=c).description

    params = { 'cid': cid, 'pltid': pltid,
               'data': data, 'app': app, 'user': user, 'owner': owner,
               'ticks': ticks, 'plot_title': plot_title, 'plotpath': plotpath,
               'rows': list_of_plots, 'options': options, 'datadef': datadef,
               'stats': stats, 'description': desc }

    if jid: params['jid'] = jid

    return template(tfn, params)

@get('/mpl/<pltid>')
def matplotlib(pltid):
    """Generate a random image using Matplotlib and display it"""
    # in the future create a private function __import__ to import third-party
    # libraries, so that it can respond gracefully.  See for example the
    # Examples section at https://docs.python.org/2/library/imp.html
    user = authorized()
    from pylab import savefig
    import StringIO
    from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
    from matplotlib.figure import Figure
    app = request.query.app
    cid = request.query.cid

    fig = Figure()
    fig.set_tight_layout(True)
    ax = fig.add_subplot(111)

    # get info about plot from db
    p = plotmod.Plot()
    result = db(plots.id==pltid).select().first()
    plot_title = result['title']
    plottype = result['ptype']
    options = result['options']

    # parse plot options to extract and set x- and y-axis labels
    m = re.search("xaxis:\s*{(.*)}", options)
    if m:
        n = re.search("axisLabel:\s*\"(\w*)\"", m.group(1))
        if n: ax.set_xlabel(n.group(1))

    m = re.search("yaxis:\s*{(.*)}", options)
    if m:
        n = re.search("axisLabel:\s*\"(\w*)\"", m.group(1))
        if n: ax.set_ylabel(n.group(1))

    # get info about data source
    # fix in the future to handle multiple data sources
    result = db(datasource.pltid==pltid).select()
    for r in result:
        plotfn = r['filename']
        cols = r['cols']
        line_range = r['line_range']
        (col1str, col2str) = cols.split(":")
        col1 = int(col1str)
        col2 = int(col2str)
        if line_range is not None:
            # to prevent breaking current spc apps, still support
            # expressions like 1:1000, but in the future this should
            # be changed to a range 1-1000.  Therefore, using : is deprecated
            # and will be removed in the future.
            (line1str, line2str) = re.split("[-:]", line_range)
            line1 = int(line1str)
            line2 = int(line2str)

    plotfn = re.sub(r"<cid>", cid, plotfn)
    sim_dir = os.path.join(user_dir, user, app, cid)
    plotpath = os.path.join(sim_dir, plotfn)
    xx = p.get_column_of_data(plotpath, col1)
    yy = p.get_column_of_data(plotpath, col2)
    # convert elements from strings to floats
    xx = [float(i) for i in xx]
    yy = [float(i) for i in yy]

    # plot
    if plottype == 'mpl-line':
        ax.plot(xx, yy)
    elif plottype == 'mpl-bar':
        ax.bar(xx, yy)
    else:
        return "ERROR: plottype not supported"
    canvas = FigureCanvas(fig)
    png_output = StringIO.StringIO()
    canvas.print_png(png_output)

    # save file
    tmp_dir = "static/tmp"
    if not os.path.exists(tmp_dir):
        os.makedirs(tmp_dir)
    fn = plot_title+'.png'
    fig.set_size_inches(7, 4)
    img_path = os.path.join(sim_dir, fn)
    fig.savefig(img_path)

    # get list of all plots for this app
    query = (apps.id==plots.appid) & (apps.name==app)
    list_of_plots = db(query).select()
    stats = compute_stats(plotpath)

    params = {'image': fn, 'app': app, 'cid': cid, 'pltid': pltid,
              'plotpath': plotpath, 'img_path': img_path, 'plot_title': plot_title,
              'rows': list_of_plots, 'stats': stats }
    return template('plots/matplotlib', params)

@get('/zipcase')
def zip_case():
    """zip case on machine to prepare for download"""
    user = authorized()
    import zipfile
    app = request.query.app
    cid = request.query.cid

    base_dir = os.path.join(user_dir, user, app)
    path = os.path.join(base_dir, cid+".zip")
    zf = zipfile.ZipFile(path, mode='w', compression=zipfile.ZIP_DEFLATED)
    sim_dir = os.path.join(base_dir, cid)
    for fn in os.listdir(sim_dir):
        zf.write(os.path.join(sim_dir, fn))
    zf.close()

    return static_file(path, root="./")
    # status = "case compressed"
    # redirect(request.headers.get('Referer')+"&status="+status)

@get('/zipget')
def zipget():
    """get zipfile from another machine, save to current machine"""
    import zipfile
    user = authorized()
    cid = request.query.cid
    app = request.query.app
    try:
        worker = config.remote_worker_url
    except:
        exc_type, exc_value, exc_traceback = sys.exc_info()
        print traceback.print_exception(exc_type, exc_value, exc_traceback)
        worker = request.query.url

    # if config.worker != "remote" or config.remote_worker_url is None:
    if worker is None:
        params = { 'app': app,
                   'err': "worker and remote_worker_url parameters must be set " +
                          " in config.py for this feature to work" }
        return template('error', params)

    # try:
    requests.get(worker + "/zipcase",
         params={'app': app, 'cid': cid, 'user': user})

    path = os.path.join(user_dir, user, app, cid)
    file_path = path+".zip"
    url = os.path.join(worker, file_path)

    print "url is:", url
    if not os.path.exists(path):
        os.makedirs(path)

    print "downloading " + url
    fh, _ = urllib.urlretrieve(url)
    z = zipfile.ZipFile(fh, 'r', compression=zipfile.ZIP_DEFLATED)
    z.extractall()

    # add case to database
    uid = users(user=user).id
    jid = db.jobs.insert(uid=uid, app=app, cid=cid, state="REMOTE",
                          description="", time_submit=time.asctime(),
                          walltime="", np="", priority="")
    db.commit()

    # status = "file_downloaded"
    # redirect(request.headers.get('Referer')) #+ "&status=" + status)
    redirect("/jobs")

    # except:
    #     params = { 'app': app, 'err': "Configuration not setup with remote worker." }
    #     return template('error', params)


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

@post('/upload')
def upload_file():
    user = authorized()
    upload = request.files.upload
    if not upload:
        return template('error', err="no file selected.")
    #name, ext = os.path.splitext(upload.filename)
    #if ext not in ('.zip','.txt'):
    #    return template('error', err="file extension not allowed")
    #try:
    save_path_dir = os.path.join(user_dir, user, upload_dir)
    if not os.path.exists(save_path_dir): os.makedirs(save_path_dir)
    save_path = os.path.join(save_path_dir, upload.filename)
    if os.path.isfile(save_path):
        return template('error', err="file exists")
    upload.save(save_path)
    return "SUCCESS"
    #except:
    #    return "FAILED"

@post('/upload_data')
def upload_data():
    user = authorized()
    save_path_dir = os.path.join(user_dir, user, upload_dir)
    if not os.path.exists(save_path_dir): os.makedirs(save_path_dir)
    filename = request.forms.filename
    # print "filename:", filename
    if not filename: return template('error', err="file not specified")
    save_path = os.path.join(save_path_dir, filename)
    # print "save_path:", save_path
    # if os.path.isfile(save_path): return template('error', err="file exists")
    upload_data = request.forms.upload_data
    with open(save_path, 'w') as f: f.write(upload_data)

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

    # attempt to mix in docker functionality
    try:
        dockermod.bind(globals())
        app.app.merge(dockermod.dockerMod)
    except Exception, e:
        pass

    # run the app
    try:
        run(server=config.server, app=app, host='0.0.0.0', \
            port=config.port, debug=False)
    except:
        run(app=app, host='0.0.0.0', port=config.port, debug=False)
