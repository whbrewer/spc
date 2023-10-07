from __future__ import print_function
from __future__ import absolute_import
from flask import Flask, Blueprint
import sys, json, psutil, datetime, logging, traceback, argparse as ap
from threading import Timer

from .model import db, Jobs

fn = 'log/machine_stats.log'
logging.basicConfig(filename=fn)
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

util = Blueprint('routes', __name__)

@util.route('/stats')
def get_stats():
    root.authorized()
    params = {}

    # number of jobs in queued, running, and completed states
    params['nq'] = Jobs.select().where(Jobs.state == 'Q').count()
    params['nr'] = Jobs.select().where(Jobs.state == 'R').count()
    params['nc'] = Jobs.select().where(Jobs.state == 'C').count()

    params['cpu'] = psutil.cpu_percent()
    params['vm'] = psutil.virtual_memory().percent
    params['disk'] = psutil.disk_usage('/').percent
    params['cid'] = request.query.cid
    params['app'] = request.query.app

    return template("stats", params)

@util.route('/stats/mem')
def get_stats_mem():
    res = {}
    try:
        res['mem'] = psutil.virtual_memory().percent
        res['cpu'] = psutil.cpu_percent()
        return json.dumps(res)
    except:
        exc_type, exc_value, exc_traceback = sys.exc_info()
        print(traceback.print_exception(exc_type, exc_value, exc_traceback))


def print_machine_stats():
    logger.info("%s %s %s", datetime.datetime.now(), psutil.virtual_memory().percent, psutil.cpu_percent())


def setup_rotating_handler(max_bytes = 200000000, backup_count = 3):
    """Create a rotating log handler with the given parameters."""
    handler = logging.handlers.RotatingFileHandler(fn, "a", max_bytes, backup_count)
    # logging.getLogger().addHandler(handler)
    logger.addHandler(handler)


# https://stackoverflow.com/a/38317060/2636544
class MachineStatsLogger(object):

    def __init__(self, interval, function, *args, **kwargs):
        self._timer     = None
        self.interval   = interval
        self.function   = function
        self.args       = args
        self.kwargs     = kwargs
        self.is_running = False
        self.start()

    def _run(self):
        self.is_running = False
        self.start()
        self.function(*self.args, **self.kwargs)

    def start(self):
        if not self.is_running:
            self._timer = Timer(self.interval, self._run)
            self._timer.start()
            self.is_running = True

    def stop(self):
        self._timer.cancel()
        self.is_running = False
