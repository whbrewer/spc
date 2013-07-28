from bottle import route, template, static_file, view
from bottle import get, post, request
from bottle import run
#run(reloader=True)
import config
print "sim_config_file: " + config.sim_conf_file
sim_conf_file = 'mendel.in'

@route('/start/<cid>')
def index(cid='test00'):
	return template('<b>Hello {{cid}}</b>!', cid=cid)
@route('/static/<filename>')
def server_static(filename):
	return static_file(filename, root='./views')

@post('/confirm')
def confirm_form():
   user = request.forms.get('user')
   cid = request.forms.get('cid')
   mutn_rate = request.forms.get('mutn_rate')  
   frac_fav_mutn = request.forms.get('frac_fav_mutn')
   reproductive_rate = request.forms.get('reproductive_rate')
   pop_size = request.forms.get('pop_size')
   num_generations = request.forms.get('num_generations')
   f = open(config.sim_conf_file, 'w')
   f.write('case_id: %s' % cid) 
   f.close
	
@get('/login')
def login_form():
    return '''<form method="POST" action="/login">
                <input name="user"     type="text" />
                <input name="password" type="password" />
                <input type="submit" />
              </form>'''

@post('/login')
def login_submit():
    user     = request.forms.get('user')
    password = request.forms.get('password')
    if check_login(user, password):
        config.params['user'] = user
        return template('start', config.params)
    else:
        return "<p>Login failed</p>"

def check_login(user, password):
	if user == config.user and password == config.password:
		return 1
	else:
		return 0

run(host='localhost', port=8080)

