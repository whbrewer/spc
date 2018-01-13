from bottle import Bottle, request, template, redirect
import os, sys, re, traceback, shutil, time, argparse as ap, zipfile
from datetime import datetime, timedelta

from user_data import user_dir
from common import rand_cid, replace_tags, slurp_file
from model import db, users, jobs
import config
import migrate

routes = Bottle()

def bind(app):
    global root
    root = ap.Namespace(**app)

@routes.get('/jobs')
def show_jobs():
    user = root.authorized()
    #if app not in root.myapps: redirect('/apps')
    cid = request.query.cid
    app = request.query.app or root.active_app()
    n = int(request.query.n or config.jobs_num_rows)
    q = request.query.q
    starred = request.query.starred
    shared = request.query.shared
    uid = users(user=user).id

    if starred:
        result = db((jobs.uid==uid) & (jobs.starred=="True")).select(orderby=~jobs.id)[:n]
    elif shared:
        result = db(jobs.shared=="True").select(orderby=~jobs.id)[:n]
    elif q:
        query_array = [ tuple(qa.strip().split(":")) for qa in q.strip().split() ]

        if len(query_array) == 1:

            if len(query_array[0]) == 1: # for general case search 3 main fields: cid, app, labels
                result = db((jobs.uid==uid) & \
                           ((db.jobs.cid.contains(q.encode('utf8'), case_sensitive=False)) |
                            (db.jobs.app.contains(q.encode('utf8'), case_sensitive=False)) |
                            (db.jobs.description.contains(q.encode('utf8'), case_sensitive=False)))).select(orderby=~jobs.id)

            else: # in the case of specific tag searching, e.g. app:mendel
                key = query_array[0][0]
                query = query_array[0][1]

                if key == "user" and user == "admin":
                    if query == "all":
                        result = db().select(jobs.ALL, orderby=~jobs.id)[:n]
                    else:
                        this_id = users(user=query).id
                        result = db(jobs.uid==this_id).select(orderby=~jobs.id)[:n]
                        for i, r in enumerate(result):
                            result[i]['cid'] = query + "/" + result[i]['cid']
                elif key == "cid":
                    result = db((jobs.uid==uid) & \
                        (db.jobs.cid.contains(query, case_sensitive=False))).select(orderby=~jobs.id)
                elif key == "app":
                    result = db((jobs.uid==uid) & (jobs.app==query)).select(orderby=~jobs.id)
                elif key =="np":
                    result = db((jobs.uid==uid) & (jobs.np==query)).select(orderby=~jobs.id)
                elif key == "is":
                    if query == "starred":
                        result = db((jobs.uid==uid) & (jobs.starred=="True")).select(
                                 orderby=~jobs.id)[:n]
                    elif query == "shared":
                        result = db(jobs.shared=="True").select(orderby=~jobs.id)[:n]
                elif key == "state":
                    result = db((jobs.uid==uid) & (db.jobs.state==query)).select(orderby=~jobs.id)
                elif key == "label":
                    result = db((db.jobs.uid==uid) & (db.jobs.description.contains(
                                 query, case_sensitive=False))).select(orderby=~jobs.id)
                elif key == "after" or key == "before":
                    if len(query) != 8:
                        return template('error', err="date format must be YY/MM/DD, e.g. after:16/12/01")
                    rows = db(jobs.uid==uid).select(orderby=~jobs.id)
                    result = []
                    for row in rows:
                        a = datetime.strptime(row.time_submit, "%a %b %d %H:%M:%S %Y")
                        b = datetime.strptime(query, "%y/%m/%d")
                        if key == "after":
                            if a-b > timedelta(days=0): result.append(row)
                        else:
                            if a-b < timedelta(days=0): result.append(row)
                else:
                    return template('error', err="search key not supported: "+key)

        elif len(query_array) == 2: # the case when user search with both after and before dates
            key1, query1 = query_array[0][0], query_array[0][1]
            key2, query2 = query_array[1][0], query_array[1][1]
            if len(query1) != 8 or len(query2) != 8:
                return template('error', err="date format must be YY/MM/DD, e.g. after:16/12/01")
            if key1 == "after" and key2 == "before" or key1 == "before" and key2 == "after":
                rows = db(jobs.uid==uid).select(orderby=~jobs.id)
                result = []
                for row in rows:
                    a = datetime.strptime(row.time_submit, "%a %b %d %H:%M:%S %Y")
                    b = datetime.strptime(query1, "%y/%m/%d")
                    c = datetime.strptime(query2, "%y/%m/%d")
                    if key1 == "after":
                        if a-b > timedelta(days=0) and a-c < timedelta(days=0): result.append(row)
                    else:
                        if a-c > timedelta(days=0) and a-b < timedelta(days=0): result.append(row)
            else:
                return template('error', err="search type not supported")

        else:
            return template('error', err="search type not supported")
    else:
        result = db(jobs.uid==uid).select(orderby=~jobs.id)[:n]

    # number of jobs in queued state
    params = {}
    params['q'] = q
    params['cid'] = cid
    params['app'] = app
    params['user'] = user
    params['np'] = config.np
    params['n'] = n
    params['status'] = "showing " + str(len(result)) + " cases"
    params['num_rows'] = config.jobs_num_rows
    return template('jobs', params, rows=result)

@routes.get('/jobs/new')
def start_new_job():
    user = root.authorized()
    app = request.query.app or root.active_app()

    if app: root.set_active(app)
    else: redirect('/myapps')

    if config.auth and not root.authorized(): redirect('/login')

    if app not in root.myapps: redirect('/apps')

    cid = request.query.cid
    if re.search("/", cid):
        owner, cid = cid.split("/")
    else:
        owner = user

    # read default params... this ensures no 500 error when restarting
    # in case params are missing
    params = {}
    params.update(root.myapps[app].params)
    # pass by value not by reference to avoid apps templates modifying
    # the myapps dictionary

    # if restarting from old case
    if re.search("[a-z]", cid):
        params, _, _ = root.myapps[app].read_params(owner, cid)
        if user == owner:
            params['tags'] = cid
        else:
            params['tags'] = os.path.join(owner, cid)

    params['cid'] = cid
    params['app'] = app
    params['user'] = user
    params['apps'] = root.myapps
    try:
        return template('apps/' + root.myapps[app].appname, params)
    except:
        exc_type, exc_value, exc_traceback = sys.exc_info()
        print traceback.print_exception(exc_type, exc_value, exc_traceback)
        return template('error', err="there was a problem with the template. Check traceback.")

@routes.get('/jobs/diff')
def diff_jobs():
    user = root.authorized()
    app = root.active_app()

    selected_cases = request.query.selected_diff_cases
    cases = selected_cases.rstrip(':').split(':')

    cids = list()
    contents = list()
    for jid in cases:
        cid = jobs(jid).cid
        cids.append(cid)
        app = jobs(jid).app
        base_dir = os.path.join(user_dir, user, root.myapps[app].appname)
        fn = os.path.join(base_dir, cid, root.myapps[app].simfn)
        content = slurp_file(fn).splitlines(1)
        contents.append(content)

    import difflib
    d = difflib.Differ()
    result = list(d.compare(contents[0], contents[1]))
    title = "diff " + cids[0] + " " + cids[1]

    params = { 'cid': cid, 'contents': ' '.join(result), 'app': app, 'user': user, 'fn': title }
    return template('more', params)

@routes.post('/jobs/annotate')
def annotate_job():
    root.authorized()
    cid = request.forms.cid
    # jid = request.forms.jid
    desc = request.forms.description
    desc = desc.replace(',', ', ')
    jobs(cid=cid).update_record(description=desc)
    db.commit()
    redirect('/jobs')

@routes.post('/jobs/star')
def star_case():
    root.authorized()
    jid = request.forms.jid
    jobs(id=jid).update_record(starred="True")
    db.commit()
    redirect('/jobs')

@routes.post('/jobs/unstar')
def unstar_case():
    root.authorized()
    jid = request.forms.jid
    jobs(id=jid).update_record(starred="False")
    db.commit()
    redirect('/jobs')

@routes.post('/jobs/share')
def share_case():
    root.authorized()
    jid = request.forms.jid
    jobs(id=jid).update_record(shared="True")
    db.commit()
    # increase count in database for every user
    for u in db().select(users.ALL):
        nmsg = users(user=u.user).new_shared_jobs or 0
        users(user=u.user).update_record(new_shared_jobs=nmsg+1)
    db.commit()
    redirect('/jobs')

@routes.post('/jobs/unshare')
def unshare_case():
    root.authorized()
    jid = request.forms.jid
    jobs(id=jid).update_record(shared="False")
    db.commit()
    redirect('/jobs')

@routes.get('/jobs/all')
def get_all_jobs():
    user = root.authorized()
    if not user == "admin":
        return template("error", err="must be admin to use this feature")
    cid = request.query.cid
    app = request.query.app or root.active_app()
    n = request.query.n
    if not n:
        n = config.jobs_num_rows
    else:
        n = int(n)
    # sort by descending order of jobs.id
    result = db((db.jobs.uid==users.id)).select(orderby=~jobs.id)[:n]

    # clear notifications
    users(user=user).update_record(new_shared_jobs=0)
    db.commit()

    params = {}
    params['cid'] = cid
    params['app'] = app
    params['user'] = user
    params['n'] = n
    params['num_rows'] = config.jobs_num_rows
    return template('shared', params, rows=result)

@routes.get('/jobs/shared')
def get_shared():
    """Return the records from the shared table."""
    user = root.authorized()
    cid = request.query.cid
    app = request.query.app or root.active_app()
    n = request.query.n
    if not n:
        n = config.jobs_num_rows
    else:
        n = int(n)
    # sort by descending order of jobs.id
    result = db((db.jobs.shared=="True") & (db.jobs.uid==users.id)).select(orderby=~jobs.id)[:n]
    # result = db((db.jobs.shared=="True") &
    #             (jobs.gid == users.gid)).select(orderby=~jobs.id)[:n]

    # clear notifications
    users(user=user).update_record(new_shared_jobs=0)
    db.commit()

    params = {}
    params['cid'] = cid
    params['app'] = app
    params['user'] = user
    params['n'] = n
    params['num_rows'] = config.jobs_num_rows
    return template('shared', params, rows=result)

@routes.post('/jobs/delete/<jid>')
def delete_job(jid):
    user = root.authorized()
    app = request.forms.app
    cid = request.forms.cid
    state = jobs(jid).state

    if re.search("/", cid):
        return template("error", err="only possible to delete cases that you own")

    if state != "R":
        path = os.path.join(user_dir, user, app, cid)
        if os.path.isdir(path): shutil.rmtree(path)
        root.sched.stop(jid)
        root.sched.qdel(jid)
    else:
        return template("error", err="cannot delete while job is still running")
    redirect("/jobs")

@routes.post('/jobs/merge/<rtype>')
def merge(rtype):
    user = root.authorized()
    selected_cases = request.forms.selected_merge_cases
    jids = selected_cases.rstrip(':').split(':')
    cases = list()
    output = dict()

    for jid in jids:
        app = jobs(id=jid).app
        cid = jobs(id=jid).cid
        cases.append(cid)
        fn = replace_tags(request.forms.file_pattern, {'cid': cid})
        path = os.path.join(user_dir, user, app, cid, fn)

        with open(path, "r") as infile:
            # Loop over lines in each file
            for line in infile:
                line = str(line)
                # Skip comment lines
                if not re.search('^#', line):
                    items = line.split()
                    # If a line matching this one has been encountered in a previous
                    # file, add the column values
                    if len(items) > 0:
                        currkey = int(items[0])
                        if currkey in output.keys():
                            for ii in range(len(output[currkey])):
                                output[currkey][ii] += float(items[ii+1])
                        # Otherwise, add a new key to the output and create the columns
                        else:
                            output[currkey] = list(map(float, items[1:]))

    # Get total number of files for calculating average
    if rtype == "sum":
       nfile = 1
    elif rtype == "avg":
       nfile = len(cases)
    else:
       raise ValueError(rtype + " operation no supported")
    print "nfile:", nfile, selected_cases

    # generate new case_id for outputtinging merged files
    while True:
        ocid = rand_cid()
        run_dir = os.path.join(user_dir, user, app, ocid)
        # check if this case exists or not, if it exists generate a new case id
        if not os.path.exists(run_dir):
            os.makedirs(run_dir)
            break

    # write a default input file b/c SPC requires a file in each job dir
    root.myapps[app].params['case_id'] = ocid
    root.myapps[app].write_params(root.myapps[app].params, user)

    # Sort the output keys
    skey = sorted(output.keys())
    lines = list()
    # Loop through sorted keys and print each averaged column to stdout
    for key in skey:
        outline = str(int(key))
        for item in output[key]:
            outline += ' ' + str("{0:.3e}".format(item/nfile,3))
        lines.append(outline)

    ofn = replace_tags(request.forms.file_pattern, {'cid': ocid})
    with open(os.path.join(run_dir, ofn), 'w') as f:
        f.writelines("%s\n" % l for l in lines)

    # save case to DB
    uid = users(user=user).id
    desc = "merge " + rtype + " cases " + str(cases)
    db.jobs.insert(uid=uid, app=app, cid=ocid, state='C', description=desc,
                   time_submit=time.asctime(), np=config.np, priority=1)
    db.commit()

    return "merged file written to " + run_dir + "<meta http-equiv='refresh' content='2; url=/jobs'>"

@routes.post('/jobs/delete_selected_cases')
def delete_jobs():
    user = root.authorized()
    selected_cases = request.forms.selected_cases
    cases = selected_cases.rstrip(':').split(':')
    # in case someone selected elements twice, get unique cases
    cases = list(set(cases))
    for jid in cases:
        cid = jobs(id=jid).cid
        app = jobs(id=jid).app
        path = os.path.join(user_dir, user, app, cid)
        if cid is not None:
            print "removing path:", path
            if os.path.isdir(path): shutil.rmtree(path)
            root.sched.stop(jid)
            root.sched.qdel(jid)
        else:
            print "ERROR: not removing path:", path, "because cid missing"
    redirect("/jobs")

@routes.post('/jobs/stop')
def stop_job():
    root.authorized()
    app = request.forms.app
    cid = request.forms.cid
    jid = request.forms.jid

    if re.search("/", cid):
        return template("error", err="only possible to stop cases that you own")

    root.sched.stop(jid)
    time.sleep(0.1)
    jobs(jid).update_record(state="X")
    db.commit()
    redirect("/case?app="+app+"&cid="+cid+"&jid="+jid)

def import_job_db(user, app, cid):
    dal = migrate.dal(uri=config.uri, migrate=True)
    uid = dal.db.users(user=user).id
    dal.db.jobs.insert(
        uid=uid,
        app=app,
        cid=cid,
        state='D',
        description='',
        time_submit=time.asctime(),
        walltime='',
        np='',
        priority=''
    )
    dal.db.commit()

@routes.get('/jobs/import', method='POST')
def import_job():
    upload = request.files.get('upload')

    z = zipfile.ZipFile(upload.file)
    z.extractall()

    # Get the username, appname, and case id from the file structure
    _, user, app, cid, _ = z.namelist()[0].split(os.sep)

    import_job_db(user, app, cid)

    redirect('/jobs')
