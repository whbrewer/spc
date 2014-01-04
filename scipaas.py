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
import config
import sqlite3 as lite

# default user - if not logged in
user = "guest"

# sqlite plugin
plugin = ext.sqlite.Plugin(dbfile=config.database)
install(plugin)

# create instance of scheduler
sched = scheduler.scheduler()

pbuffer = ''

@post('/<app>/confirm')
def confirm_form(app):
    global user
    # if case_id not in form will throw error, but just ignore it
    # as some apps will not use case_id
    try:
        cid = request.forms['case_id']
    except: 
        return "ERROR: problem with template... case_id not in form"
    params = {'cid': cid, 'app': app, 'user': user }
    #print 'cid:%s,app:%s' % (cid, app)

    if(myapps[app].write_params(request.forms,user)):
        return template('confirm', params)
    else:
        return 'ERROR: failed to write parameters to file'

@post('/<app>/<cid>/execute')
def execute(app,cid):
    global user
    try:
        run_dir = myapps[app].user_dir + os.sep + user + os.sep + myapps[app].appname + os.sep + cid
        print 'run_dir:',run_dir
        ofn = run_dir + os.sep + myapps[app].outfn
	    # this path works for OSX
        rel_path = os.pardir + os.sep + os.pardir + os.sep + os.pardir + os.sep + os.pardir + os.sep 
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
        params = { 'cid': cid, 'output': pbuffer, 'app': app, 'user': user }
        return template('output',params)

    except OSError, e:
        print >>sys.stderr, "Execution failed:", e
        params = { 'cid': cid, 'output': pbuffer, 'app': app, 'user': user }
        return template('error',params)
        #return "ERROR: failed to start job"

@get('/<app>/<cid>/output')
def output(app,cid):
    global user
    run_dir = myapps[app].user_dir + os.sep + user + os.sep + myapps[app].appname + os.sep + cid
    ofn = run_dir + os.sep + myapps[app].outfn
    f = open(ofn,'r')
    output = f.read()
    f.close()
    params = { 'cid': cid, 'output': output, 'app': app, 'user': user }
    return template('output', params)
   
@route('/')
def root():
    return template('overview')

@route('/<app>')
def show_app(app):
    global user, myapps
    # parameters for return template
    params = myapps[app].params
    print app, 'params:',params
    params['cid'] = 'test00'
    params['app'] = app
    params['user'] = user
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
    global user
    user     = request.forms.get('user')
    password = request.forms.get('password')
    u = users.user()
    if u.authenticate(user,password):
        params = myapps[default_app].params
        params['app'] = default_app
        params['cid'] = ''
        params['user'] = user
        tpl = myapps[default_app].appname 
        return template(tpl, params)
    else:
        return "<p>Login failed: wrong username or password</p>"

@get('/apps')
def showapps():
    redirect("/apps/show/name")

@get('/apps/load')
def load_apps(db):
    # this needs to be moved into apps.py in the future
    global myapps, default_app
    # Connect to DB 
    try:
        db = lite.connect(config.database)
    except lite.Error, e:
        print "Error %s:" % e.args[0]
        sys.exit(1)
    c = db.execute('SELECT name,appid FROM apps')
    result = c.fetchall()
    c.close()
    myapps = {}
    for row in result:   
        name = row[0]
        appid = row[1]
        print 'loading: %s id: %s' % (name,appid)
        myapp = apps.f90(name,appid)
        myapps[name] = myapp
    default_app = name # simple soln - use last app read from DB
    return 0

@get('/apps/show/<sort>')
def getapps(db,sort="name"):
    c = db.execute('SELECT * FROM apps ORDER BY ' + sort) 
    result = c.fetchall()
    c.close()
    return template('apps', rows=result)

@get('/apps/add')
def create_app_form():
    return static_file('addapp.html', root='static')

@post('/apps/add')
def addapp():
    # get data from form
    appname = request.forms.get('appname')
    description = request.forms.get('description')
    category = request.forms.get('category')
    language = request.forms.get('language')  
    # put in db
    a = apps.app()
    a.create(appname,description,category,language)
    redirect("/apps/show/name")

@post('/apps/create_view')
def create_view():
    appname = request.forms.get('appname')
    myapp = apps.f90(appname)
    #params,_,_ = myapp.read_params()
    if myapp.write_html_template():
        return "SUCCESS: successfully output template"
    else:
        return "ERROR: there was a problem when creating view"

@get('/apps/delete/<appid>')
def delete_app(appid):
    a = apps.app()
    a.delete(appid)
    redirect("/apps/show/name")

@get('/apps/edit/<appid>')
def edit_app(appid):
    return 'SORRY - this function has not yet been implemented'
    a = apps.app()
    (name,description,category,language) = a.read(appid)
    params = {'name': name, 'description': description, 'category': category, 'language': language }
    return template(app_edit, params)

@get('/<app>/start')
def getstart(app):
    global user
    params = myapps[app].params
    cid = request.forms.get('cid')
    if cid is '':
        params = myapps[app].params
    else:
        params,_,_ = myapps[app].read_params(user,cid)
    #params['cid'] = params['case_id']
    params['cid'] = cid
    params['app'] = app
    params['user'] = user
    return template(myapps[app].appname, params)

@get('/<app>/list')
def list(app):
    global user
    str = ''
    cid = request.forms.get('cid')
    for case in os.listdir(myapps[app].user_dir+os.sep+user+os.sep+app):
        str += '<a onclick="set_cid(\'' + case + '\')">' + case + '</a><br>\n'
    params = { 'content': str }
    params['cid'] = cid
    params['app'] = app
    params['user'] = user
    return template('list', params)

@get('/<app>/plots')
@get('/<app>/<cid>/plots')
def get_plots(db,app):
    try: print cid
    except: cid='test00'
    c = db.execute('select pltid, type, filename, col1, col2, title from apps natural join plots where name=?',(app,))
    result = c.fetchall()
    c.close()
    params = { 'app': app, 'cid': cid } 
    return template('plots', params, rows=result)

@get('/<app>/plots/delete/<pltid>')
def delete_plot(db,app,pltid):
    p = plots.plot()
    p.delete(pltid)
    redirect ('/' + app + '/plots')

@post('/<app>/plots/create')
def create_plot(app):
    p = plots.plot()
    r = request
    p.create(myapps[app].appid,r.forms['ptype'],r.forms['fn'],r.forms['col1'],r.forms['col2'],r.forms['title'])
    redirect ('/' + app + '/plots')

@get('/<app>/<cid>/plot/<pltid>')
def plot_interface(app,cid,pltid):
    global user
    p = plots.plot()
    (plottype,plotfn,col1,col2,title) = p.read(app,pltid)

    # if plot not in DB return error
    if plottype is None:
        params = { 'cid': cid, 'app': app, 'user': user }
        params['err'] = "Sorry! This app does not support plotting capability"
        return template('error', params)

    sim_dir = myapps[app].user_dir+os.sep+user+os.sep+app+os.sep+cid+os.sep
    if re.search(r'^\s*$', cid):
        return "Error: no case id specified"
    else:
        plotfn = re.sub(r"<cid>", cid, plotfn)
        print sim_dir + plotfn
        p = plots.plot()
        data = p.get_data(sim_dir + plotfn,col1,col2)
        params = { 'cid': cid, 'data': data, 'app': app, 'user': user, 'title': title }
        return template('plot', params)

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
        save_path_dir = apps.apps_dir + os.sep + name
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

if __name__ == "__main__":
    db = lite.connect(config.database)
    load_apps(db)
    run(host='0.0.0.0', port=8081, debug=True)

