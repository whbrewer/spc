from bottle import Bottle, request, template, redirect
import os, sys, traceback, cgi, time, shutil, json
import argparse as ap
from model import users, db, apps, app_user, plots
from common import slurp_file
import config
import apps_reader_writer as apprw

routes = Bottle()

def bind(app):
    global root
    root = ap.Namespace(**app)

@routes.get('/<app>')
def show_app(app):
    # very similar to start_new_job() consider consolidating
    user = root.authorized()
    root.set_active(app)
    # parameters for return template
    if app not in root.myapps:
        return template('error', err="app %s is not installed" % (app))

    try:
        params = {}
        params.update(root.myapps[app].params)
        params['cid'] = ''
        params['app'] = app
        params['user'] = user
        params['apps'] = root.myapps
        return template(os.path.join('apps', app),  params)
    except:
        exc_type, exc_value, exc_traceback = sys.exc_info()
        print traceback.print_exception(exc_type, exc_value, exc_traceback)
        redirect('/app/'+app)

@routes.post('/app_exists/<appname>')
def app_exists(appname):
    """Server-side AJAX function to check if an app exists in the DB."""
    appname = request.forms.appname
    # return booleans as strings here b/c they get parsed by JavaScript
    if apps(name=appname): return 'true'
    else: return 'false'

@routes.get('/apps')
def showapps():
    user = root.authorized()
    q = request.query.q
    if not q:
        result = db().select(apps.ALL, orderby=apps.name)
    else:
        result = db(db.apps.name.contains(q, case_sensitive=False) |
                    db.apps.category.contains(q, case_sensitive=False) |
                    db.apps.description.contains(q, case_sensitive=False)).select()

    # find out what apps have already been activated so that a user can't activate twice
    uid = users(user=user).id
    activated = db(app_user.uid == uid).select()
    activated_apps = []
    for row in activated:
        activated_apps.append(row.appid)

    if user == "admin":
        configurable = True
    else:
        configurable = False

    params = { 'configurable': configurable, 'user': user }
    return template('apps', params, rows=result, activated=activated_apps)

@routes.get('/myapps')
def showapps():
    user = root.authorized()
    uid = users(user=user).id
    app = root.active_app()

    result = db((apps.id == app_user.appid) & (uid == app_user.uid)).select(orderby=apps.name)
    if user == "admin":
        configurable = True
    else:
        configurable = False
    params = { 'configurable': configurable, 'user': user, 'app': app }
    return template('myapps', params, rows=result)

@routes.get('/apps/load')
def get_load_apps():
    root.load_apps()
    redirect('/myapps')

@routes.post('/app/edit/<appid>')
def app_edit(appid):
    user = root.authorized()
    if user != 'admin':
        return template('error', err="must be admin to edit app")
    cid = request.forms.cid
    app = request.forms.app
    result = db(apps.name==app).select().first()
    params = {'app': app, 'cid': cid}
    return template('app_edit', params, rows=result)

@routes.post('/app/save/<appid>')
def app_save(appid):
    root.authorized()
    app = request.forms.app
    lang = request.forms.language
    info = request.forms.input_format
    category = request.forms.category
    preprocess = request.forms.preprocess
    postprocess = request.forms.postprocess
    assets = request.forms.assets
    if assets == "None": assets = None
    desc = request.forms.description
    row = db(db.apps.id==appid).select().first()
    row.update_record(language=lang, category=category, description=desc, input_format=info,
                      preprocess=preprocess, postprocess=postprocess, assets=assets)
    db.commit()
    redirect("/app/"+app)

# allow only admin or user to delete apps
@routes.post('/app/delete/<appid>')
def delete_app(appid):
    user = root.authorized()
    if user != 'admin':
        return template('error', err="must be admin to edit app")
    appname = request.forms.app
    del_app_dir = request.forms.del_app_dir

    try:
        if user == 'admin':
            # delete entry in DB
            a = apprw.App()
            if del_app_dir == "on":
                del_files = True
            else:
                del_files = False
            root.myapps[appname].delete(appid, del_files)
        else:
            return template("error", err="must be admin")
    except:
        exc_type, exc_value, exc_traceback = sys.exc_info()
        print traceback.print_exception(exc_type, exc_value, exc_traceback)
        return template("error", err="failed to delete app... did the app load properly?")

    redirect("/apps")

@routes.get('/app/<app>')
def view_app(app):
    user = root.authorized()
    if app: root.set_active(app)
    else: redirect('/myapps')

    if user != 'admin':
        return template('error', err="must be admin to edit app")
    cid = request.query.cid
    result = db(apps.name==app).select().first()
    params = {}
    params['app'] = app
    params['user'] = user
    params['cid'] = cid
    #if request.query.edit:
    #    return template('appedit', params, rows=result)
    #else:
    try:
        return template('app', params, rows=result)
    except:
        exc_type, exc_value, exc_traceback = sys.exc_info()
        print traceback.print_exception(exc_type, exc_value, exc_traceback)
        return template('error', err="there was a problem showing the app template. Check traceback.")


@routes.post('/useapp')
def useapp():
    user = root.authorized()
    uid = users(user=user).id
    app = request.forms.app
    appid = apps(name=app).id
    print "allowing user", user, uid, "to access app", app, appid
    app_user.insert(uid=uid, appid=appid)
    db.commit()
    redirect('/apps')

@routes.post('/removeapp')
def removeapp():
    user = root.authorized()
    uid = users(user=user).id
    app = request.forms.app
    appid = apps(name=app).id
    auid = app_user(uid=uid, appid=appid).id
    del app_user[auid]
    print "removing user", user, uid, "access to app", app, appid
    db.commit()
    redirect('/myapps')

@routes.get('/addapp')
def getaddapp():
    user = root.authorized()
    if user != 'admin':
        return template('error', err="must be admin to add app")
    return template('appconfig/addapp')

@routes.post('/addapp')
def addapp():
    user = root.authorized()
    if user != 'admin':
        return template('error', err="must be admin to add app")
    appname = request.forms.appname
    input_format = request.forms.input_format
    # ask for app name
    category = request.forms.category
    language = request.forms.language
    description = request.forms.description
    command = request.forms.command
    preprocess = request.forms.preprocess
    postprocess = request.forms.postprocess
    # put in db
    a = apprw.App()
    #print "user:",user
    a.create(appname, description, category, language,
             input_format, command, preprocess, postprocess)
    # load_apps() needs to be called here in case a user wants to delete
    # this app just after it has been created... it is called again after
    # the user uploads a sample input file
    root.load_apps()
    redirect('/app/'+appname)

@routes.get('/appconfig/status')
def appconfig_status():
    root.authorized()
    status = dict()
    app = request.query.app

    # check db file
    appname = apps(name=app).name
    if appname:
        status['command'] = 1
    else:
        status['command'] = 0

    # check template file
    if os.path.exists("views/apps/"+app+".tpl"):
        status['template'] = 1
    else:
        status['template'] = 0

    # check inputs file
    extension = {'namelist': '.in', 'ini': '.ini', 'xml': '.xml', 'json': '.json', 'yaml': '.yaml'}
    if os.path.exists(os.path.join(apprw.apps_dir, app,
                      app + extension[root.myapps[app].input_format])):
        status['inputs'] = 1
    else:
        status['inputs'] = 0

    # check app binary
    if os.path.exists(os.path.join(apprw.apps_dir, app, app)):
        status['binary'] = 1
    else:
        status['binary'] = 0

    # check plots
    appid = apps(name=app).id
    result = db(plots.appid==appid).select().first()
    if result:
        status['plots'] = 1
    else:
        status['plots'] = 0

    return json.dumps(status)


@routes.post('/appconfig/exe/<step>')
def appconfig_exe(step="upload"):
    user = root.authorized()
    if user != 'admin':
        return template('error', err="must be admin to configure app")
    if step == "upload":
        appname = request.forms.appname
        params = {'appname': appname}
        return template('appconfig/exe_upload', params)
    elif step == "test":
        appname    = request.forms.appname
        upload     = request.files.upload
        if not upload:
            return template('appconfig/error',
                   err="no file selected. press back button and try again")
        name, ext = os.path.splitext(upload.filename)
        # if ext not in ('.exe','.sh','.xml','.json',):
        #     return 'ERROR: File extension apps not allowed.'
        try:
            save_path_dir = os.path.join(apprw.apps_dir, name)
            if not os.path.exists(save_path_dir):
                os.makedirs(save_path_dir)
            save_path = os.path.join(save_path_dir, name) + ext
            if os.path.isfile(save_path):
                timestr = time.strftime("%Y%m%d-%H%M%S")
                shutil.move(save_path, save_path+"."+timestr)
            upload.save(save_path)
            os.chmod(save_path, 0700)

            # process = subprocess.Popen(["otool -L", save_path], stdout=subprocess.PIPE, stdin=subprocess.PIPE)
            # contents = process.readlines()
            contents = "SUCCESS"

            params = {'appname': appname, 'contents': contents}
            return template('appconfig/exe_test', params)
        except IOError:
            exc_type, exc_value, exc_traceback = sys.exc_info()
            print traceback.print_exception(exc_type, exc_value, exc_traceback)
            return "IOerror:", IOError
        else:
            return "ERROR: must be already a file"

@routes.post('/appconfig/export')
def export():
    user = root.authorized()
    if user != 'admin':
        return template('error', err="must be admin to use export function")
    app = request.forms.app
    result = db(apps.name==app).select().first()

    data = {}
    data['name'] = result.name
    data['description'] = result.description
    data['category'] = result.category
    data['language'] = result.language
    data['input_format'] = result.input_format
    data['command'] = result.command
    data['preprocess'] = result.preprocess
    data['postprocess'] = result.postprocess

    assets = list()
    if result.assets is not None:
        for asset in result.assets.split(","):
            assets.append(asset.strip())
    data['assets'] = assets

    appid = apps(name=app).id

    myplots = db(plots.appid==appid).select()
    data['plots'] = list()

    for p in myplots:
        thisplot = {}
        thisplot['ptype'] = p.ptype
        thisplot['title'] = p.title
        thisplot['options'] = p.options
        thisplot['datasource'] = list()

        myds = db(datasource.pltid==p.id).select()

        for ds in myds:
            thisds = {}
            thisds['label'] = ds.label
            thisds['filename'] = ds.filename
            thisds['cols'] = ds.cols
            thisds['line_range'] = ds.line_range
            thisds['data_def'] = ds.data_def

            thisplot['datasource'].append(thisds)

        data['plots'].append(thisplot)

    path = os.path.join(apprw.apps_dir, app, 'spc.json')
    with open(path, 'w') as outfile:
        json.dump(data, outfile, indent=3)

    return "spc.json file written to " + path + "<meta http-equiv='refresh' content='2; url=/app/"+app+"'>"

@routes.post('/appconfig/inputs/<step>')
def edit_inputs(step):
    user = root.authorized()
    if user != 'admin':
        return template('error', err="must be admin to edit app")
    # upload zip file and return a text copy of the input file
    if step == "upload":
        appname = request.forms.appname
        input_format = request.forms.input_format
        params = {'appname': appname, 'input_format': input_format}
        return template('appconfig/inputs_upload', params)
    if step == "parse":
        input_format = request.forms.input_format
        appname    = request.forms.appname
        upload     = request.files.upload
        if not upload:
            return template('appconfig/error',
                   err="no file selected. press back button and try again")
        name, ext = os.path.splitext(upload.filename)
        if ext not in ('.in', '.ini', '.xml', '.json', '.yaml', ):
            return 'ERROR: File extension not allowed.'
        try:
            save_path_dir = os.path.join(apprw.apps_dir, name)
            if not os.path.exists(save_path_dir):
                os.makedirs(save_path_dir)
            save_path = os.path.join(save_path_dir, name) + ext
            if os.path.isfile(save_path):
                timestr = time.strftime("%Y%m%d-%H%M%S")
                shutil.move(save_path, save_path+"."+timestr)
            upload.save(save_path)

            # return the contents of the input file
            # this is just for namelist.input format, but
            # we need to create this dynamically based on input_format
            if input_format == "namelist":
                fn = appname + ".in"
            elif input_format == "ini":
                fn = appname + ".ini"
            elif input_format == "xml":
                fn = appname + ".xml"
            elif input_format == "json":
                fn = appname + ".json"
            elif input_format == "yaml":
                fn = appname + ".yaml"
            else:
                return "ERROR: input_format not valid: ", input_format
            path = os.path.join(apprw.apps_dir, appname, fn)
            # cgi.escape converts HTML chars like > to entities &gt;
            contents = cgi.escape(slurp_file(path))
            params = {'fn': fn, 'contents': contents, 'appname': appname,
                      'input_format': input_format }
            return template('appconfig/inputs_parse', params)
        except IOError:
            exc_type, exc_value, exc_traceback = sys.exc_info()
            print traceback.print_exception(exc_type, exc_value, exc_traceback)
            return "IOerror:", IOError
        else:
            return "ERROR: must be already a file"
    # show parameters with options how to tag and describe each parameter
    elif step == "create_view":
        input_format = request.forms.input_format
        appname = request.forms.appname
        myapp = root.app_instance(input_format, appname)
        inputs, _, _ = myapp.read_params()
        print "inputs:", inputs
        params = { "appname": appname }
        return template('appconfig/inputs_create_view', params, inputs=inputs,
                                        input_format=input_format)
    # create a template in the views/apps folder
    elif step == "end":
        appname = request.forms.get('appname')
        html_tags = request.forms.getlist('html_tags')
        data_type = request.forms.getlist('data_type')
        descriptions = request.forms.getlist('descriptions')
        bool_rep = request.forms.bool_rep
        keys = request.forms.getlist('keys')
        key_tag = dict(zip(keys, html_tags))
        key_desc = dict(zip(keys, descriptions))
        input_format = request.forms.input_format
        myapp = root.app_instance(input_format, appname)
        params, _, _ = myapp.read_params()
        if myapp.create_template(html_tags=key_tag, bool_rep=bool_rep, desc=key_desc):
            root.load_apps()
            params = { "appname": appname, "port": config.port }
            return template('appconfig/inputs_end', params)
        else:
            return "ERROR: there was a problem when creating view"
    else:
        return template('error', err="step not supported")
