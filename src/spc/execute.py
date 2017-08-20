from bottle import Bottle, request, template, redirect
import os, re, sys, traceback, cgi
import argparse as ap
from common import rand_cid, slurp_file, replace_tags
from user_data import user_dir
import config
from model import db, apps, jobs, users
import apps_reader_writer as apprw

try:
    import requests
except:
    print "INFO: not importing requests... only needed for remote workers"

routes = Bottle()

def bind(app):
    global root
    root = ap.Namespace(**app)

@routes.post('/confirm')
def confirm_form():
    user = root.authorized()
    app = request.forms.app

    # generate a random case id
    # force the first string to be a letter so that the case id
    # will be guaranteed to be a string
    while True:
        cid = rand_cid()
        run_dir = os.path.join(user_dir, user, app, cid)
        # check if this case exists or not, if it exists generate a new case id
        if not os.path.isdir(run_dir): break

    # pass the case_id to be used by the program input parameters,
    # if case_id is defined in the input deck it will be used
    # otherwise it is ignored
    request.forms['case_id'] = cid
    request.forms['cid'] = cid
    request.forms['user'] = user

    try:
        desc = request.forms['desc']
    except:
        desc = "None"
    desc = desc.replace(',', ', ')

    # set config.submit_type to default value if not set in config.py file
    try:    config.submit_type
    except: config.submit_type = "default"

    if config.submit_type == 'remote':

        request.forms['np'] = 1
        request.forms['desc'] = desc
        request.forms['appmod'] = pickle.dumps(root.myapps[app])

        try:
            print config.remote_worker_url + '/execute'
            resp = requests.post(config.remote_worker_url +'/execute', data=dict(request.forms), verify=False)

        except:
            exc_type, exc_value, exc_traceback = sys.exc_info()
            print traceback.print_exception(exc_type, exc_value, exc_traceback)
            return template('error', err="failed to submit job to SPC worker. " + \
                "Possible solutions: Is a container running? Is Python requests " + \
                "package installed? (pip install requests)")
        else:
            jid = resp.text
            # insert job entry in local DB; scheduler will also insert entry in remote DB
            pry = 1
            uid = users(user=user).id
            db.jobs.insert(uid=uid, app=app, cid=cid, state=jid, description=desc,
                           time_submit=time.asctime(), np=config.np, priority=pry)
            db.commit()
            redirect("/case?app="+app+"&cid="+str(cid)+"&jid="+str(jid))

    elif config.submit_type == 'noverify':
        # "noverify" means don't echo the parameters back to the user before running
        # the simulation.  Just run the simulation when user submits the parameters

        # replace placeholder tags in the command line, e.g. <cid> with appropriate params
        request.forms['rel_apps_path'] = (os.pardir + os.sep)*4 + apprw.apps_dir
        root.myapps[app].write_params(request.forms, user)

        cmd = apps(name=app).command
        cmd = replace_tags(cmd, request.forms)
        outfn = app + ".out"
        cmd = cmd + ' > ' + outfn + ' 2>&1 '
        print "cmd:", cmd
        # following two params are temporary solutions
        np = 1
        walltime = 60
        uid = users(user=user).id
        priority = db(users.user==user).select(users.priority).first().priority
        jid = root.sched.qsub(app, cid, uid, cmd, np, priority, walltime, desc)
        redirect("/case?app="+app+"&cid="+str(cid)+"&jid="+str(jid))

    else:

        run_dir = os.path.join(user_dir, user, root.myapps[app].appname, cid)
        fn = os.path.join(run_dir, root.myapps[app].simfn)

        # this app-specific code should be removed in future
        # this writes a customized forsim script needed to run the simulation
        if app == "forsim":
            inputs = request.forms.script.decode('utf-8')
            inputs = inputs.replace(u'\r\n', '\n')
            if not os.path.exists(run_dir): os.makedirs(run_dir)
            thisfn = os.path.join(run_dir, "input.sim")
            with open(thisfn, 'w') as f: f.write(inputs)

        root.myapps[app].write_params(request.forms, user)

        # read the file
        inputs = slurp_file(fn)

        # convert html tags to entities (e.g. < to &lt;)
        inputs = cgi.escape(inputs)

        # attempt to get number of procs from forms inputs
        if 'num_procs' in request.forms:
            np = request.forms.num_procs
        else:
            np = 1

        params = { 'cid': cid, 'inputs': inputs, 'app': app,
                   'user': user, 'nap': config.np, 'np': np, 'desc': desc }
        # try:
        return template('confirm', params)
        # except:
        #     return 'ERROR: failed to write parameters to file'

@routes.post('/execute')
def execute():
    user = root.authorized()
    app = request.forms.app
    cid = request.forms.cid
    np = int(request.forms.np) or 1
    walltime = request.forms.walltime
    desc = request.forms.desc
    #priority = request.forms.priority
    params = {}
    # base_dir = os.path.join(user_dir, user, app, cid)

    inputs, _, _ = root.myapps[app].read_params(user, cid)
    # in addition to supporting input params, also support case id
    if "cid" not in inputs: inputs["cid"] = cid

    # if preprocess is set run the preprocessor
    # try:
    #     if root.myapps[app].preprocess:
    #         processed_inputs = process.preprocess(inputs,
    #                                    root.myapps[app].preprocess,base_dir)
    # except:
    #     exc_type, exc_value, exc_traceback = sys.exc_info()
    #     print traceback.print_exception(exc_type, exc_value, exc_traceback)
    #     return template('error', err="There was an error with the preprocessor")

    cmd = apps(name=app).command

    # for parallel runs
    if np > 1: cmd = config.mpirun + " -np " + str(np) + " " + cmd

    # this is the relative path to the executable from the case directory where
    # the simulation files are stored
    inputs['rel_apps_path'] = (os.pardir + os.sep)*4 + apprw.apps_dir

    # replace placeholder tags in the command line, e.g. <cid> with appropriate params
    cmd = replace_tags(cmd, inputs)

    outfn = app + ".out"
    cmd = cmd + ' > ' + outfn + ' 2>&1 '
    print "cmd:", cmd

    # submit job to queue
    try:
        params['cid'] = cid
        params['app'] = app
        params['user'] = user
        priority = db(users.user==user).select(users.priority).first().priority
        uid = users(user=user).id
        jid = root.sched.qsub(app, cid, uid, cmd, np, priority, walltime, desc)
        redirect("/case?app="+app+"&cid="+cid+"&jid="+jid)
    except OSError, e:
        exc_type, exc_value, exc_traceback = sys.exc_info()
        print traceback.print_exception(exc_type, exc_value, exc_traceback)
        print >> sys.stderr, "Execution failed:", e
        params = { 'cid': cid, 'app': app, 'user': user, 'err': e }
        return template('error', params)

@routes.get('/<app>/<cid>/tail')
def tail(app, cid):
    user = root.authorized()
    # submit num_lines as form parameter
    num_lines = int(request.query.num_lines) or 24
    progress = 0
    complete = 0
    if config.worker == 'remote':
        myparams = {'user': user, 'app': app, 'cid': cid}
        resp = requests.get(config.remote_worker_url +'/output', params=myparams)
        output = resp.text
        myoutput = output #[len(output)-num_lines:]
        # xoutput = ''.join(myoutput)
        xoutput = myoutput
        ofn = 'remote'
    else:
        run_dir = os.path.join(user_dir, user, root.myapps[app].appname, cid)
        ofn = os.path.join(run_dir, root.myapps[app].outfn)
        if os.path.exists(ofn):
            f = open(ofn,'r')
            output = f.readlines()
            # custom mendel mods for progress bar
            for line in output:
                m = re.search("num_generations\s=\s*(\d+)", line)
                if m:
                    complete = int(m.group(1))
                if complete > 0:
                    m = re.match("generation\s=\s*(\d+)", line)
                    if m: progress = int(float(m.group(1))/float(complete)*100)
            # end mendel mods
            start_position = len(output) - num_lines
            if start_position > 0:
                myoutput = output[start_position:]
            else:
                myoutput = output
            xoutput = ''.join(myoutput)
            f.close()
        elif os.path.exists(os.path.join(run_dir, root.myapps[app].simfn)):
            xoutput = 'waiting to start...'
        else:
            xoutput = 'Oops! It appears that the directory does not exist.  Possibly it has been deleted'

    params = { 'cid': cid, 'contents': xoutput, 'app': app,
               'user': user, 'fn': ofn, 'progress': progress }
    return template('more_contents', params)
