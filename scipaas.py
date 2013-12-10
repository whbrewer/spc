from bottle import *
from bottle.ext import sqlite
import scheduler
import subprocess
import string, random
import sys, os, re
import plots
import apps
import uploads
import users

# sqlite plugin
plugin = ext.sqlite.Plugin(dbfile='scipaas.db')
install(plugin)

# create instance of scheduler
sched = scheduler.scheduler()

# app configuration here
mendel = apps.app_f90('mendel','<cid>.000.hst')
burger = apps.app_f90('burger','burger.dat')
dna = apps.app_f90('dna','dna.dat')
myapps = { 'mendel': mendel, 'burger': burger, 'dna': dna }
default_app = 'mendel'
# end app config

pbuffer = ''

@get('/createapp')
def create_app_form():
    return static_file('createapp.html', root='static')

@post('/createapp')
def create_app():
    appname = request.forms['appname']
    # create directory for app binary/source
    os.mkdir(apps.apps_dir + os.sep + appname)
    # create directory for user data
    os.mkdir(apps.user_dir + os.sep + appname)
    # create the template directory
    os.mkdir(apps.user_dir + os.sep + appname + os.sep + apps.template_dir)
    # create a new instance of the app
    # add app instance to myapps data structure
    return appname, ' app created'

@post('/<app>/confirm')
def confirm_form(app):
    # if case_id not in form will throw error, but just ignore it
    # as some apps will not use case_id
    try:
        cid = request.forms['case_id']
    except: 
        # give some nice error message here in the future
        pass
    params = {'cid': cid, 'app': app }
    #print 'cid:%s,app:%s' % (cid, app)

    if(myapps[app].write_params(request.forms)):
        return template('confirm', params)
    else:
        return 'ERROR: failed to write parameters to file'

@post('/<app>/<cid>/execute')
def execute(app,cid):
    try:
        run_dir = myapps[app].user_dir + os.sep + cid 
        ofn = run_dir + os.sep + myapps[app].outfn
	    # this path works for OSX
        rel_path = os.pardir + os.sep + os.pardir + os.sep + os.pardir + os.sep 
        cmd = rel_path + myapps[app].exe
	    # this path works for Windows
        #cmd = myapps[app].exe 
        f = open(ofn,'w')
        p = subprocess.Popen([cmd], cwd=run_dir, stdout=subprocess.PIPE)
        # schedule job
        sched.qsub(cmd)
        pbuffer = ''
        while p.poll() is None:
            out = p.stdout.readline()
            f.write(out)
            pbuffer += out 
        p.wait()
        f.close()
        params = { 'cid': cid, 'output': pbuffer, 'app': app }
        return template('output',params)

    except OSError, e:
        print >>sys.stderr, "Execution failed:", e
        return "ERROR: failed to start job"

@post('/<app>/<cid>/output')
def output(app,cid):
    #print "output app:",app,"."
    run_dir = myapps[app].user_dir + os.sep + cid 
    #print "output run_dir:",run_dir
    ofn = run_dir + os.sep + myapps[app].outfn
    f = open(ofn,'r')
    output = f.read()
    f.close()
    params = { 'cid': cid, 'output': output, 'app': app }
    return template('output', params)
   
@route('/')
def overview():
    return template('overview')

@route('/<app>')
def show_app(app):
    params = myapps[app].params
    params['cid'] = 'test00'
    params['app'] = app
    return template(app, params)

@get('/login')
def login_form():
    return '''<form method="POST" action="/login">
                <input name="user"     type="text" />
                <input name="password" type="password" />
                <input type="submit" />
              </form>'''

@route('/static/:path#.+#', name='static')
def static(path):
    return static_file(path, root='static')

@post('/login')
def login_submit(db):
    user     = request.forms.get('user')
    password = request.forms.get('password')
    u = users.user()
    if u.authenticate(user,password):
        params = myapps[default_app].params
        params['app'] = default_app
        params['cid'] = ''
        tpl = myapps[default_app].appname 
        return template(tpl, params)
    else:
        return "<p>Login failed: wrong username or password</p>"
    
@get('<app>/start')
def getstart(app):
    params = myapps[app].params
    params['cid'] = params['case_id']
    return template(myapps[app].appname, params)

@post('/<app>/start')
def start(app):
    # ignore blockmap and blockorder from read_params()
    cid = request.forms['cid']
    if cid is '':
        params = myapps[app].params
    else:
        params,_,_ = myapps[app].read_params(cid)
    params['cid'] = cid
    params['app'] = app
    return template(myapps[app].appname, params)

@post('/<app>/list')
def list(app):
    str = ''
    cid = request.forms['cid']
    for case in os.listdir(myapps[app].user_dir):
        str += '<a onclick="set_cid(\'' + case + '\')">' + case + '</a><br>\n'
    content = { 'content': str }
    content['cid'] = cid
    content['app'] = app
    return template('list', content)

@post('/<app>/<cid>/plot')
def plot_interface(app,cid):
    sim_dir = myapps[app].user_dir + os.sep + cid + os.sep
    if re.search(r'^\s*$', cid):
        return "Error: no case id specified"
    else:
        plotfn = re.sub(r"<cid>", cid, myapps[app].plotfn)
        print sim_dir + plotfn
        p = plots.plot()
        data = p.get_data(sim_dir + plotfn,0,1)
        params = { 'cid': cid, 'data': data, 'app': app }
        return template('plot', params)

@post('/upload')
def do_upload():
    appname    = request.forms.get('appname')
    upload     = request.files.get('upload')
    name, ext = os.path.splitext(upload.filename)
    if ext not in ('.zip','.txt'):
        return 'File extension not allowed.'
    try:
        save_path_dir = apps.apps_dir + os.sep + name
        save_path = save_path_dir + ext
        if os.path.isfile(save_path):
            return 'ERROR: zip file exists already. Please remove first.'
        upload.save(save_path)
        # before unzip file check if directory exists
        if os.path.isdir(save_path_dir):
            return 'ERROR: app already exists. Please change name.'
        else:
            u = uploads.uploader()
            u.unzip(save_path)
            return 'OK'
        # remove zip file
        os.remove(save_path)
    except IOError:
        return "IOerror:", IOError
        raise
    else:
        return "ERROR: must be already a file"

run(host='0.0.0.0', port=8081, debug=True)

