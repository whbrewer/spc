from bottle import Bottle, request, template, redirect
import argparse as ap
import os, re, sys, csv, traceback
import json

from user_data import user_dir
from model import db, apps, jobs, plots, datasource
from common import replace_tags
import config

routes = Bottle()


def bind(app):
    global root
    root = ap.Namespace(**app)


def compute_stats(path):
    """compute statistics on output data"""
    xoutput = ''
    if os.path.exists(path):
        f = open(path,'r')
        output = f.readlines()
        for line in output:
            m = re.search(r'#.*$', line)
            if m:
                xoutput += line
        # app-specific: this is a temporary hack for mendel (remove in future)
        if path[-3:] == "hst":
            xoutput += output[len(output)-1]
    return xoutput


class Plot(object):


    def get_data(self,fn,col1,col2=None,line1=1,line2=1e6):
        """return data as string in format [ [x1,y1], [x2,y2], ... ]"""
        y = ''
        z = []
        lineno = 0
        try:
            data = open(fn, 'rU').readlines()
        except IOError:
            exc_type, exc_value, exc_traceback = sys.exc_info()
            print traceback.print_exception(exc_type, exc_value, exc_traceback)
            return -1

        try:
            nlines = len(data)
            # allow for tailing a file by giving a negative range, e.g. -100:10000
            if line1 < 0:
                line1 += nlines
            for line in data:
                lineno += 1
                if lineno >= line1 and lineno <= line2:
                    # don't parse comments
                    if re.search(r'#',line): continue
                    x = line.split()
                    #following line doesnt work when NaN's in another column
                    #if not re.search(r'[A-Za-z]{2,}\s+[A-Za-z]{2,}',line):
                    if col2:
                        y += '[ ' + x[col1-1] + ', ' + x[col2-1] + '], '
                    else:
                        try: z += [ float(x[col1-1]) ]
                        except: pass
            if col2:
                return "[ %s ]" % y
            else:
                return z
        except:
            exc_type, exc_value, exc_traceback = sys.exc_info()
            print traceback.print_exception(exc_type, exc_value, exc_traceback)
            return -2


    def get_csv_data(self, fn):
        try:
            with open(fn, 'rU') as csv_file:
                data = csv.reader(csv_file)
                return list(data)

        except IOError:
            exc_type, exc_value, exc_traceback = sys.exc_info()
            print traceback.print_exception(exc_type, exc_value, exc_traceback)
            return -1


    def get_data_gantt(self,fn,col1,col2,col3,col4,line1=1,line2=1e6):
        """return data as string in format [ [x1,y1], [x2,y2], ... ]"""
        y = ''
        lineno = 0
        try:
            data = open(fn, 'rU').readlines()
            nlines = len(data)
            # allow for tailing a file by giving a negative range, e.g. -100:10000
            if line1 < 0:
                line1 += nlines
            for line in data:
                lineno += 1
                if lineno >= line1 and lineno <= line2:
                    # don't parse comments
                    if re.search(r'#',line): continue
                    x = line.split()
                    #following line doesnt work when NaN's in another column
                    #if not re.search(r'[A-Za-z]{2,}\s+[A-Za-z]{2,}',line):
                    y += '[ ' + x[col1-1] + ', ' + x[col2-1] + x[col3-1] + x[col4-1] + '], '
            s = "[ %s ]" % y
            return s
        except:
            return False


    def get_raw_data(self,fn,line1=1,line2=1e6):
        """return data as an array..."""
        data = open(fn, 'rU').readlines()
        return data[line1:line2]


    def get_column_of_data(self,fn,col,line1=1,line2=1e6):
        try:
            y = []
            lineno = 0
            data = open(fn, 'rU').readlines()
            nlines = len(data)
            # allow for tailing a file by giving a negative range, e.g. -100:10000
            if line1 < 0:
                line1 += nlines
            for line in data:
                lineno += 1
                if lineno >= line1 and lineno <= line2:
                    # don't parse comments
                    if re.search(r'#',line): continue
                    x = line.split()
                    #following line doesnt work when NaN's in another column
                    #if not re.search(r'[A-Za-z]{2,}\s+[A-Za-z]{2,}',line):
                    y += [ x[col-1] ]
            return y
        except:
            return False


    def get_ticks(self,fn,col1,col2):
        try:
            y = ''
            i = 0
            for line in open(fn, 'rU'):
                # don't parse comments
                if re.search(r'#',line): continue
                x = line.split()
                if not re.search(r'[A-Za-z]{2,}\s+[A-Za-z]{2,}',line):
                    y += '[ ' + str(i) + ', ' + x[col1-1] + '], '
                    i += 1
            s = "[ %s ]" % y
            return s
        except:
            return False


@routes.get('/plots/edit')
def editplotdefs():
    user = root.authorized()
    if user != 'admin':
        return template('error', err="must be admin to edit plots")
    app = request.query.app
    if config.auth and not root.authorized(): redirect('/login')
    if app not in root.myapps: redirect('/apps')
    query = (root.apps.id==plots.appid) & (root.apps.name==app)
    result = db(query).select()
    params = { 'app': app, 'user': user }
    return template('plots/plotdefs', params, rows=result)


@routes.get('/plots/edit/<pltid>')
def editplotdef(pltid):
    user = root.authorized()
    if user != 'admin':
        return template('error', err="must be admin to edit plots")
    app = request.forms.app
    result = db(plots.id==pltid).select().first()
    params = { 'app': app, 'user': user }
    return template('plots/edit_plot', params, row=result)


@routes.post('/plots/edit/<pltid>')
def editplot(pltid):
    user = root.authorized()
    if user != 'admin':
        return template('error', err="must be admin to edit plots")
    app = request.forms.app
    title = request.forms.title
    ptype = request.forms.ptype
    options = request.forms.options
    print "updating plot ", pltid, "for app", app
    plots(pltid).update_record(title=title, ptype=ptype, options=options)
    db.commit()
    redirect('/plots/edit?app='+app)


@routes.get('/plots/delete/<pltid>')
def delete_plot(pltid):
    user = root.authorized()
    if user != 'admin':
        return template('error', err="must be admin to edit plots")
    app = request.query.app
    del db.plots[pltid]
    db.commit()
    redirect ('/plots/edit?app='+app)


@routes.get('/plots/<pltid>/datasources')
def get_datasource(pltid):
    """get list of datasources for given plot"""
    user = root.authorized()
    if user != 'admin':
        return template('error', err="must be admin to edit plots")
    app = request.query.app
    cid = request.query.cid
    if root.myapps[app].appname not in root.myapps: redirect('/apps')
    if config.auth and not root.authorized(): redirect('/login')
    result = db(datasource.pltid==pltid).select()
    title = plots(pltid).title
    params = { 'app': app, 'cid': cid, 'user': user, 'pltid': pltid, 'rows': result, 'title': title}
    return template('plots/datasources', params, rows=result)


@routes.post('/plots/<pltid>/datasources')
def add_datasource(pltid):
    """create a new datasource for given plot"""
    user = root.authorized()
    if user != 'admin':
        return template('error', err="must be admin to edit plots")
    app = request.forms.app
    r = request.forms
    datasource.insert(pltid=pltid, label=r['label'],  filename=r['fn'], cols=r['cols'],
                      line_range=r['line_range'], data_def=r['data_def'])
    db.commit()
    redirect ('/plots/' + str(pltid) + '/datasources?app='+app)


@routes.get('/plots/<pltid>/datasources/<dsid>')
def edit_datasource(pltid, dsid):
    """create a new datasource for given plot"""
    user = root.authorized()
    if user != 'admin':
        return template('error', err="must be admin to edit plots")
    app = request.query.app
    query = (datasource.id==dsid)
    result = db(query).select().first()
    params = {'app': app, 'pltid': pltid, 'dsid': dsid}
    return template('plots/edit_datasource', params, row=result)


@routes.post('/plots/<pltid>/datasources/<dsid>')
def edit_datasource_post(pltid, dsid):
    """update datasource for given plot"""
    user = root.authorized()
    if user != 'admin':
        return template('error', err="must be admin to edit plots")
    app = request.forms.get('app')
    r = request.forms
    datasource(id=dsid).update_record(label=r['label'], pltid=pltid, filename=r['fn'], cols=r['cols'],
                                      line_range=r['line_range'], data_def=r['data_def'])
    db.commit()
    redirect ('/plots/' + str(pltid) + '/datasources?app='+app)
    params = {'app': app, 'pltid': pltid, 'dsid': dsid}
    return template('plots/edit_datasource', params)


@routes.post('/plots/datasource_delete')
def delete_datasource():
    user = root.authorized()
    if user != 'admin':
        return template('error', err="must be admin to edit plots")
    app = request.forms.get('app')
    pltid = request.forms.get('pltid')
    dsid = request.forms.get('dsid')
    del db.datasource[dsid]
    db.commit()
    redirect ('/plots/' + str(pltid) + '/datasources?app='+app)


@routes.post('/plots/create')
def create_plot():
    user = root.authorized()
    if user != 'admin':
        return template('error', err="must be admin to edit plots")
    app = request.forms.get('app')
    r = request
    plots.insert(appid=root.myapps[app].appid, ptype=r.forms['ptype'],
                 title=r.forms['title'], options=r.forms['options'])
    db.commit()
    redirect ('/plots/edit?app='+app)


@routes.get('/plot/<pltid>')
def plot_interface(pltid):
    user = root.authorized()
    app = request.query.app
    cid = request.query.cid
    jid = request.query.jid
    params = dict()

    if not cid:
        params['err'] = "No case id specified. First select a case id from the list of jobs."
        return template('error', params)

    if re.search("/", cid):
        (owner, c) = cid.split("/")
    else:
        owner = user
        c = cid

    shared = jobs(cid=c).shared
    # only allow admin to see other user's cases that have not been shared
    if owner != user and shared != "True" and user != "admin":
        return template('error', err="access forbidden")

    inputs, _, _ = root.myapps[app].read_params(owner, c)
    sim_dir = os.path.join(user_dir, owner, app, c)

    # use pltid of 0 to trigger finding the first pltid for the current app
    if int(pltid) == 0:
        query = (apps.id==plots.appid) & (apps.name==app)
        result = db(query).select().first()
        if result: pltid = result['plots']['id']

    p = Plot()

    # get the data for the pltid given
    try:
        result = db(plots.id==pltid).select().first()
        plottype = result['ptype']

        plot_title = result['title']
    except:
        exc_type, exc_value, exc_traceback = sys.exc_info()
        print traceback.print_exception(exc_type, exc_value, exc_traceback)
        redirect ('/plots/edit?app='+app+'&cid='+cid)

    # if plot not in DB return error
    if plottype is None:
        params = { 'cid': cid, 'app': app, 'user': user }
        params['err'] = "Sorry! This app does not support plotting capability"
        return template('error', params)

    # determine which view template to use
    if plottype == 'flot-cat':
        tfn = 'plots/flot-cat'
    elif plottype == 'flot-scatter':
        tfn = 'plots/flot-scatter'
    elif plottype == 'flot-scatter-animated':
        tfn = 'plots/flot-scatter-animated'    # for backwards compatability
    elif plottype == 'flot-line':
        tfn = 'plots/flot-scatter'
    elif plottype == 'plotly-hist':
        tfn = 'plots/plotly-hist'
    elif plottype == 'mpl-line' or plottype == 'mpl-bar':
        redirect('/mpl/'+pltid+'?app='+app+'&cid='+cid)
    elif plottype == 'handson':
        tfn = 'plots/handson'
    elif plottype == 'flot-3d':
        return plot_flot_3d(result, cid, app, sim_dir, owner, user, plot_title, pltid)
    else:
        return template("error", err="plot type not supported: " + plottype)

    if result['options']:
        options = replace_tags(result['options'], inputs)
    else:
        options = ''

    # get list of all plots for this app
    query = (apps.id==plots.appid) & (apps.name==app)
    list_of_plots = db(query).select()

    # extract data from files
    data = []
    ticks = []
    plotpath = ''
    result = db(datasource.pltid==pltid).select()

    datadef = ""
    for r in result:
        plotfn = r['filename']

        # in addition to supporting input params, also support case id
        if "cid" not in inputs: inputs["cid"] = c

        # replace <cid>.dat with xyz123.dat
        plotfn = replace_tags(plotfn, inputs)
        plotpath = os.path.join(sim_dir, plotfn)

        # handle CSV data
        _, file_extension = os.path.splitext(plotfn)
        if file_extension == '.csv':
            data = p.get_csv_data(plotpath)
            stats = ''

        # handle X, Y columnar data
        else:
            cols = r['cols']
            line_range = r['line_range']
            try:
                datadef += r['data_def'] + ", "
            except:
                exc_type, exc_value, exc_traceback = sys.exc_info()
                print traceback.print_exception(exc_type, exc_value, exc_traceback)
                datadef = ""

            if cols.find(":") > 0: # two columns
                num_fields = 2
                (col1str, col2str) = cols.split(":")
                col1 = int(col1str); col2 = int(col2str)
            else: # single column
                num_fields = 1
                col1 = int(cols)

            # do some postprocessing
            if line_range is not None:
                # to prevent breaking current spc apps, still support
                # expressions like 1:1000, but in the future this should
                # be changed to a range 1-1000.  Therefore, using : is deprecated
                # and will be removed in the future.
                (line1str, line2str) = re.split("[-:]", line_range)
                line1 = int(line1str)
                ## there is a problem with the following statement
                ## shows up in mendel app
                # if root.myapps[app].postprocess > 0:
                #    dat = process.postprocess(plotpath, line1, line2)
                # else:
                try: # if line2 is specified
                    line2 = int(line2str)
                    dat = p.get_data(plotpath, col1, col2, line1, line2)
                except: # if line2 not specified
                    exc_type, exc_value, exc_traceback = sys.exc_info()
                    print traceback.print_exception(exc_type, exc_value, exc_traceback)
                    if num_fields == 2:
                        dat = p.get_data(plotpath, col1, col2, line1)
                    else: # single column of data
                        dat = p.get_data(plotpath, col1)
                # remove this app-specific code in future
                if app == "fpg":
                    import process
                    dat = process.postprocess(plotpath, line1, line2)
            else:
                dat = p.get_data(plotpath, col1, col2)

            if dat == -1:
                stats = "ERROR: Could not read data file"
            elif dat == -2:
                stats = "ERROR: file exists, but problem parsing data. Are column and line ranges setup properly? Is all the data there?"
            else:
                stats = compute_stats(plotpath)
            # [[1,2,3]] >>> [1,2,3]

            # clean data
            #dat = [d.replace('?', '0') for d in dat]
            data.append(dat)

            if num_fields == 1: data = data[0]

            if plottype == 'flot-cat':
                ticks = p.get_ticks(plotpath, col1, col2)

    desc = jobs(cid=c).description

    params = { 'cid': cid, 'pltid': pltid,
               'data': data, 'app': app, 'user': user, 'owner': owner,
               'ticks': ticks, 'plot_title': plot_title, 'plotpath': plotpath,
               'rows': list_of_plots, 'options': options, 'datadef': datadef,
               'stats': stats, 'description': desc }

    if jid: params['jid'] = jid

    return template(tfn, params)


def plot_flot_3d(plot, cid, app, sim_dir, owner, user, plot_title, pltid):

    # to handle data in user/cid format when looking at shared cases
    if re.search("/", cid):
        (owner, c) = cid.split("/")
    else:
        owner = user
        c = cid

    desc = jobs(cid=c).description
    list_of_plots = db((apps.id==plots.appid) & (apps.name==app)).select()

    options = json.loads(plot['options'])

    plot_data = []
    z_data = []

    data_dir = os.path.join(sim_dir, options['directory'])
    z_property = options['z_property']
    file_names = sorted(os.listdir(data_dir))

    for file_name in file_names:
        file_path = os.path.join(data_dir, file_name)

        if os.path.isfile(file_path) and not file_name.startswith('.') and file_name.endswith('.json'):
            with open(file_path) as file_:
                file_data = json.load(file_)
                all_series = []

                for source in options['datasources']:
                    series = {
                        'data': zip(file_data[source['x_property']], file_data[source['y_property']]),
                    }
                    series.update(source['data_def'])

                    all_series.append(series)

                plot_data.append(all_series)
                z_data.append(file_data[z_property])

    params = {
        'app': app,
        'cid': cid,
        'description': desc,
        'owner': owner,
        'plot_title': plot_title,
        'pltid': pltid,
        'rows': list_of_plots,
        'stats': '',
        'user': user,
        'flot_3d_json': json.dumps({
            'flot_options': options['flot_options'],
            'data': plot_data,
            'z_data': z_data,
            'z_label': options['z_label'],
            'x_axis_scale': options.get('x_axis_scale', ''),
        }),
    }

    return template('plots/flot-3d', params)


@routes.get('/mpl/<pltid>')
def matplotlib(pltid):
    """Generate a random image using Matplotlib and display it"""
    # in the future create a private function __import__ to import third-party
    # libraries, so that it can respond gracefully.  See for example the
    # Examples section at https://docs.python.org/2/library/imp.html
    user = root.authorized()
    import StringIO
    from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
    from matplotlib.figure import Figure
    app = request.query.app
    cid = request.query.cid

    fig = Figure()
    fig.set_tight_layout(True)
    ax = fig.add_subplot(111)

    # get info about plot from db
    p = Plot()
    result = db(plots.id==pltid).select().first()
    plot_title = result['title']
    plottype = result['ptype']
    options = result['options']

    # parse plot options to extract and set x- and y-axis labels
    m = re.search("xaxis:\s*{(.*)}", options)
    if m:
        n = re.search("axisLabel:\s*\"(\w*)\"", m.group(1))
        if n: ax.set_xlabel(n.group(1))

    m = re.search("yaxis:\s*{(.*)}", options)
    if m:
        n = re.search("axisLabel:\s*\"(\w*)\"", m.group(1))
        if n: ax.set_ylabel(n.group(1))

    # get info about data source
    # fix in the future to handle multiple data sources
    result = db(datasource.pltid==pltid).select()
    for r in result:
        plotfn = r['filename']
        cols = r['cols']
        line_range = r['line_range']
        (col1str, col2str) = cols.split(":")
        col1 = int(col1str)
        col2 = int(col2str)
        if line_range is not None:
            # to prevent breaking current spc apps, still support
            # expressions like 1:1000, but in the future this should
            # be changed to a range 1-1000.  Therefore, using : is deprecated
            # and will be removed in the future.
            (line1str, line2str) = re.split("[-:]", line_range)

    plotfn = re.sub(r"<cid>", cid, plotfn)
    sim_dir = os.path.join(user_dir, user, app, cid)
    plotpath = os.path.join(sim_dir, plotfn)
    xx = p.get_column_of_data(plotpath, col1)
    yy = p.get_column_of_data(plotpath, col2)
    # convert elements from strings to floats
    xx = [float(i) for i in xx]
    yy = [float(i) for i in yy]

    # plot
    if plottype == 'mpl-line':
        ax.plot(xx, yy)
    elif plottype == 'mpl-bar':
        ax.bar(xx, yy)
    else:
        return "ERROR: plottype not supported"
    canvas = FigureCanvas(fig)
    png_output = StringIO.StringIO()
    canvas.print_png(png_output)

    # save file
    tmp_dir = "static/tmp"
    if not os.path.exists(tmp_dir):
        os.makedirs(tmp_dir)
    fn = plot_title+'.png'
    fig.set_size_inches(7, 4)
    img_path = os.path.join(sim_dir, fn)
    fig.savefig(img_path)

    # get list of all plots for this app
    query = (apps.id==plots.appid) & (apps.name==app)
    list_of_plots = db(query).select()
    stats = compute_stats(plotpath)

    params = {'image': fn, 'app': app, 'cid': cid, 'pltid': pltid,
              'plotpath': plotpath, 'img_path': img_path, 'plot_title': plot_title,
              'rows': list_of_plots, 'stats': stats }
    return template('plots/matplotlib', params)
