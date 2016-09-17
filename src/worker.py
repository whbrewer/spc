from bottle import Bottle, template, static_file, request, redirect, app, get, post, run
import config, cgi, os
import scheduler_sp
import pickle
from model import *

sched = scheduler_sp.Scheduler()

@get('/')
def root(): return "hello this is an SPC worker node"

@get('/query')
def query(): pass

@post('/stop')
def stop(): pass

@post('/execute')
def execute():
    app = request.forms['app']
    user = request.forms['user']
    cid = request.forms['cid']
    desc = request.forms['desc']
    appmod = pickle.loads(request.forms['appmod'])
    # remove the appmod key
    del request.forms['appmod']
    print request.forms
    
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
        jid = sched.qsub(app, cid, uid, config.np, priority, desc)
        return jid
        #redirect("http://localhost:"+str(config.port)+"/case?app="+str(app)+"&cid="+str(cid)+"&jid="+str(jid))
    except OSError, e:
        return "ERROR: a problem occurred"

@get('/output')
def output():
    app = request.query.app
    cid = request.query.cid
    user = request.query.user
    
    try:
        if re.search("/", cid):
            (u, c) = cid.split("/")
        else:
            u = user
            c = cid
        run_dir = os.path.join(myapps[app].user_dir, u, myapps[app].appname, c)
        fn = os.path.join(run_dir, myapps[app].outfn)
        output = slurp_file(fn)
        # the following line will convert HTML chars like > to entities &gt;
        # this is needed so that XML input files will show paramters labels
        output = cgi.escape(output)
        params = { 'cid': cid, 'contents': output, 'app': app,
                   'user': u, 'fn': fn, 'apps': myapps.keys() }
        return template('more', params)
    except:
        params = { 'app': app, 'apps': myapps.keys(),
                   'err': "Couldn't read input file. Check casename." }
        return template('error', params)

if __name__ == "__main__":
    sched.poll()
    # run the app
    try:
        run(server=config.server, app=app, host='0.0.0.0', \
            port=config.port, debug=False)
    except:
        # run(app=app, host='0.0.0.0', port=config.port, debug=False)
        run(host='0.0.0.0', port=config.port+1, debug=True)
