from __future__ import print_function
from __future__ import absolute_import
from flask import Flask, Blueprint
import os, re, sys, shutil, urllib, traceback, cgi, time, json
import argparse as ap
try:
    import requests
except:
    print("INFO: not importing requests... only needed for remote workers")

from .common import slurp_file
from .model import db, Users, Jobs
from . import config

user_dir = 'user_data'
upload_dir = '_uploads'

user_data = Blueprint('routes', __name__)

@user_data.route('/' + user_dir + '/<filepath:path>')
def get_user_data(filepath):
    user = root.authorized()
    # filepath = request.query.filepath
    # get the owner from the filepath
    # e.g. "user_data/wes/mendel/y23022/file.dat"
    path_list = filepath.split("/")
    owner = path_list[0]
    cid = path_list[2]
    shared = Jobs.get(Jobs.cid == cid).shared
    # print filepath, path_list, shared

    # only allow admin to see other user's cases that have not been shared
    if owner != user and shared != "True" and user != "admin":
        return template('error', err="access forbidden")

    return static_file(filepath, root=user_dir)


@user_data.route('/more')
def more():
    """given a form with the attribute plotpath,
       output the file to the browser"""
    user = root.authorized()
    app = request.query.app
    cid = request.query.cid

    filepath = request.query.filepath
    # get the owner from the filepath
    # e.g. "user_data/wes/mendel/y23022/file.dat"
    path_list = filepath.split("/")
    owner = path_list[1]

    if re.search("/", cid):
        (_, c) = cid.split("/")
    else:
        c = cid

    shared = Jobs.get(Jobs.cid == c).shared
    # only allow admin to see other user's cases that have not been shared
    if owner != user and shared != "True" and user != "admin":
        return template('error', err="access forbidden")

    contents = slurp_file(filepath)
    # convert html tags to entities (e.g. < to &lt;)
    contents = cgi.escape(contents)
    params = { 'cid': c, 'contents': contents, 'app': app, 'user': user, 'fn': filepath }
    return template('more', params)


@user_data.route('/case')
def case():
    user = root.authorized()
    app = request.query.app
    root.set_active(app)
    cid = request.query.cid
    jid = request.query.jid

    if re.search("/", cid):
        (owner, c) = cid.split("/")
        shared = Jobs.get(Jobs.cid == c).shared
        # only allow admin to see other user's cases that have not been shared
        if owner != user and shared != "True" and user != "admin":
            return template('error', err="access forbidden")

    else:
        owner, c = user, cid

    # if case does not exist return error
    if Jobs.get_or_none(Jobs.cid == c) is None:
        return template('error', err="case does not exist")

    state = Jobs.get(Jobs.cid == c).state
    run_dir = os.path.join(user_dir, owner, root.myapps[app].appname, c)
    fn = os.path.join(run_dir, root.myapps[app].outfn)

    # note: eventually need to merge the following two into one
    if re.search("/", cid):
        sid = request.query.sid # id of item in shared
        output = slurp_file(fn)

        params = { 'cid': cid, 'app': app, 'contents': output,
                   'sid': sid, 'user': user, 'fn': fn, 'state': state, 'owner': owner }

        if jid: params['jid'] = jid

        return template('case_public', params)

    else:
        result = Jobs.select().where(Jobs.cid == cid).first()
        desc = result['description']
        shared = result['shared']

        params = { 'cid': cid, 'app': app, 'jid': jid,
                   'user': user, 'fn': fn, 'description': desc, 'shared': shared,
                   'state': state, 'owner': owner }

        if jid: params['jid'] = jid

        #return template('case', params)
        return template('case_tail-f', params)


@user_data.route('/output')
def output():
    user = root.authorized()
    app = request.query.app
    cid = request.query.cid
    jid = request.query.jid

    if re.search("/", cid):
        (owner, c) = cid.split("/")
    else:
        owner = user
        c = cid

    shared = jobs(cid=c).shared
    # only allow admin to see other user's cases that have not been shared
    if owner != user and shared != "True" and user != "admin":
        return template('error', err="access forbidden")

    run_dir = os.path.join(user_dir, owner, root.myapps[app].appname, c)
    fn = os.path.join(run_dir, root.myapps[app].outfn)

    # prevent 500 error in case config.worker not defined in config.py
    try: config.worker
    except: config.worker = 'local'

    if config.worker == 'remote':

        params = {'user': user, 'app': app, 'cid': cid}
        resp = requests.get(config.remote_worker_url +'/output', params=params)
        output = resp.text

    else:

        output = slurp_file(fn)
        # the following line will convert HTML chars like > to entities &gt;
        # this is needed so that XML input files will show paramters labels
        output = cgi.escape(output)

    desc = jobs(cid=c).description

    params = { 'cid': cid, 'contents': output, 'app': app,
               'user': owner, 'owner': owner, 'fn': fn, 'description': desc }

    if jid: params['jid'] = jid

    return template('more', params)


@user_data.route('/inputs')
def inputs():
    user = root.authorized()
    app = request.query.app
    cid = request.query.cid

    if re.search("/", cid):
        (owner, c) = cid.split("/")
    else:
        owner = user
        c = cid

    shared = jobs(cid=c).shared
    # only allow admin to see other user's cases that have not been shared
    if owner != user and shared != "True" and user != "admin":
        return template('error', err="access forbidden")

    run_dir = os.path.join(user_dir, owner, root.myapps[app].appname, c)
    fn = os.path.join(run_dir, root.myapps[app].simfn)
    inputs = slurp_file(fn)
    # the following line will convert HTML chars like > to entities &gt;
    # this is needed so that XML input files will show paramters labels
    inputs = cgi.escape(inputs)

    desc = jobs(cid=c).description

    params = { 'cid': cid, 'contents': inputs, 'app': app, 'user': owner,
               'fn': fn, 'description': desc }
    return template('more', params)


@user_data.route('/files')
def list_files():
    user = root.authorized()
    cid = request.query.cid
    app = request.query.app
    path = request.query.path

    params = dict()
    params['cid'] = cid
    params['app'] = app
    params['user'] = user

    q = request.query.q
    if "." not in q or q == "*.*": q = ""

    if re.search("/", cid):
        owner, cid = cid.split("/")
    else:
        owner = user

    shared = Jobs.get(Jobs.cid == cid).shared
    # only allow admin to see other user's cases that have not been shared
    if owner != user and shared != "True" and user != "admin":
        return template('error', err="access forbidden")

    if not path:
        path = os.path.join(user_dir, owner, app, cid)

    params['path'] = path
    if q:
        _, ext = q.split('.')
        params['files'] = sorted([ fn for fn in os.listdir(path) if fn.endswith(ext) ])
    else:
        q = ""
        params['files'] = sorted(os.listdir(path))
    params['q'] = q

    num_files = len(params['files'])
    params['status'] = "listing " + str(num_files) + " files"
    params['description'] = jobs(cid=cid).description

    return template('files', params)


@user_data.route('/files/delete_selected', methods=['POST'])
def delete_f():
    user = root.authorized()
    app = request.forms.app
    cid = request.forms.cid
    selected_files = request.forms.selected_files
    files = selected_files.rstrip(':').split(':')
    for file in files:
        path = os.path.join(user_dir, user, app, cid, file)
        if cid is not None:
            if os.path.isfile(path):
                print("removing file:", path)
                os.remove(path)
            elif os.path.isdir(path):
                print("removing path:", path)
                shutil.rmtree(path)
        else:
            print("ERROR: not removing path:", path, "because cid missing")
    redirect("/files?cid="+cid+"&app="+app)


@user_data.route('/files/modify/<operation>', methods=['POST'])
def modify_selected_files(operation):
    user = root.authorized()
    app = request.forms.app
    cid = request.forms.cid
    factor = request.forms.factor or 1.0
    factor = float(factor)
    columns = request.forms.columns or 1
    cols = list(map(int, columns.split(':')))

    import operator
    ops = {'add': operator.add, 'sub': operator.sub,
           'mul': operator.mul, 'div': operator.div}
    op = ops[operation]

    selected_files = request.forms.selected_files_mod
    files = selected_files.rstrip(':').split(':')

    for file in files:
        print(file)
        path = os.path.join(user_dir, user, app, cid, file)

        out = list()
        with open(path, "r") as infile:
            # Loop over lines in each file
            for line in infile:
                line = str(line)
                # Skip comment lines
                if not re.search('^#', line):
                    items = line.split()
                    if len(items) > 0:
                        # execute operation on user-specified columns
                        for col in cols:
                            items[col-1] = str(op(float(items[col-1]), factor))
                    out.append('\t'.join(items)+'\n')
                else:
                    out.append(line)

        with open(path, "w") as outfile:
            outfile.writelines(out)
            outfile.write("# modifications to file: cols = " + str(cols) + ", operation = " + operation + ", factor = " + str(factor) + "\n")

    redirect("/files?cid="+cid+"&app="+app)


@user_data.route('/files/zip_selected', methods=['POST'])
def zip_selected_files():
    user = root.authorized()
    import zipfile
    app = request.forms.app
    cid = request.forms.cid

    selected_files = request.forms.selected_files_zip
    files = selected_files.rstrip(':').split(':')

    for file in files:
        path = os.path.join(user_dir, user, app, cid, file)
        print("attempting to zip:", path)
        zf = zipfile.ZipFile(path+".zip", mode='w', compression=zipfile.ZIP_DEFLATED)
        zf.write(path)
        zf.close()
        # remove the original file if the zipfile now exists
        if os.path.isfile(path+".zip"): os.remove(path)

    redirect("/files?cid="+cid+"&app="+app)


@user_data.route('/zipcase')
def zip_case():
    """zip case on machine to prepare for download"""
    user = root.authorized()
    import zipfile
    app = request.query.app
    cid = request.query.cid

    base_dir = os.path.join(user_dir, user, app)
    path = os.path.join(base_dir, cid+".zip")
    zf = zipfile.ZipFile(path, mode='w', compression=zipfile.ZIP_DEFLATED)
    sim_dir = os.path.join(base_dir, cid)
    for fn in os.listdir(sim_dir):
        zf.write(os.path.join(sim_dir, fn))
    zf.close()

    return static_file(path, root="./")
    # status = "case compressed"
    # redirect(request.headers.get('Referer')+"&status="+status)


@user_data.route('/zipget')
def zipget():
    """get zipfile from another machine, save to current machine"""
    import zipfile
    user = root.authorized()
    cid = request.query.cid
    app = request.query.app
    try:
        worker = config.remote_worker_url
    except:
        exc_type, exc_value, exc_traceback = sys.exc_info()
        print(traceback.print_exception(exc_type, exc_value, exc_traceback))
        worker = request.query.url

    # if config.worker != "remote" or config.remote_worker_url is None:
    if worker is None:
        params = { 'app': app,
                   'err': "worker and remote_worker_url parameters must be set " +
                          " in config.py for this feature to work" }
        return template('error', params)

    requests.get(worker + "/zipcase",
         params={'app': app, 'cid': cid, 'user': user})

    path = os.path.join(user_dir, user, app, cid)
    file_path = path+".zip"
    url = os.path.join(worker, file_path)

    print("url is:", url)
    if not os.path.exists(path):
        os.makedirs(path)

    print("downloading " + url)
    fh, _ = urllib.urlretrieve(url)
    z = zipfile.ZipFile(fh, 'r', compression=zipfile.ZIP_DEFLATED)
    z.extractall()

    # Query for user ID
    user_instance = Users.get_or_none(Users.user == user)
    if user_instance:
        uid = user_instance.id

        # Add case to database
        Jobs.create(uid=uid, app=app, cid=cid, state="REMOTE",
                    description="", time_submit=time.asctime(),
                    walltime="", np="", priority="")

    # status = "file_downloaded"
    # redirect(request.headers.get('Referer')) #+ "&status=" + status)
    redirect("/jobs")


@user_data.route('/upload', methods=['POST'])
def upload_file():
	# upload file to user_dir/user/upload_dir folder
    user = root.authorized()
    upload = request.files.upload
    if not upload:
        return template('error', err="no file selected.")

    save_path_dir = os.path.join(user_dir, user, upload_dir)
    if not os.path.exists(save_path_dir): os.makedirs(save_path_dir)
    save_path = os.path.join(save_path_dir, upload.filename)
    if os.path.isfile(save_path):
        return template('error', err="file exists")
    upload.save(save_path)
    return "SUCCESS"


@user_data.route('/upload_data', methods=['POST'])
def upload_data():
	# upload a payload of data that the user submits via form to the filename specified
    user = root.authorized()
    save_path_dir = os.path.join(user_dir, user, upload_dir)
    if not os.path.exists(save_path_dir): os.makedirs(save_path_dir)
    filename = request.forms.filename
    # print "filename:", filename
    if not filename: return template('error', err="file not specified")
    save_path = os.path.join(save_path_dir, filename)
    # print "save_path:", save_path
    # if os.path.isfile(save_path): return template('error', err="file exists")
    upload_data = request.forms.upload_data
    with open(save_path, 'w') as f: f.write(upload_data)


@user_data.route('/download/<filepath:path>')
def download(filepath):
    root.authorized()
    return static_file(filepath, root='download', download=filepath)


@user_data.route('/notifications')
def get_notifications():
    user = root.authorized()
    response = dict()
    response['new_shared_jobs'] = users(user=user).new_shared_jobs
    return json.dumps(response)

