from bottle import Bottle, request, template
import sys, psutil, json, traceback, argparse as ap

from model import db, jobs

routes = Bottle()

def bind(app):
    global root
    root = ap.Namespace(**app)

@routes.get('/stats')
def get_stats():
    root.authorized()
    params = {}

    # number of jobs in queued, running, and completed states
    params['nq'] = db(jobs.state=='Q').count()
    params['nr'] = db(jobs.state=='R').count()
    params['nc'] = db(jobs.state=='C').count()

    params['cpu'] = psutil.cpu_percent()
    params['vm'] = psutil.virtual_memory()
    params['disk'] = psutil.disk_usage('/')
    params['cid'] = request.query.cid
    params['app'] = request.query.app

    return template("stats", params)

@routes.get('/stats/mem')
def get_stats_mem():
    res = {}
    try:
        res['mem'] = psutil.virtual_memory().percent
        res['cpu'] = psutil.cpu_percent()
        return json.dumps(res)
    except:
        exc_type, exc_value, exc_traceback = sys.exc_info()
        print traceback.print_exception(exc_type, exc_value, exc_traceback)
        pass




