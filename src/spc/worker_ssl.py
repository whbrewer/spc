# This is an SSL worker for submitting jobs remotely
# with some code borrowed from:
# https://github.com/nickbabcock/bottle-ssl/blob/master/main.py

# to use this must install the following package using apt-get or yum:
#   python-dev
#   libssl-dev
#   libffi-dev

# Also, must install the following using pip or easy_install:
#   cherrypy
#   pyOpenSSL

from bottle import Bottle, template, static_file, request, redirect, response, app, get, post, run, ServerAdapter
from cherrypy import wsgiserver
from cherrypy.wsgiserver.ssl_pyopenssl import pyOpenSSLAdapter
from OpenSSL import SSL

import config, cgi, os
from os import listdir
import scheduler_sp
import pickle, re
from model import *
from common import *
from user_data import user_dir

ssl_cert = "/etc/apache2/ssl/ssl.crt"
ssl_key = "/etc/apache2/ssl/private.key"

sched = scheduler_sp.Scheduler()

@get('/')
def root(): return "hello this is an SPC worker node"

@get('/delete')
def del_job():
    # jid = request.forms['jid']
    jid = request.query.jid
    sched.stop(jid)
    sched.qdel(jid)
    return "OK"

@get('/stop')
def stop():
    # jid = request.forms['jid']
    jid = request.query.jid
    sched.stop(jid)
    return "OK"

@get('/status/<jid>')
def get_status(jid):
    resp = db(jobs.id==jid).select(jobs.state).first()
    if resp is None: return 'X'
    else: return resp.state

@get('/listfiles')
def listfiles():
    app = request.forms['app']
    user = request.forms['user']
    cid = request.forms['cid']
    return listdir(mypath)

@post('/execute')
def execute():
    app = request.forms['app']
    user = request.forms['user']
    cid = request.forms['cid']
    desc = request.forms['desc']
    np = request.forms['np']
    appmod = pickle.loads(request.forms['appmod'])
    # remove the appmod key
    del request.forms['appmod']

    appmod.write_params(request.forms, user)

    # if preprocess is set run the preprocessor
    try:
        if appmod.preprocess:
            run_params, _, _ = appmod.read_params(user, cid)
            processed_inputs = process.preprocess(run_params, appmod.preprocess, base_dir)
        if appmod.preprocess == "terra.in":
            appmod.outfn = "out"+run_params['casenum']+".00"
    except:
        return template('error', err="There was an error with the preprocessor")

    # submit job to queue
    try:
        priority = db(users.user==user).select(users.priority).first().priority
        uid = users(user=user).id
        jid = sched.qsub(app, cid, uid, np, priority, desc)
        return str(jid)
        #redirect("http://localhost:"+str(config.port)+"/case?app="+str(app)+"&cid="+str(cid)+"&jid="+str(jid))
    except OSError, e:
        return "ERROR: a problem occurred"

@get('/output')
def output():
    response.headers['Access-Control-Allow-Origin'] = '*'
    response.headers['Access-Control-Allow-Methods'] = 'PUT, GET, POST, DELETE, OPTIONS'
    response.headers['Access-Control-Allow-Headers'] = 'Origin, Accept, Content-Type, X-Requested-With, X-CSRF-Token'

    app = request.query.app
    cid = request.query.cid
    user = request.query.user

    try:
        if re.search("/", cid):
            (u, c) = cid.split("/")
        else:
            u = user
            c = cid
        run_dir = os.path.join(user_dir, u, app, c)
        fn = os.path.join(run_dir, app + '.out')
        output = slurp_file(fn)
        # the following line will convert HTML chars like > to entities &gt;
        # this is needed so that XML input files will show paramters labels
        output = cgi.escape(output)
        return output
        # params = { 'cid': cid, 'contents': output, 'app': app,
        #            'user': u, 'fn': fn, 'apps': myapps.keys() }
        # return template('more', params)
    except:
        return "ERROR: something went wrong!"
        # params = { 'app': app, 'apps': myapps.keys(),
        #            'err': "Couldn't read input file. Check casename." }
        # return template('error', params)

@get('/zipcase')
def zipcase():
    """zip case on machine to prepare for download"""
    import zipfile
    app = request.query.app
    cid = request.query.cid
    user = request.query.user
    base_dir = os.path.join(user_dir, user, app)
    path = os.path.join(base_dir, cid+".zip")

    zf = zipfile.ZipFile(path, mode='w')
    sim_dir = os.path.join(base_dir, cid)
    for fn in os.listdir(sim_dir):
        zf.write(os.path.join(sim_dir, fn))
    zf.close()

    return "OK"


@get('/user_data/<filepath:path>')
def user_data(filepath):
    return static_file(filepath, root='user_data')

# By default, the server will allow negotiations with extremely old protocols
# that are susceptible to attacks, so we only allow TLSv1.2
class SecuredSSLServer(pyOpenSSLAdapter):
    def get_context(self):
        c = super(SecuredSSLServer, self).get_context()
        c.set_options(SSL.OP_NO_SSLv2)
        c.set_options(SSL.OP_NO_SSLv3)
        c.set_options(SSL.OP_NO_TLSv1)
        c.set_options(SSL.OP_NO_TLSv1_1)
        return c

# Create our own sub-class of Bottle's ServerAdapter
# so that we can specify SSL. Using just server='cherrypy'
# uses the default cherrypy server, which doesn't use SSL
class SSLCherryPyServer(ServerAdapter):
    def run(self, handler):
        server = wsgiserver.CherryPyWSGIServer((self.host, self.port), handler)
        server.ssl_adapter = SecuredSSLServer(ssl_cert, ssl_key)
        try:
            server.start()
        finally:
            server.stop()

if __name__ == "__main__":
    sched.poll()
    ## run(server='cherrypy', host='0.0.0.0', port=config.port+1, debug=False)
    run(host='0.0.0.0', port=8581, server=SSLCherryPyServer)
