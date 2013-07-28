from bottle import route, template, static_file, view
from bottle import get, post, request, run
from subprocess import call
#run(reloader=True)
import config

@post('/confirm')
def confirm_form():
   if(config.write_params(request.forms)):
      #return template('wrote parameters to file: {{fn}}',fn=config.sim_conf_file)
      return template('execute', config.exe)
   else:
      return template('failed to write parameters to file: {{fn}}',fn=config.sim_conf_file)

@post('/execute')
def execute():
   call(config.sim_exe_path)
   
@route('/')
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

