from bottle import route, template, static_file, view
from bottle import get, post, request, run
#from subprocess import call
import subprocess
import string, random
import sys, os, re
#import mendel, flot
import flot
#from apps import app_f90
import apps
import login
#from gevent import monkey; monkey.patch_all()

mendel = apps.app_f90('mendel')
burger = apps.app_f90('burger')
myapps = { 'mendel': mendel, 'burger': burger }
default_app = 'mendel'

@post('/confirm')
def confirm_form():
   app = request.forms['app']
   params = {'cid': request.forms['case_id'], 'app': app }
   #my_dict = request.query.decode()
   #print my_dict

   if(mendel.write_params(request.forms)):
   #if(myapps[app].write_params(request.forms)):
      return template('confirm', params)
   else:
      return 'ERROR: failed to write parameters to file'

@post('/execute')
def execute():
    # student - need to use popen here and repeatedly read from the pipe and display
    cid = request.forms['cid']
    app = request.forms['app']
    try:
        cmd = os.pardir + os.sep + os.pardir + os.sep + mendel.exe
        #retcode = call(cmd)
        #run_dir = myapps[app].user_dir + os.sep + cid 
        run_dir = mendel.user_dir + os.sep + cid 
        print run_dir
        p = subprocess.Popen([cmd], cwd=run_dir, shell=True, stdout=subprocess.PIPE)
        while p.poll() is None:
            output = p.stdout.readline()
            #yield output
            print output,
        p.wait()
        #if retcode < 0:
        #    print >>sys.stderr, "Child was terminated by signal", -retcode
        #    return template('job terminated by signal: {{x}}', x=-retcode)
        #else:
        #    print >>sys.stderr, "Child returned", retcode
        params = dict()
        params['cid'] = cid
        return template('output',params)

    except OSError, e:
        print >>sys.stderr, "Execution failed:", e
        return "ERROR: failed to start job"
   
@route('/')
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
        #mendel.params['user'] = user
        # ignore blockmap and blockorder from read_params()
        params = mendel.params
        params['cid'] = ''
        params['app'] = myapps[default_app]
        return template('start', params)
    else:
        return "<p>Login failed</p>"

@post('/start')
def start():
    # ignore blockmap and blockorder from read_params()
    cid = request.forms['cid']
    app = request.forms['app']
    if cid is '':
        params = myapps[app].params
    else:
        params,_,_ = myapps[app].read_params(cid)
    params['cid'] = cid
    params['app'] = app
    return template('start', params)

@post('/list')
def list():
    str = ''
    cid = request.forms['cid']
    for case in os.listdir(mendel.user_dir):
        str += '<a onclick="set_cid(\'' + case + '\')">' + case + '</a><br>\n'
    content = { 'content': str }
    content['cid'] = cid
    return template('list', content)

@post('/plot')
def plot():
    cid = request.forms['cid']
    sim_dir = mendel.user_dir + os.sep + cid + os.sep
    if re.search(r'^\s*$', cid):
        return "Error: no case id specified"
    else:
        hst=flot.get_data(sim_dir + cid + '.000.hst',0,1)
        params = { 'cid': cid, 'hst': hst }
        return template('plot', params)

def check_login(user, password):
	if user == login.user and password == login.password:
		return 1
	else:
		return 0

run(host='localhost', port=8080)
#run(host='localhost', port=8080, server='gevent')

