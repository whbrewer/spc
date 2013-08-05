from bottle import route, template, static_file, view
from bottle import get, post, request, run
#from subprocess import call
import subprocess
import string, random
import sys, os, re
import config, flot

@post('/confirm')
def confirm_form():
   params = {'cid': request.forms['case_id'] }
   if(config.write_params(request.forms)):
      return template('confirm', params)
   else:
      return 'ERROR: failed to write parameters to file'

@post('/execute')
def execute():
    # student - need to use popen here and repeatedly read from the pipe and display
    cid = request.forms['cid']
    try:
        cmd = os.pardir + os.sep + os.pardir + os.sep + config.sim_exe
        #retcode = call(cmd)
        run_dir = config.sim_user_dir + os.sep + cid 
        print run_dir
        p = subprocess.Popen([cmd], cwd=run_dir, shell=True, stdout=subprocess.PIPE)
        f = open('tmp.out','w')
        while p.poll() is None:
            output = p.stdout.readline()
            #print output,
        f.close()
        p.wait()
        #if retcode < 0:
        #    print >>sys.stderr, "Child was terminated by signal", -retcode
        #    return template('job terminated by signal: {{x}}', x=-retcode)
        #else:
        #    print >>sys.stderr, "Child returned", retcode
        return template('output')

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
        #config.params['user'] = user
        # ignore blockmap and blockorder from read_params()
        params,_,_ = config.read_params()
        return template('start', params)
    else:
        return "<p>Login failed</p>"

@get('/start')
def start():
    # ignore blockmap and blockorder from read_params()
    params,_,_ = config.read_params()
    return template('start', params)

@get('/list')
def list():
    # ignore blockmap and blockorder from read_params()
    #for x in range(6): cid += random.choice(string.letters)
    #params = { 'filename': cid }
    #f = open('static/tmp/'+cid, 'w')
    fn = 'views/listing.tpl'
    f = open(fn, 'w')
    listing = os.listdir(config.sim_user_dir)
    #print listing
    #params = { 'listing': listing }
    #f.write('<br>\n'.join(os.listdir(config.sim_user_dir)))
    for case in listing: #os.listdir(config.sim_user_dir):
        f.write('<a onclick="set_cid(\'' + case + '\')">' + case + '</a><br>\n')
    f.close()
    return template('list')

@post('/plot')
def plot():
    cid = request.forms['cid']
    sim_dir = config.sim_user_dir + os.sep + cid + os.sep
    if re.search(r'^\s*$', cid):
        return "Error: no case id specified"
    else:
        hst=flot.get_data(sim_dir + cid + '.000.hst',0,1)
        params = { 'cid': cid, 'hst': hst }
        return template('plot', params)

def check_login(user, password):
	if user == config.user and password == config.password:
		return 1
	else:
		return 0

run(host='localhost', port=8080)

