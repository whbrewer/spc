from bottle import Bottle, request, template, redirect
import argparse as ap
import psutil, json, traceback
from model import db, users, jobs

routes = Bottle()

def bind(app):
    global root
    root = ap.Namespace(**app)

@routes.get('/notifications')
def get_notifications():
    user = root.authorized()
    response = dict()
    response['new_shared_jobs'] = users(user=user).new_shared_jobs
    return json.dumps(response)

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
