#!/usr/bin/env python

# web framework
from bottle import *
# python built-ins
import uuid, hashlib, shutil, string
import random, subprocess, sys, os, re
import cgi, urllib2, json, smtplib, time
# other local modules
import config, uploads, process
import scheduler, scheduler_mp
import apps as appmod
import plots as plotmod
try:
    import aws as awsmod
except ImportError:
    pass
try:
    import container as dockermod
except ImportError:
    pass
# data access layer
from gluino import DAL, Field
from model import *

### session management configuration ###
from beaker.middleware import SessionMiddleware
USER_ID_SESSION_KEY = 'user_id'
APP_SESSION_KEY = 'app'

session_opts = {
    'session.type': 'file',
    'session.cookie_expires': True, # delete cookies when browser closed
    'session.data_dir': config.user_dir,
    'session.auto': True
}

app = SessionMiddleware(app(), session_opts)
### end session management configuration ###

# create instance of scheduler
if config.sched == "mp":
    sched = scheduler_mp.scheduler()
else:
    sched = scheduler.scheduler()

pbuffer = ''

@post('/confirm')
def confirm_form():
    global user
    check_user_var()
    app = request.forms.app
    # force the first string to be a letter so that the case id
    # will be guaranteed to be a string
    cid = random.choice(string.ascii_lowercase) + str(uuid.uuid4())[:5]
    # pass the case_id to be used by the program input parameters,
    # if case_id is defined in the input deck it will be used
    # otherwise it is ignored
    request.forms['case_id'] = cid
    try:
        desc = request.forms['desc']
    except:
        desc = "None"
    myapps[app].write_params(request.forms,user)
    # read the file
    run_dir = os.path.join(myapps[app].user_dir,user,myapps[app].appname,cid)
    fn = os.path.join(run_dir,myapps[app].simfn)
    inputs = slurp_file(fn)
    # convert html tags to entities (e.g. < to &lt;)
    inputs = cgi.escape(inputs)
    params = { 'cid': cid, 'inputs': inputs, 'app': app,
               'user': user, 'apps': myapps.keys(), 'np': config.np,
               'desc': desc }
    try:
        return template('confirm', params)
    except:
        return 'ERROR: failed to write parameters to file'

@get('/test')
def test():
    return template('websocket')

@post('/execute')
def execute():
    global user
    check_user_var()
    app = request.forms.app
    cid = request.forms.cid
    np = request.forms.np
    desc = request.forms.desc
    #priority = request.forms.priority
    params = {}
    base_dir = os.path.join(myapps[app].user_dir,user,app,cid)

    # if preprocess is set run the preprocessor
    try:
        if myapps[app].preprocess:
            run_params,_,_ = myapps[app].read_params(user,cid)
            processed_inputs = process.preprocess(run_params,
                                       myapps[app].preprocess,base_dir)
        if myapps[app].preprocess == "terra.in":
            myapps[app].outfn = "out"+run_params['casenum']+".00"
    except:
        return template('error',err="There was an error with the preprocessor")

    # submit job to queue
    try:
        params['cid'] = cid
        params['app'] = app
        params['user'] = user
        priority = db(users.user==user).select(users.priority).first().priority
        jid = sched.qsub(app,cid,user,np,priority,desc)
        redirect("/case?app="+app+"&cid="+cid+"&jid="+jid)
    except OSError, e:
        print >>sys.stderr, "Execution failed:", e
        params = { 'cid': cid, 'output': pbuffer, 'app': app, 'user': user,
                   'err': e, 'apps': myapps.keys() }
        return template('error',params)

@get('/more')
def more():
    """given a form with the attribute plotpath,
       output the file to the browser"""
    global user
    app = request.query.app
    cid = request.query.cid
    filepath = request.query.filepath
    contents = slurp_file(filepath)
    # convert html tags to entities (e.g. < to &lt;)
    contents = cgi.escape(contents)
    params = { 'cid': cid, 'contents': contents, 'app': app, 'user': user,
               'fn': filepath, 'apps': myapps.keys() }
    return template('more', params)

@get('/case')
def case():
    if config.auth and not authorized(): redirect('/login')
    global user
    check_user_var()
    app = request.query.app
    cid = request.query.cid
    jid = request.query.jid or -1
    try:
        if re.search("/",cid):
            (u,c) = cid.split("/")
            sid = request.query.sid # id of item in shared
            run_dir = os.path.join(myapps[app].user_dir,u,myapps[app].appname,c)
            fn = os.path.join(run_dir,myapps[app].outfn)
            output = slurp_file(fn)
            params = { 'cid': cid, 'contents': output, 'app': app, 'jid': jid,
                       'sid': sid, 'user': u, 'fn': fn, 'apps': myapps.keys() }
            return template('case_public', params)
        else:
            u = user
            c = cid
            run_dir = os.path.join(myapps[app].user_dir,u,myapps[app].appname,c)
            fn = os.path.join(run_dir,myapps[app].outfn)
            output = slurp_file(fn)
            # result = db(jobs.id==jid).select().first()
            result = db(jobs.cid==cid).select().first()
            desc = result['description']
            shared = result['shared']
            params = { 'cid': cid, 'contents': output, 'app': app, 'jid': jid,
                       'user': u, 'fn': fn, 'apps': myapps.keys(),
                       'description': desc, 'shared': shared }
            return template('case', params)
    except:
        params = { 'app': app, 'apps': myapps.keys(),
                   'err': "There was a problem... Sorry!" }
        return template('error', params)

@get('/output')
def output():
    if config.auth and not authorized(): redirect('/login')
    global user
    app = request.query.app
    cid = request.query.cid
    check_user_var()
    try:
        if re.search("/",cid):
            (u,c) = cid.split("/")
        else:
            u = user
            c = cid
        run_dir = os.path.join(myapps[app].user_dir,u,myapps[app].appname,c)
        fn = os.path.join(run_dir,myapps[app].outfn)
        output = slurp_file(fn)
        # the following line will convert HTML chars like > to entities &gt;
        # this is needed so that XML input files will show paramters labels
        output = cgi.escape(output)
        params = { 'cid': cid, 'contents': output, 'app': app,
                   'user': u, 'fn': fn, 'apps': myapps.keys() }
        return template('more', params)
    except:
        params = { 'app': app, 'apps': myapps.keys(),
                   'err': "Couldn't read input file. Check casename." }
        return template('error', params)

@get('/inputs')
def inputs():
    if config.auth and not authorized(): redirect('/login')
    global user
    app = request.query.app
    cid = request.query.cid
    check_user_var()
    try:
        if re.search("/",cid):
            (u,c) = cid.split("/")
        else:
            u = user
            c = cid
        run_dir = os.path.join(myapps[app].user_dir,u,myapps[app].appname,c)
        fn = os.path.join(run_dir,myapps[app].simfn)
        inputs = slurp_file(fn)
        # the following line will convert HTML chars like > to entities &gt;
        # this is needed so that XML input files will show paramters labels
        inputs = cgi.escape(inputs)

        params = { 'cid': cid, 'contents': inputs, 'app': app, 'user': u,
                   'fn': fn, 'apps': myapps.keys() }
        return template('more', params)
    except:
        params = { 'app': app, 'apps': myapps.keys(),
                   'err': "Couldn't read input file. Check casename." }
        return template('error', params)

def slurp_file(path):
    """read file given by path and return the contents of the file
       as a single string datatype"""
    try:
        with open(path,'r') as f:
            data = f.read()
        return data
    except IOError:
        return("ERROR: the file cannot be opened or does not exist " + path)

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
        # this is a temporary hack for mendel
        if path[-3:] == "hst":
            xoutput += output[len(output)-1]
    return xoutput

@get('/<app>/<cid>/tail')
def tail(app,cid):
    global user
    check_user_var()
    # submit num_lines as form parameter
    # num_lines = int(request.query.num_lines)
    # if not num_lines or num_lines < 10:
    #     num_lines = 24
    num_lines = config.tail_num_lines
    progress = 0
    complete = 0
    run_dir = os.path.join(myapps[app].user_dir,user,myapps[app].appname,cid)
    ofn = os.path.join(run_dir,myapps[app].outfn)
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
        myoutput = output[len(output)-num_lines:]
        xoutput = ''.join(myoutput)
        f.close()
    else:
        xoutput = 'waiting to start...'
    params = { 'cid': cid, 'contents': xoutput, 'app': app,
               'user': user, 'fn': ofn, 'apps': myapps.keys(),
               'progress': progress }
    return template('more_contents', params)

@get('/')
def root():
    if config.auth and not authorized(): redirect('/login')
    #return template('overview')
    redirect('/apps')

@get('/jobs')
def show_jobs():
    if config.auth and not authorized(): redirect('/login')
    #if app not in myapps: redirect('/apps')
    global user
    cid = request.query.cid
    app = request.query.app
    n = int(request.query.n or config.jobs_num_rows)
    q = request.query.q
    starred = request.query.starred
    shared = request.query.shared
    check_user_var()
    if starred:
        result = db(jobs.user==user and jobs.starred=="True").select(orderby=~jobs.id)[:n]
    elif shared:
        result = db(jobs.user==user and jobs.shared=="True").select(orderby=~jobs.id)[:n]
    elif q:
        result = db(jobs.user==user and \
            db.jobs.description.contains(q, case_sensitive=False)).select(orderby=~jobs.id)        
    else:
        result = db(jobs.user==user).select(orderby=~jobs.id)[:n]
    params = {}
    params['cid'] = cid
    params['app'] = app
    params['user'] = user
    params['apps'] = myapps.keys()
    params['sched'] = config.sched
    params['np'] = config.np
    params['n'] = n
    params['num_rows'] = config.jobs_num_rows
    return template('jobs', params, rows=result)

@get('/aws')
def get_aws():
    if config.auth and not authorized(): redirect('/login')
    #if app not in myapps: redirect('/apps')
    global user
    cid = request.query.cid
    app = request.query.app
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
    params['apps'] = myapps.keys()
    if request.query.status:
        params['status'] = request.query.status
    return template('aws',params,creds=creds,instances=instances)

@post('/aws/creds')
def post_aws_creds():
    if config.auth and not authorized(): redirect('/login')
    check_user_var()
    global user
    a = request.forms.account_id
    s = request.forms.secret
    k = request.forms.key
    uid = users(user=user).id
    db.aws_creds.insert(account_id=a,secret=s,key=k,uid=uid)
    db.commit()
    redirect('/aws')

@post('/aws/instance')
def post_instance():
    if config.auth and not authorized(): redirect('/login')
    global user
    check_user_var()
    i = request.forms.instance
    t = request.forms.itype
    r = request.forms.region
    uid = users(user=user).id
    db.aws_instances.insert(instance=i,itype=t,region=r,uid=uid)
    db.commit()
    redirect('/aws')

@post('/aws/cred/delete')
def aws_cred_del():
    id = request.forms.id
    del db.aws_creds[id]
    db.commit()
    redirect('/aws')

def aws_conn(id):
    """create a connection to the EC2 machine and return the handle"""
    global user
    check_user_var()
    uid = users(user=user).id
    creds = db(db.aws_creds.uid==uid).select().first()
    account_id = creds['account_id']
    secret = creds['secret']
    key = creds['key']
    instances = db(db.aws_instances.id==id).select().first()
    instance = instances['instance']
    region = instances['region']
    rate = instances['rate'] or 0.
    return awsmod.ec2(key,secret,account_id,instance,region,rate)

@get('/aws/status/<aid>')
def aws_status(aid):
    if config.auth and not authorized(): redirect('/login')
    global user
    check_user_var()
    cid = request.query.cid
    app = request.query.app
    params = {}
    params['aid'] = aid
    params['cid'] = cid
    params['app'] = app
    params['user'] = user
    params['apps'] = myapps.keys()
    if awsmod:
        a = aws_conn(aid)
    else:
        return template('error',err="To use this feature, you need to install the Python boto libs see <a href=\"https://pypi.python.org/pypi/boto/\">https://pypi.python.org/pypi/boto/</a>")
    try:
        astatus = a.status()
        astatus['uptime'] = a.uptime(astatus['launch_time'])
        astatus['charge since last boot'] = a.charge(astatus['uptime'])
        return template('aws_status',params,astatus=astatus)
    except:
        return template('error',err="There was a problem connecting to the AWS machine. Check the credentials and make sure the machine is running.")

@get('/aws/start/<aid>')
def aws_start(aid):
    if config.auth and not authorized(): redirect('/login')
    global user
    check_user_var()
    cid = request.query.cid
    app = request.query.app
    params = {}
    params['aid'] = aid
    params['cid'] = cid
    params['app'] = app
    params['user'] = user
    params['apps'] = myapps.keys()
    if awsmod:
        a = aws_conn(aid)
    else:
        return template('error',err="To use this feature, you need to install the Python boto libs see <a href=\"https://pypi.python.org/pypi/boto/\">https://pypi.python.org/pypi/boto/</a>")
    a.start()
    # takes a few seconds for the status to change on the Amazon end
    time.sleep(5) 
    astatus = a.status()
    return template('aws_status',params,astatus=astatus)

@get('/aws/stop/<aid>')
def aws_stop(aid):
    if config.auth and not authorized(): redirect('/login')
    global user
    check_user_var()
    cid = request.query.cid
    app = request.query.app
    params = {}
    params['aid'] = aid
    params['cid'] = cid
    params['app'] = app
    params['user'] = user
    params['apps'] = myapps.keys()
    a = aws_conn(aid)
    a.stop()
    # takes a few seconds for the status to change on the Amazon end
    time.sleep(5) 
    return template('aws_status',params,astatus=a.status())

@get('/account')
def get_account():
    if config.auth and not authorized(): redirect('/login')
    global user
    check_user_var()
    app = request.query.app
    params = {}
    params['app'] = app
    params['user'] = user
    params['apps'] = myapps.keys()
    uid = users(user=user).id
    return template('account',params)

@post('/jobs/annotate')
def annotate_job():
    if config.auth and not authorized(): redirect('/login')
    check_user_var()
    app = request.forms.app
    cid = request.forms.cid
    jid = request.forms.jid
    desc = request.forms.description
    jobs(id=jid).update_record(description=desc)
    db.commit()
    redirect('/jobs')

@post('/jobs/star')
def star_case():
    jid = request.forms.jid
    jobs(id=jid).update_record(starred="True")
    db.commit()
    redirect('/jobs')

@post('/jobs/unstar')
def unstar_case():
    jid = request.forms.jid
    jobs(id=jid).update_record(starred="False")
    db.commit()
    redirect('/jobs')

@post('/jobs/share')
def share_case():
    if config.auth and not authorized(): redirect('/login')
    check_user_var()
    app = request.forms.app
    cid = request.forms.cid
    jid = request.forms.jid
    jobs(id=jid).update_record(shared="True")
    db.commit()
    redirect('/jobs')

@post('/jobs/unshare')
def unshare_case():
    if config.auth and not authorized(): redirect('/login')
    check_user_var()
    app = request.forms.app
    cid = request.forms.cid
    jid = request.forms.jid
    jobs(id=jid).update_record(shared="False")
    db.commit()
    redirect('/jobs')

@get('/jobs/shared')
def get_shared():
    """Return the records from the shared table."""
    if config.auth and not authorized(): redirect('/login')
    global user
    cid = request.query.cid
    app = request.query.app
    n = request.query.n
    if not n: 
        n = config.jobs_num_rows
    else:
        n = int(n)
    # sort by descending order of jobs.id
    result = db(jobs.shared=="True").select(orderby=~jobs.id)[:n]
    params = {}
    params['cid'] = cid
    params['app'] = app
    params['user'] = user
    params['apps'] = myapps.keys()
    params['n'] = n
    params['num_rows'] = config.jobs_num_rows
    return template('shared', params, rows=result)

@post('/jobs/delete/<jid>')
def delete_job(jid):
    if config.auth and not authorized(): redirect('/login')
    check_user_var()
    app = request.forms.app
    cid = request.forms.cid
    #try:
    if True:
        # this will fail if the app has been removed 
        path = os.path.join(myapps[app].user_dir,user,app,cid)
        if os.path.isdir(path): shutil.rmtree(path)
        sched.stop()
        sched.qdel(jid)
    #except:
    #    return "there was an error!"
    redirect("/jobs")

@post('/jobs/stop')
def stop_job():
    if config.auth and not authorized(): redirect('/login')
    app = request.forms.app
    cid = request.forms.cid
    jid = request.forms.jid
    sched.stop()
    redirect("/case?app="+app+"&cid="+cid+"&jid="+jid)

@get('/<app>')
def show_app(app):
    if config.auth and not authorized(): redirect('/login')
    check_user_var()
    global user, myapps
    # set a session variable to keep track of the current app
    s = request.environ.get('beaker.session')
    s[APP_SESSION_KEY] = app
    # parameters for return template
    try:
        params = myapps[app].params
        params['cid'] = ''
        params['app'] = app
        params['user'] = user
        params['apps'] = myapps
        return template(os.path.join(config.apps_dir,app), params)
    except:
        redirect('/app/'+app)

@get('/login')
@get('/login/<referrer>')
def get_login(referrer=''):
    return template('login',{'referrer': referrer})

@get('/logout')
def logout():
    s = request.environ.get('beaker.session')
    s.delete()
    redirect('/login')

@get('/static/<filepath:path>')
def server_static(filepath):
    return static_file(filepath, root='static')

@get('/user_data/<filepath:path>')
def server_static(filepath):
    return static_file(filepath, root='user_data')

@get('/favicon.ico')
def get_favicon():
    return static_file('favicon.ico', root='static')
#    return server_static('favicon.ico')

@post('/login')
def post_login():
    global user
    s = request.environ.get('beaker.session')
    user = users(user=request.forms.get('user'))
    pw = request.forms.passwd
    err = "<p>Login failed: wrong username or password</p>"
    # if password matches, set the USER_ID_SESSION_KEY
    hashpw = hashlib.sha256(pw).hexdigest()
    try:
        if hashpw == user.passwd:
            # set global user and session key
            user = s[USER_ID_SESSION_KEY] = user.user
        else:
            return err
    except:
        return err
    # if referred to login from another page redirect to referring page
    referrer = request.forms.referrer
    if referrer: redirect('/'+referrer)
    else: redirect('/apps')

@post('/account/change_password')
def change_password():
    # this is basically the same coding as the register function
    # needs to be DRY'ed out in the future
    global user
    if config.auth and not authorized(): redirect('/login')
    opasswd = request.forms.opasswd
    pw1 = request.forms.npasswd1
    pw2 = request.forms.npasswd2
    # check old passwd
    #user = request.forms.user
    if _check_user_passwd(user,opasswd) and pw1 == pw2 and len(pw1) > 0:
        u = users(user=user)
        u.update_record(passwd=_hash_pass(pw1))
        db.commit()
    else:
        return template('error',err="problem with password")
    params = {}
    params['status'] = "password changed"
    return template('account',params)

def _check_user_passwd(user,passwd):
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
    user = request.forms.user
    pw1 = request.forms.password1
    pw2 = request.forms.password2
    email = request.forms.email
    if pw1 == pw2:
        hashpw = _hash_pass(pw1)
        try:
            config.default_priority
        except:
            config.default_priority = 3
        users.insert(user=user, passwd=hashpw, email=email,
                     priority=config.default_priority)
        db.commit()
        # email admin user
        try:
            server = smtplib.SMTP('localhost')
            message = user + " just registered " + email
            admin_email = db(users.user=="admin").select(users.email).first()
            server.sendmail('admin@scipaas.com', [admin_email], message)
            server.quit()
            redirect('/login')
        except:
            redirect('/login')
    else:
        return template('register')

@get('/admin/show_users')
def admin_show_users():
    global user
    if config.auth and not authorized(): redirect('/login')
    if not user == "admin":
        return template("error",err="must be admin to delete")
    result = db().select(users.ALL)
    params = {'user': user}
    return template('admin/users',params,rows=result)

@post('/admin/delete_user')
def admin_delete_user():
    global user
    if config.auth and not authorized(): redirect('/login')
    if not user == "admin":
        return template("error",err="must be admin to delete")
    uid = request.forms.uid
    print "uid is:",uid
    if int(uid) == 0:
        return template("error",err="can't delete admin user")
    del db.users[uid]
    db.commit()
    redirect("/admin/show_users")

@post('/check_user')
def check_user():
    user = request.forms.user
    """Server-side AJAX function to check if a username exists in the DB."""
    # return booleans as strings here b/c they get parsed by JavaScript
    if users(user=user): return 'true'
    else: return 'false'

@post('/app_exists/<appname>')
def app_exists(appname):
    """Server-side AJAX function to check if an app exists in the DB."""
    appname = request.forms.appname
    # return booleans as strings here b/c they get parsed by JavaScript
    if apps(name=appname): return 'true'
    else: return 'false'

def check_user_var():
    # this check is because user is global var when restarting 
    # user does not exist so return... need to implement better solution
    # such as using a session variable to check for user
    try: user
    except: redirect('/apps')
    return True

@get('/apps')
def showapps():
    global user
    if config.auth and not authorized(): redirect('/login')
    result = db().select(apps.ALL)
    if user == "admin":
        configurable = True
    else:
        configurable = False    
    params = { 'apps': myapps.keys(), 'configurable': configurable }
    return template('apps', params, rows=result)

@get('/apps/load')
def get_load_apps():
    load_apps()
    redirect('/apps')

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
            print 'loading: %s (id: %s)' % (name,appid)
            myapps[name] = app_instance(input_format,name,preprocess,postprocess)
            myapps[name].appid = appid
        except:
            print 'ERROR: LOADING: %s (ID: %s) FAILED TO LOAD' % (name,appid)
    default_app = name # simple soln - use last app read from DB
    return True

@post('/app/edit/<appid>')
def app_edit(appid):
    global user
    if config.auth and not authorized(): redirect('/login')
    if user != 'admin': 
        return template('error',err="must be admin to edit app")
    cid = request.forms.cid
    app = request.forms.app
    result = db(apps.name==app).select().first()
    params = {'app': app, 'cid': cid, 'apps': myapps.keys()}
    return template('app_edit', params, rows=result)

@post('/app/save/<appid>')
def app_save(appid):
    app = request.forms.app
    cmd = request.forms.command
    lang = request.forms.language
    info = request.forms.input_format
    desc = request.forms.description
    row = db(db.apps.id==appid).select().first()
    row.update_record(language=lang, description=desc, input_format=info,
                      command=cmd)
    db.commit()
    redirect("/app/"+app)

# allow only admin or user to delete apps
@post('/app/delete/<appid>')
def delete_app(appid):
    global user
    check_user_var()
    appname = request.forms.app
    del_app_dir = request.forms.del_app_dir
    del_app_cases = request.forms.del_app_cases
    if user == 'admin':
        # delete entry in DB
        a = appmod.app()
        a.delete(appid)
    else:
        return template("error", err="must be admin")
    # if delete files checkbox ticked
    if del_app_dir == "on":
        # delete app directory
        path = os.path.join(config.apps_dir,appname)
        if os.path.isdir(path):
            shutil.rmtree(path)
        # remove template file
        path = "views/apps/"+appname+".tpl"
        if os.path.isfile(path):
            os.remove(path)
    redirect("/apps")

@get('/app/<app>')
def view_app(app):
    if config.auth and not authorized(): redirect('/login')
    check_user_var()
    global user
    if user != 'admin': 
        return template('error',err="must be admin to edit app")
    cid = request.query.cid
    result = db(apps.name==app).select().first()
    params = {}
    params['app'] = app
    params['user'] = user
    params['apps'] = myapps.keys()
    params['cid'] = cid
    #if request.query.edit:
    #    return template('appedit', params, rows=result)
    #else:
    return template('app', params, rows=result)

@get('/start')
def getstart():
    global user
    check_user_var()
    app = request.query.app
    if config.auth and not authorized(): redirect('/login')
    if myapps[app].appname not in myapps: redirect('/apps')
    cid = request.query.cid
    if re.search("/",cid):
        (u,cid) = cid.split("/")
    else:
        u = user
    params = myapps[app].params
    # if no valid casename read default parameters
    if not re.search("[a-z]",cid):
        params = myapps[app].params
    else: # read parameters from file
        params,_,_ = myapps[app].read_params(u,cid)
    params['cid'] = cid
    params['app'] = app
    params['user'] = u
    params['apps'] = myapps.keys()
    return template('apps/' + myapps[app].appname, params)

@get('/files')
def list_files():
    global user
    cid = request.query.cid
    app = request.query.app
    path = request.query.path
    check_user_var()
    if re.search("/",cid):
        (u,cid) = cid.split("/")
    else:
        u = user
    if not path:
        path = os.path.join(myapps[app].user_dir,u,app,cid)
    params = dict()
    params['cid'] = cid
    params['app'] = app
    params['user'] = u
    params['apps'] = myapps.keys()
    params['path'] = path
    params['files'] = os.listdir(path)
    return template('files', params)

@get('/plots/edit')
def editplot():
    global user
    check_user_var()
    if user != 'admin': 
        return template('error',err="must be admin to edit plots")
    app = request.query.app
    cid = request.query.cid
    if config.auth and not authorized(): redirect('/login')
    if app not in myapps: redirect('/apps')
    query = (apps.id==plots.appid) & (apps.name==app)
    result = db(query).select()
    params = { 'app': app, 'cid': cid, 'user': user, 'apps': myapps.keys() }
    return template('plots/edit', params, rows=result)

@get('/plots/delete/<pltid>')
def delete_plot(pltid):
    app = request.query.app
    cid = request.query.cid
    del db.plots[pltid]
    db.commit()
    redirect ('/plots/edit?app='+app+'&cid='+cid)

@get('/plots/datasource/<pltid>')
def get_datasource(pltid):
    global user
    app = request.query.app
    cid = request.query.cid
    check_user_var()
    if myapps[app].appname not in myapps: redirect('/apps')
    if config.auth and not authorized(): redirect('/login')
    result = db(datasource.pltid==pltid).select()
    params = { 'app': app, 'cid': cid, 'user': user, 'pltid': pltid,
               'rows': result, 'apps': myapps.keys() }
    return template('plots/datasource', params, rows=result)

@post('/plots/datasource_add')
def add_datasource():
    app = request.forms.get('app')
    cid = request.forms.get('cid')
    pltid = request.forms.get('pltid')
    r = request.forms
    datasource.insert(pltid=pltid, filename=r['fn'], cols=r['cols'],
                      line_range=r['line_range'], data_def=r['data_def'])
    db.commit()
    redirect ('/plots/datasource/'+pltid+'?app='+app+'&cid='+cid)

@post('/plots/datasource_delete')
def delete_plot():
    app = request.forms.get('app')
    cid = request.forms.get('cid')
    pltid = request.forms.get('pltid')
    dsid = request.forms.get('dsid')
    del db.datasource[dsid]
    db.commit()
    redirect ('/plots/datasource/'+pltid+'?app='+app+'&cid='+cid)

@post('/plots/create')
def create_plot():
    app = request.forms.get('app')
    cid = request.forms.get('cid')
    r = request
    print "app:", app, "cid:", cid
    print myapps
    plots.insert(appid=myapps[app].appid, ptype=r.forms['ptype'],
                 title=r.forms['title'], options=r.forms['options'])
    db.commit()
    redirect ('/plots/edit?app='+app+'&cid='+cid)

@get('/plot/<pltid>')
def plot_interface(pltid):
    app = request.query.app
    cid = request.query.cid
    check_user_var()
    params = dict()

    if not cid:
        params['err']="No case id specified. First select a case id from the list of jobs."
        return template('error', params)

    if re.search("/",cid):
        (u,c) = cid.split("/")
    else:
        u = user
        c = cid

    sim_dir = os.path.join(myapps[app].user_dir,u,app,c)

    # use pltid of 0 to trigger finding the first pltid for the current app
    if int(pltid) == 0:
        query = (apps.id==plots.appid) & (apps.name==app)
        result = db(query).select().first()
        if result: pltid = result['plots']['id']

    p = plotmod.plot()

    # get the data for the pltid given
    try:
        result = db(plots.id==pltid).select().first()
        plottype = result['ptype']
        options = result['options']
        title = result['title']
    except:
        redirect ('/plots/edit?app='+app+'&cid='+cid)

    # if plot not in DB return error
    if plottype is None:
        params = { 'cid': cid, 'app': app, 'user': u }
        params['err'] = "Sorry! This app does not support plotting capability"
        return template('error', params)

    # determine which view template to use
    if plottype == 'flot-bar':
        tfn = 'plots/flot-bar'
    elif plottype == 'flot-cat':
        tfn = 'plots/flot-cat'
    elif plottype == 'flot-line':
        tfn = 'plots/flot-line'
    elif plottype == 'mpl-line' or plottype == 'mpl-bar':
        redirect('/mpl/'+pltid+'?app='+app+'&cid='+cid)
    else:
        tfn = 'plots/plot-line'

    # get list of all plots for this app
    query = (apps.id==plots.appid) & (apps.name==app)
    list_of_plots = db(query).select()

    # extract data from files
    data = []
    ticks = []
    plotpath = ''
    result = db(datasource.pltid==pltid).select()
    print pltid


    datadef = ""
    for r in result:
        plotfn = r['filename']
        cols = r['cols']
        line_range = r['line_range']
        try:
            datadef += r['data_def'] + ", "
        except:
            datadef = ""
        plotfn = re.sub(r"<cid>", c, plotfn)
        plotpath = os.path.join(sim_dir,plotfn)
        (col1str,col2str) = cols.split(":")
        col1 = int(col1str); col2 = int(col2str)
        # do some postprocessing
        if line_range is not None:
            (line1str,line2str) = line_range.split(":")
            line1 = int(line1str); line2 = int(line2str)
        ### there is a problem with the following statement
        ### shows up in mendel app
        #    if myapps[app].postprocess > 0:
        #        dat = process.postprocess(plotpath,line1,line2)
        #    else:
            dat = p.get_data(plotpath,col1,col2,line1,line2)
        else:
            dat = p.get_data(plotpath,col1,col2)
        # clean data
        #dat = [d.replace('?', '0') for d in dat]
        data.append(dat)
        #data.append(p.get_data(plotpath,col1,col2))
        if plottype == 'flot-cat':
            ticks = p.get_ticks(plotpath,col1,col2)
    #if not result:
    #    return template("error",err="need to specify at least one datasource")

    stats = compute_stats(plotpath)

    params = { 'cid': cid, 'pltid': pltid, 'data': data, 'app': app, 'user': u,
               'ticks': ticks, 'title': title, 'plotpath': plotpath,
               'rows': list_of_plots, 'options': options, 'datadef': datadef,
               'apps': myapps.keys(), 'stats': stats }
    return template(tfn, params)

@get('/mpl/<pltid>')
def matplotlib(pltid):
    """Generate a random image using Matplotlib and display it"""
    # in the future create a private function __import__ to import third-party
    # libraries, so that it can respond gracefully.  See for example the
    # Examples section at https://docs.python.org/2/library/imp.html
    from pylab import savefig
    import numpy as np
    import StringIO
    from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
    from matplotlib.figure import Figure
    global user
    check_user_var()
    app = request.query.app
    cid = request.query.cid

    fig = Figure()
    fig.set_tight_layout(True)
    ax = fig.add_subplot(111)

    # get info about plot from db
    p = plotmod.plot()
    result = db(plots.id==pltid).select().first()
    title = result['title']
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
        (col1str,col2str) = cols.split(":")
        col1 = int(col1str)
        col2 = int(col2str)
        if line_range is not None:
            (line1str,line2str) = line_range.split(":")
            line1 = int(line1str)
            line2 = int(line2str)

    plotfn = re.sub(r"<cid>", cid, plotfn)
    sim_dir = os.path.join(myapps[app].user_dir,user,app,cid)
    plotpath = os.path.join(sim_dir,plotfn)
    xx = p.get_column_of_data(plotpath,col1)
    yy = p.get_column_of_data(plotpath,col2)
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
    if not os.path.exists(config.tmp_dir):
        os.makedirs(config.tmp_dir)
    fn = title+'.png'
    fig.set_size_inches(7,4)
    img_path = os.path.join(sim_dir,fn)
    fig.savefig(img_path)

    # get list of all plots for this app
    query = (apps.id==plots.appid) & (apps.name==app)
    list_of_plots = db(query).select()
    stats = compute_stats(plotpath)

    params = {'image': fn, 'app': app, 'cid': cid, 'pltid': pltid,
              'plotpath': plotpath, 'img_path': img_path, 'title': title,
              'rows': list_of_plots, 'apps': myapps.keys(), 'stats': stats }
    return template('plots/matplotlib', params)

@get('/monitor')
def monitor():
    global user
    check_user_var()
    cid = request.query.cid
    app = request.query.app
    jid = request.query.jid
    params = { 'cid': cid, 'app': app, 'jid': jid, 'user': user,
               'apps': myapps.keys() }
    return template('monitor', params)

@get('/zipcase')
def zipcase():
    """zip case on machine to prepare for download"""
    global user
    import zipfile
    app = request.query.app
    cid = request.query.cid
    base_dir = os.path.join(myapps[app].user_dir,user,app)
    path = os.path.join(base_dir,cid+".zip")
    zf = zipfile.ZipFile(path, mode='w')
    sim_dir = os.path.join(base_dir,cid)
    for fn in os.listdir(sim_dir):
        zf.write(os.path.join(sim_dir,fn))
    zf.close()
    status="<a href=\""+path+"\">"+path+"</a>"
    redirect("/aws?status="+status)

@get('/zipget')
def zipget():
    """get zipfile from another machine, save to current machine"""
    zipkey = request.query.zipkey
    netloc = request.query.netloc
    #url = os.path.join(netloc,config.tmp_dir,zipkey+".zip")
    url = os.path.join(netloc,zipkey)
    try:
        f = urllib2.urlopen(url)
        print "downloading " + url
        # Open our local file for writing
        with open(os.path.basename(url), "wb") as local_file:
            local_file.write(f.read())
    #handle errors
    except urllib2.HTTPError, e:
        print "HTTP Error:", e.code, url
    except urllib2.URLError, e:
        print "URL Error:", e.reason, url
    status = "file downloaded"
    redirect("/aws?status="+status)

@get('/addapp')
def getaddapp():
    global user
    if user != 'admin': 
        return template('error',err="must be admin to add app")
    return template('appconfig/addapp')

@post('/addapp')
def addapp():
    global user
    check_user_var()
    if user != 'admin': 
        return template('error',err="must be admin to add app")
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
    a = appmod.app()
    #print "user:",user
    uid = users(user=user).id
    a.create(appname, description, category, language,
             input_format, command, preprocess, postprocess, uid)
    redirect('/app/'+appname)

@get('/appconfig/status')
def appconfig_status():
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
    if os.path.exists(os.path.join(config.apps_dir,app,app+".in")):
        status['inputs'] = 1
    else:
        status['inputs'] = 0
    # check app binary
    if os.path.exists(os.path.join(config.apps_dir,app,app)):
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
    global user
    if user != 'admin': 
        return template('error',err="must be admin to configure app")
    if step == "upload":
        appname = request.forms.appname
        params = {'appname': appname}
        return template('appconfig/exe_upload',params)
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
            save_path_dir = os.path.join(appmod.apps_dir,name)
            if not os.path.exists(save_path_dir):
                os.makedirs(save_path_dir)
            save_path = os.path.join(save_path_dir,name) + ext
            if os.path.isfile(save_path):
                timestr = time.strftime("%Y%m%d-%H%M%S")
                shutil.move(save_path,save_path+"."+timestr)
            upload.save(save_path)
            os.chmod(save_path,0700)

            # process = subprocess.Popen(["otool -L", save_path], stdout=subprocess.PIPE, stdin=subprocess.PIPE)
            # contents = process.readlines()
            contents = "SUCCESS"

            params = {'appname': appname, 'contents': contents}
            return template('appconfig/exe_test', params)
        except IOError:
            return "IOerror:", IOError
        else:
            return "ERROR: must be already a file"

@post('/appconfig/inputs/<step>')
def edit_inputs(step):
    global user
    if user != 'admin': 
        return template('error',err="must be admin to edit app")
    # upload zip file and return a text copy of the input file
    if step == "upload":
        appname = request.forms.appname
        input_format = request.forms.input_format
        params = {'appname': appname, 'input_format': input_format}
        return template('appconfig/inputs_upload',params)
    if step == "parse":
        input_format = request.forms.input_format
        appname    = request.forms.appname
        upload     = request.files.upload
        if not upload:
            return template('appconfig/error',
                   err="no file selected. press back button and try again")
        name, ext = os.path.splitext(upload.filename)
        if ext not in ('.in','.ini','.xml','.json',):
            return 'ERROR: File extension not allowed.'
        try:
            save_path_dir = os.path.join(appmod.apps_dir,name)
            if not os.path.exists(save_path_dir):
                os.makedirs(save_path_dir)
            save_path = os.path.join(save_path_dir,name) + ext
            if os.path.isfile(save_path):
                timestr = time.strftime("%Y%m%d-%H%M%S")
                shutil.move(save_path,save_path+"."+timestr)
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
            else:
                return "ERROR: input_format not valid: ", input_format
            path = os.path.join(config.apps_dir,appname,fn)
            params = {'fn': fn, 'contents': slurp_file(path),
                      'appname': appname, 'input_format': input_format }
            return template('appconfig/inputs_parse', params)
        except IOError:
            return "IOerror:", IOError
        else:
            return "ERROR: must be already a file"
    # show parameters with options how to tag and describe each parameter
    elif step == "create_view":
        input_format = request.forms.input_format
        appname = request.forms.appname
        myapp = app_instance(input_format,appname)
        inputs,_,_ = myapp.read_params()
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
        key_tag = dict(zip(keys,html_tags))
        key_desc = dict(zip(keys,descriptions))
        input_format = request.forms.input_format
        myapp = app_instance(input_format,appname)
        params,_,_ = myapp.read_params()
        if myapp.create_template(html_tags=key_tag,bool_rep=bool_rep,desc=key_desc):
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
#def select_input_file(appname,fn):
#    path = os.path.join(config.apps_dir,appname,fn)
#    params = {'fn': fn, 'contents': slurp_file(path), 'appname': appname }
#    return template('appconfig/step3', params)

@post('/upload')
def upload_data():
    global user
    if config.auth and not authorized(): redirect('/login')
    upload = request.files.upload
    if not upload:
        return template('error', err="no file selected.")
    #name, ext = os.path.splitext(upload.filename)
    #if ext not in ('.zip','.txt'):
    #    return template('error', err="file extension not allowed")
    #try:
    save_path_dir = os.path.join(config.user_dir,user,config.upload_dir)
    save_path = os.path.join(save_path_dir,upload.filename)
    if os.path.isfile(save_path):
        return template('error', err="file exists")
    upload.save(save_path)
    return "SUCCESS"
    #except:
    #    return "FAILED"

def app_instance(input_format,appname,preprocess=0,postprocess=0):
    if(input_format=='namelist'):
        myapp = appmod.namelist(appname,preprocess,postprocess)
    elif(input_format=='ini'):
        myapp = appmod.ini(appname,preprocess,postprocess)
    elif(input_format=='xml'):
        myapp = appmod.xml(appname,preprocess,postprocess)
    elif(input_format=='json'):
        myapp = appmod.json(appname,preprocess,postprocess)
    else:
        return 'ERROR: input_format ',input_format,' not supported'
    return myapp

def authorized():
    '''Return True if user is already logged in, False otherwise'''
    global user
    s = request.environ.get('beaker.session')
    s[USER_ID_SESSION_KEY] = s.get(USER_ID_SESSION_KEY,False)
    if not s[USER_ID_SESSION_KEY]:
        return False
    else:
        user = s[USER_ID_SESSION_KEY]
        return True

def getuser():
    '''Return the current user, if logged in'''
    global user
    return user

if __name__ == "__main__":
    # set user session if authentication is disabled
    if not config.auth:
        s = {USER_ID_SESSION_KEY: "guest"}
        user = s[USER_ID_SESSION_KEY]
    # load apps into memory
    load_apps()
    # start a polling thread to continuously check for queued jobs
    sched.poll()
    # attempt to mix in docker functionality
    try:
        dockermod.bind(globals())
        app.app.merge(dockermod.dockerMod)
    except Exception,e:
        pass
    # run the app
    try:
        run(server=config.server, app=app, host='0.0.0.0',\
            port=config.port, debug=False)
    except:
        run(app=app, host='0.0.0.0', port=config.port, debug=False)
