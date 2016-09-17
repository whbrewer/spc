from bottle import Bottle, template, static_file, request, redirect, app, get, post, run
import config, cgi, os
from os import listdir
import scheduler_sp
import pickle, re
from model import *
from common import *

sched = scheduler_sp.Scheduler()

@get('/')
def root(): return "hello this is an SPC worker node"

@get('/query')
def query(): pass

@post('/stop')
def stop(): pass

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
        return str(jid)
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
        run_dir = os.path.join(config.user_dir, u, app, c)
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
    base_dir = os.path.join(config.user_dir, user, app)
    path = os.path.join(base_dir, cid+".zip")
    print "path is:", path
    zf = zipfile.ZipFile(path, mode='w')
    sim_dir = os.path.join(base_dir, cid)
    for fn in os.listdir(sim_dir):
        zf.write(os.path.join(sim_dir, fn))
    zf.close()
    # status="<a href=\""+path+"\">"+path+"</a>"
    # redirect("/aws?status="+status)
    return "OK"


@get('/user_data/<filepath:path>')
def user_data(filepath):
    return static_file(filepath, root='user_data')

if __name__ == "__main__":
    sched.poll()
    # run the app
    try:
        run(server=config.server, app=app, host='0.0.0.0', \
            port=config.port, debug=False)
    except:
        # run(app=app, host='0.0.0.0', port=config.port, debug=False)
        run(host='0.0.0.0', port=config.port+1, debug=True)
