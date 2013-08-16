from bottle import route, template, static_file, view
from bottle import get, post, request, run
import subprocess
import string, random
import sys, os, re
import flot
import apps
import login

mendel = apps.app_f90('mendel')
burger = apps.app_f90('burger')
myapps = { 'mendel': mendel, 'burger': burger }
default_app = 'mendel'
pbuffer = ''

@post('/<app>/confirm')
def confirm_form(app):
   cid = request.forms['case_id']
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
def login_submit():
    user     = request.forms.get('user')
    password = request.forms.get('password')
    if check_login(user, password):
        params = myapps[default_app].params
        params['app'] = default_app
        params['cid'] = ''
        #params['apps'] = [ myapps.keys() ]
        print params
        tpl = myapps[default_app].appname 
        return template(tpl, params)
    else:
        return "<p>Login failed</p>"

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
def plot(app,cid):
    sim_dir = myapps[app].user_dir + os.sep + cid + os.sep
    if re.search(r'^\s*$', cid):
        return "Error: no case id specified"
    else:
        hst=flot.get_data(sim_dir + cid + '.000.hst',0,1)
        params = { 'cid': cid, 'hst': hst, 'app': app }
        return template('plot', params)

def check_login(user, password):
	if user == login.user and password == login.password:
		return 1
	else:
		return 0

run(host='0.0.0.0', port=8080)
