# This is an SSL worker for submitting jobs remotely.

from flask import Flask, make_response, request, send_from_directory
from werkzeug.datastructures import MultiDict
from OpenSSL import SSL
import html
import os
import pickle
import re

try:
    from cherrypy import wsgiserver
    from cherrypy.wsgiserver.ssl_pyopenssl import pyOpenSSLAdapter
except ImportError:
    from cheroot import wsgi as wsgiserver
    from cheroot.ssl.pyopenssl import pyOpenSSLAdapter

from . import process
from . import scheduler
from .common import slurp_file
from .model import db, jobs, users
from .request_shim import RequestShim
from .templating import template
from .user_data import user_dir

ssl_cert = "/etc/apache2/ssl/ssl.crt"
ssl_key = "/etc/apache2/ssl/private.key"

app = Flask(__name__)
sched = scheduler.Scheduler()


@app.before_request
def inject_request_shims():
    req = request._get_current_object()
    req.forms = RequestShim(MultiDict(request.form))
    req.query = RequestShim(MultiDict(request.args))


@app.get('/')
def root():
    return "hello this is an SPC worker node"


@app.get('/delete')
def del_job():
    jid = request.query.jid
    sched.stop(jid)
    sched.qdel(jid)
    return "OK"


@app.get('/stop')
def stop():
    jid = request.query.jid
    sched.stop(jid)
    return "OK"


@app.get('/status/<jid>')
def get_status(jid):
    row = db(jobs.id==jid).select(jobs.state).first()
    if row is None:
        return 'X'
    return row.state


@app.get('/listfiles')
def listfiles():
    appname = request.forms['app']
    user = request.forms['user']
    cid = request.forms['cid']
    mypath = os.path.join(user_dir, user, appname, cid)
    return os.listdir(mypath)


@app.post('/execute')
def execute():
    appname = request.forms['app']
    user = request.forms['user']
    cid = request.forms['cid']
    desc = request.forms['desc']
    np = request.forms['np']
    appmod_payload = request.forms['appmod']
    if isinstance(appmod_payload, str):
        appmod_payload = appmod_payload.encode('latin1')
    appmod = pickle.loads(appmod_payload)
    del request.forms['appmod']
    appmod.write_params(request.forms, user)

    try:
        if appmod.preprocess:
            run_params, _, _ = appmod.read_params(user, cid)
            base_dir = os.path.join(user_dir, user, appname)
            process.preprocess(run_params, appmod.preprocess, base_dir)
        if appmod.preprocess == "terra.in":
            appmod.outfn = "out" + run_params['casenum'] + ".00"
    except Exception:
        return template('error', err="There was an error with the preprocessor")

    try:
        priority = db(users.user==user).select(users.priority).first().priority
        uid = users(user=user).id
        jid = sched.qsub(appname, cid, uid, np, priority, desc)
        return str(jid)
    except OSError:
        return "ERROR: a problem occurred"


@app.get('/output')
def output():
    resp = make_response()
    resp.headers['Access-Control-Allow-Origin'] = '*'
    resp.headers['Access-Control-Allow-Methods'] = 'PUT, GET, POST, DELETE, OPTIONS'
    resp.headers['Access-Control-Allow-Headers'] = 'Origin, Accept, Content-Type, X-Requested-With, X-CSRF-Token'

    appname = request.query.app
    cid = request.query.cid
    user = request.query.user

    try:
        if re.search("/", cid):
            (u, c) = cid.split("/")
        else:
            u = user
            c = cid
        run_dir = os.path.join(user_dir, u, appname, c)
        fn = os.path.join(run_dir, appname + '.out')
        output_text = slurp_file(fn)
        output_text = html.escape(output_text)
        resp.set_data(output_text)
        return resp
    except Exception:
        resp.set_data("ERROR: something went wrong!")
        return resp


@app.get('/zipcase')
def zipcase():
    import zipfile
    appname = request.query.app
    cid = request.query.cid
    user = request.query.user
    base_dir = os.path.join(user_dir, user, appname)
    path = os.path.join(base_dir, cid + ".zip")

    zf = zipfile.ZipFile(path, mode='w')
    sim_dir = os.path.join(base_dir, cid)
    for fn in os.listdir(sim_dir):
        zf.write(os.path.join(sim_dir, fn))
    zf.close()

    return "OK"


@app.get('/user_data/<path:filepath>')
def user_data(filepath):
    return send_from_directory('user_data', filepath)


class SecuredSSLServer(object):
    def __init__(self, cert, key):
        self._adapter = pyOpenSSLAdapter(cert, key)

    def __getattr__(self, name):
        return getattr(self._adapter, name)

    def get_context(self):
        c = self._adapter.get_context()
        c.set_options(SSL.OP_NO_SSLv2)
        c.set_options(SSL.OP_NO_SSLv3)
        c.set_options(SSL.OP_NO_TLSv1)
        c.set_options(SSL.OP_NO_TLSv1_1)
        return c


def main():
    sched.poll()
    try:
        server = wsgiserver.CherryPyWSGIServer(('0.0.0.0', 8581), app)
    except AttributeError:
        server = wsgiserver.Server(('0.0.0.0', 8581), app)
    server.ssl_adapter = SecuredSSLServer(ssl_cert, ssl_key)
    try:
        server.start()
    finally:
        server.stop()
