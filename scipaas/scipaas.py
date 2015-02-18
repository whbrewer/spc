#!/usr/bin/env python

# web framework
from bottle import *
# python built-ins
import uuid, hashlib, shutil, string
import random, subprocess, sys, os, re
import cgi, urllib2, json, smtplib
# other SciPaaS modules
import config, uploads, process
import scheduler, scheduler_smp
import apps as appmod
import plots as plotmod
import aws as awsmod
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
#sched = scheduler.scheduler()
sched = scheduler_smp.scheduler()

pbuffer = ''

@post('/confirm')
def confirm_form():
    global user
    check_user_var()
    app = request.forms.app
    cid = str(uuid.uuid4())[:6]
    # pass the case_id to be used by the program input parameters,
    # if case_id is defined in the input deck it will be used
    # otherwise it is ignored
    request.forms['case_id'] = cid 
    myapps[app].write_params(request.forms,user)
    # read the file 
    run_dir = os.path.join(myapps[app].user_dir,user,myapps[app].appname,cid)
    fn = os.path.join(run_dir,myapps[app].simfn)
    inputs = slurp_file(fn)
    # convert html tags to entities (e.g. < to &lt;)
    inputs = cgi.escape(inputs)
    params = { 'cid': cid, 'inputs': inputs, 'app': app, 
               'user': user, 'apps': myapps.keys(), 'np': config.np }
    try:
        return template('confirm', params)
    except:
        return 'ERROR: failed to write parameters to file'

@post('/execute')
def execute():
    global user
    check_user_var()
    app = request.forms.app
    cid = request.forms.cid
    np = request.forms.np
    params = {}
    base_dir = os.path.join(myapps[app].user_dir,user,app,cid)

    # if preprocess is set run the preprocessor
    try:
        if myapps[app].preprocess:
            run_params,_,_ = myapps[app].read_params(user,cid) 
            processed_inputs = process.preprocess(run_params,
                                       myapps[app].preprocess)
            sim_dir = os.path.join(base_dir,myapps[app].preprocess)
            f = open(sim_dir,'w') 
            f.write(processed_inputs)
            f.close()
    except:
        return template('error',err="There was an error with the preprocessor")

    # start the job
    try:
        params['cid'] = cid
        params['app'] = app
        params['user'] = user
        jid = sched.qsub(app,cid,user,np)
        redirect("/monitor?app="+app+"&cid="+cid+"&jid="+jid)
    except OSError, e:
        print >>sys.stderr, "Execution failed:", e
        params = { 'cid': cid, 'output': pbuffer, 'app': app, 'user': user, 
                   'err': e, 'apps': myapps.keys() }
        return template('error',params)

@get('/more')
def more():
    """given a form with the attribute plotpath, output the file to the browser"""
    global user
    app = request.query.app
    cid = request.query.cid
    filepath = request.query.filepath
    contents = slurp_file(filepath)
    params = { 'cid': cid, 'contents': contents, 'app': app, 'user': user, 
               'fn': filepath, 'apps': myapps.keys() }
    return template('more', params)

@get('/output')
def output():
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
        params = { 'cid': cid, 'contents': output, 'app': app, 'user': u, 'fn': fn,
                   'apps': myapps.keys() }
        return template('more', params)
    except:
        params = { 'app': app, 'err': "Couldn't read input file. Check casename." } 
        return template('error', params)

@get('/inputs')
def inputs():
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
        params = { 'cid': cid, 'contents': inputs, 'app': app, 'user': u, 'fn': fn,
                   'apps': myapps.keys() }
        return template('more', params)
    except:
        params = { 'app': app, 'err': "Couldn't read input file. Check casename." } 
        return template('error', params)

def slurp_file(path):
    """read file given by path and return the contents of the file"""
    try:
        f = open(path,'r')
        data = f.read()
        f.close()
        return data
    except IOError:
        return("ERROR: the file cannot be opened or does not exist.\nPerhaps the job did not start?")

@get('/<app>/<cid>/tail')
def tail(app,cid):
    global user
    check_user_var()
    num_lines = 30
    run_dir = os.path.join(myapps[app].user_dir,user,myapps[app].appname,cid)
    ofn = os.path.join(run_dir,myapps[app].outfn)
    if os.path.exists(ofn):
        f = open(ofn,'r')
        output = f.readlines()
        myoutput = output[len(output)-num_lines:]
        xoutput = ''.join(myoutput)
        f.close()
    else:
        xoutput = 'waiting to start...'
    params = { 'cid': cid, 'contents': xoutput, 'app': app, 'user': user, 'fn': ofn,
               'apps': myapps.keys() }
    return template('more', params)

@get('/')
def root():
    if not authorized(): redirect('/login')
    return template('overview')

@get('/jobs')
def show_jobs():
    if not authorized(): redirect('/login')
    #if app not in myapps: redirect('/apps')
    global user
    cid = request.query.cid
    app = request.query.app
    check_user_var()
    result = db(jobs.user==user).select()
    params = {}
    params['cid'] = cid
    params['app'] = app
    params['user'] = user
    params['apps'] = myapps.keys()
    return template('jobs', params, rows=result)

@get('/aws')
def get_aws():
    if not authorized(): redirect('/login')
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
    if not authorized(): redirect('/login')
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
    if not authorized(): redirect('/login')
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
    rate = instances['rate']
    if not rate: rate = 0.0
    return awsmod.ec2(key,secret,account_id,instance,region,rate)

@get('/aws/status/<aid>')
def aws_status(aid):
    if not authorized(): redirect('/login')
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
    try:
        astatus = a.status()
        astatus['uptime'] = a.uptime(astatus['launch_time'])
        astatus['charge since last boot'] = a.charge(astatus['uptime'])
        return template('aws_status',params,astatus=astatus)
    except:
        return template('error',err="There was a problem connecting to the AWS machine. Check the credentials and make sure the machine is running.")

@get('/aws/start/<aid>')
def aws_start(aid):
    if not authorized(): redirect('/login')
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
    a.start()
    time.sleep(5) # takes a few seconds for the status to change on the Amazon end
    astatus = a.status()
    return template('aws_status',params,astatus=astatus)

@get('/aws/stop/<aid>')
def aws_stop(aid):
    if not authorized(): redirect('/login')
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
    time.sleep(5) # takes a few seconds for the status to change on the Amazon end
    return template('aws_status',params,astatus=a.status())

@get('/account')
def get_account():
    if not authorized(): redirect('/login')
    global user
    check_user_var()
    app = request.query.app
    params = {}
    params['app'] = app
    params['user'] = user
    params['apps'] = myapps.keys()
    uid = users(user=user).id
    return template('account',params)

@get('/wall')
def get_wall():
    """Return the records from the wall table."""
    if not authorized(): redirect('/login')
    global user
    cid = request.query.cid
    app = request.query.app
    # note: =~ means sort by descending order
    result = db(jobs.id==wall.jid).select(orderby=~wall.id)
    params = {}
    params['cid'] = cid
    params['app'] = app
    params['user'] = user
    params['apps'] = myapps.keys()
    return template('wall', params, rows=result)

@post('/wall')
def post_wall():
    if not authorized(): redirect('/login')
    check_user_var()
    app = request.forms.app
    cid = request.forms.cid
    jid = request.forms.jid
    comment = request.forms.comment
    # save comment to db
    wall.insert(jid=jid, comment=comment)
    db.commit()
    # get all wall comments
    result = db().select(wall.ALL)
    params = {}
    params['cid'] = cid
    params['app'] = app
    params['user'] = user
    redirect('/wall')

@get('/wall/delete/<wid>')
def delete_wall_item(wid):
    if not authorized(): redirect('/login')
    check_user_var()
    app = request.query.app
    cid = request.query.cid
    del db.wall[wid]
    db.commit()
    redirect ('/wall?app='+app+'&cid='+cid)

@get('/jobs/delete/<jid>')
def delete_job(jid):
    if not authorized(): redirect('/login')
    check_user_var()
    app = request.query.app
    cid = request.query.cid
    path = os.path.join(myapps[app].user_dir,user,app,cid)
    if os.path.isdir(path):
        shutil.rmtree(path)
    sched.qdel(jid)
    redirect("/jobs")

@post('/proc/stop')
def stop_job():
    if not authorized(): redirect('/login')
    check_user_var()
    app = request.query.app
    cid = request.query.cid
    jid = request.forms.jid
    sched.stop(jid)
    redirect("/monitor?app="+app+"&cid="+cid+"&jid="+jid)

@get('/<app>')
def show_app(app):
    if not authorized(): redirect('/login')
    check_user_var()
    global user, myapps
    # set a session variable to keep track of the current app
    s = request.environ.get('beaker.session')
    s[APP_SESSION_KEY] = app
    # parameters for return template
    params = myapps[app].params
    params['cid'] = '' 
    params['app'] = app
    params['user'] = user
    params['apps'] = myapps
    return template(os.path.join(config.apps_dir,app), params)

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
    return server_static('favicon.ico')

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
    if not authorized(): redirect('/login')
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
        users.insert(user=user, passwd=hashpw, email=email)
        db.commit()
        # email admin user
        try:
            server = smtplib.SMTP('localhost')
            message = user + " just registered to scipaas " + email
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
    if not authorized(): redirect('/login')
    if not user == "admin": 
        return template("error",err="must be admin to delete")
    query = (apps.id==plots.appid) & (apps.name==app)
    result = db().select(users.ALL)
    params = {'user': user}
    return template('admin/users',params,rows=result)

@post('/admin/delete_user')
def admin_delete_user():
    global user
    if not authorized(): redirect('/login')
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
    """This is the server-side AJAX function to check if a username 
       exists in the DB."""
    # return booleans as strings here b/c they get parsed by JavaScript
    if users(user=user): return 'true'
    else: return 'false' 

def check_user_var():
    # this check is because user is global var when restarting scipaas
    # user does not exist so return... need to implement better solution
    # such as using a session variable to check for user
    try: user
    except: redirect('/apps')
    return True

@get('/apps')
def showapps():
    if not authorized(): redirect('/login')
    result = db().select(apps.ALL)
    params = { 'apps': myapps.keys() }
    return template('apps', params, rows=result)

@get('/apps/load')
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
        print 'loading: %s (id: %s)' % (name,appid)
        if(input_format=='namelist'):
            myapp = appmod.namelist(name,appid)
        elif(input_format=='ini'):
            myapp = appmod.ini(name,appid,preprocess,postprocess)
        elif(input_format=='xml'):
            myapp = appmod.xml(name,appid)
        elif(input_format=='json'):
            myapp = appmod.json(name,appid)
        else:
            return 'ERROR: input_format ',input_format,' not supported'
        myapps[name] = myapp
    default_app = name # simple soln - use last app read from DB
    return 0

@get('/apps/add')
def create_app_form():
    if not authorized(): redirect('/login')
    return static_file('addapp.html', root='static')

@post('/apps/add')
def addapp():
    # get data from form
    appname = request.forms.get('appname')
    description = request.forms.get('description')
    category = request.forms.get('category')
    language = request.forms.get('language')  
    input_format = request.forms.get('input_format')
    command = request.forms.get('command')
    preprocess = request.forms.get('preprocess')
    postprocess = request.forms.get('postprocess')
    # put in db
    a = appmod.app()
    a.create(appname,description,category,language,input_format,command,preprocess,postprocess)
    redirect("/apps")

@post('/apps/create_view')
def create_view():
    appname = request.forms.get('appname')
    params,_,_ = myapp.read_params()
    if myapp.write_html_template():
        return "SUCCESS: successfully output template"
    else:
        return "ERROR: there was a problem when creating view"

# this is dangerous... needs to be POST not GET
@get('/apps/delete/<appid>')
def delete_app(appid):
    a = appmod.app()
    a.delete(appid)
    redirect("/apps")

@get('/apps/edit/<appid>')
def edit_app(appid):
    return 'SORRY - this function has not yet been implemented'

@get('/start')
def getstart():
    global user
    check_user_var()
    app = request.query.app
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

    case_path = os.path.join(myapps[app].user_dir,u,app)
        
    binary_extensions = ['.bz2','.gz','.xz','.zip']
    image_extensions = ['.png','.gif','.jpg']
    str = '<table>'
    for fn in os.listdir(path):
        this_path = os.path.join(path,fn)
        _, ext = os.path.splitext(this_path)
        str += '<tr>'
        #str += '<td><form action="/'+app+'/delete/'+fn+'">'
        #str += '<input type="image" src="/static/images/trash_can.gif"></form></td>\n'
        str += '<td>'
        if os.path.isdir(this_path): 
            str += '<a href="/files?app='+app+'&cid='+cid+'&path='+this_path+'">'+fn+'/</a>'
        elif ext in binary_extensions:
            str += '<a href="'+this_path+'">'+fn+'</a>'
        elif ext in image_extensions:
            str += '<a href="'+this_path+'"><img src="'+this_path+'" width=100><br>'+fn+'</a>'
        else:
            str += '<a href="/more?app='+app+'&cid='+cid+\
                       '&filepath='+os.path.join(path,fn)+'">'+fn+'</a>'
        str += '</td></tr>\n'
    str += '</table>'
    params = { 'content': str }
    params['cid'] = cid
    params['app'] = app
    params['user'] = u
    params['apps'] = myapps.keys()
    params['cases'] = '<a href="/files?app='+app+'&cid='+cid+'&path='+case_path+'">cases</a>'
    return template('files', params)

@get('/plots/edit')
def editplot():
    global user
    app = request.query.app
    cid = request.query.cid
    check_user_var()
    if not authorized(): redirect('/login')
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
    if not authorized(): redirect('/login')
    result = db(datasource.pltid==pltid).select()
    params = { 'app': app, 'cid': cid, 'user': user, 'pltid': pltid, 'rows': result,
               'apps': myapps.keys() } 
    return template('plots/datasource', params, rows=result)

@post('/plots/datasource_add')
def add_datasource():
    app = request.forms.get('app')
    cid = request.forms.get('cid')
    pltid = request.forms.get('pltid')
    r = request.forms
    datasource.insert(pltid=pltid, filename=r['fn'], cols=r['cols'], line_range=r['line_range'],
                      label=r['label'], ptype=r['ptype'], color=r['color'])
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
    plots.insert(appid=myapps[app].appid,ptype=r.forms['ptype'],title=r.forms['title'],options=r.forms['options'],datadef=r.forms['datadef'])
    db.commit()
    redirect ('/plots/edit?app='+app+'&cid='+cid)

@get('/plot/<pltid>')
def plot_interface(pltid):
    app = request.query.app
    cid = request.query.cid
    check_user_var()

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
        datadef = result['datadef']
        #x = json.loads(datadef)
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

    for r in result:
        plotfn = r['filename']
        cols = r['cols']
        line_range = r['line_range']
        plotfn = re.sub(r"<cid>", c, plotfn)
        plotpath = os.path.join(sim_dir,plotfn)
        (col1str,col2str) = cols.split(":")
        col1 = int(col1str); col2 = int(col2str)
        # do some postprocessing
        if line_range is not None:
            (line1str,line2str) = line_range.split(":")
            line1 = int(line1str); line2 = int(line2str)
            if myapps[app].postprocess > 0:
                dat = process.postprocess(plotpath,line1,line2)
            else:
                dat = p.get_data(plotpath,col1,col2,line1,line2) 
        else: 
            dat = p.get_data(plotpath,col1,col2)
        # clean data
        #dat = [d.replace('?', '0') for d in dat]
        data.append(dat)
        #data.append(p.get_data(plotpath,col1,col2))
        if plottype == 'flot-cat':
            ticks = p.get_ticks(plotpath,col1,col2)
    if not result:
        return template("error",err="need to specify at least one datasource")

    params = { 'cid': cid, 'pltid': pltid, 'data': data, 'app': app, 'user': u, 
               'ticks': ticks, 'title': title, 'plotpath': plotpath, 
               'rows': list_of_plots, 'options': options, 'datadef': datadef,
               'apps': myapps.keys() } 
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
    app = request.query.app
    cid = request.query.cid

    fig = Figure()
    ax = fig.add_subplot(111)

    # get info about plot 
    p = plotmod.plot()
    result = db(plots.id==pltid).select().first()
    plottype = result['ptype']
    options = result['options']
    title = result['title']

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

    # plot
    if plottype == 'mpl-line':
        ax.plot(xx, yy)
    elif plottype == 'mpl-bar':
        ax.hist(xx, yy, normed=1, histtype='bar', rwidth=0.8)
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

    params = {'image': fn, 'app': app, 'cid': cid, 'pltid': pltid, 
              'plotpath': plotpath, 'img_path': img_path, 'title': title, 
              'rows': list_of_plots, 'apps': myapps.keys() } 
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
    redirect("/aws?status="+path)

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

@post('/apps/upload')
def do_upload():
    #appname    = request.forms.get('appname')
    upload     = request.files.get('upload')
    name, ext = os.path.splitext(upload.filename)
    # we're not inputting appname yet so hold off on this check
    #if not name == appname:
    #    return 'ERROR: appname does not equal upload filename... try again'
    if ext not in ('.zip','.txt'):
        return 'ERROR: File extension not allowed.'
    try:
        save_path_dir = os.path.join(appmod.apps_dir,name)
        save_path = save_path_dir + ext
        if os.path.isfile(save_path):
            return 'ERROR: zip file exists already. Please remove first.'
        upload.save(save_path)
        # before unzip file check if directory exists
        if os.path.isdir(save_path_dir):
            msg = 'ERROR: app already exists. Please change name.'
        else:
            u = uploads.uploader()
            u.unzip(save_path)
            msg = u.verify(save_path_dir,name)
        # remove zip file
        os.remove(save_path)
        return msg
    except IOError:
        return "IOerror:", IOError
        raise
    else:
        return "ERROR: must be already a file"

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

if __name__ == "__main__":
    load_apps()
    # start a polling thread to continuously check for queued jobs
    sched.poll() 
    try:
        run(server=config.server, app=app, host='0.0.0.0', port=8081, debug=True)
    except:
        run(app=app, host='0.0.0.0', port=8081, debug=True)
    #run(app=app, host='0.0.0.0', port=8081, debug=True)
