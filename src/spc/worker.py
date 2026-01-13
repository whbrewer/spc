from flask import Flask, make_response, request, send_from_directory
from werkzeug.datastructures import MultiDict
from os import listdir
import html
import os
import pickle
import re

from . import config
from . import process
from . import scheduler
from .common import slurp_file
from .model import db, jobs, users
from .request_shim import RequestShim
from .templating import template
from .user_data import user_data_root

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
    resp = make_response()
    resp.headers['Access-Control-Allow-Origin'] = '*'
    resp.headers['Access-Control-Allow-Methods'] = 'GET, POST, PUT, OPTIONS'
    resp.headers['Access-Control-Allow-Headers'] = 'Origin, Accept, Content-Type, X-Requested-With, X-CSRF-Token'
    row = db(jobs.id==jid).select(jobs.state).first()
    if row is None:
        resp.set_data('X')
    else:
        resp.set_data(row.state)
    return resp


@app.get('/listfiles')
def listfiles():
    appname = request.forms['app']
    user = request.forms['user']
    cid = request.forms['cid']
    mypath = os.path.join(user_data_root, user, appname, cid)
    return listdir(mypath)


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
            base_dir = os.path.join(user_data_root, user, appname)
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
        run_dir = os.path.join(user_data_root, u, appname, c)
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
    base_dir = os.path.join(user_data_root, user, appname)
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


def main():
    sched.poll()
    app.run(host='0.0.0.0', port=config.port + 1, debug=False)
