import sys
import docker
import datetime
import math
import argparse as ap
from model import *
from bottle import Bottle

root = 0

def bind(app):
    global root
    root = ap.Namespace(**app)

dockerMod = Bottle()

@dockerMod.route('/docker')
def get_docker():
    global root
    if not root.authorized(): root.redirect('/login')
    user = root.getuser()
    cid = root.request.query.cid
    app = root.request.query.app
    uid = root.db(users.user==user).select(users.id).first()
    instances = root.db(containers.uid==uid).select()
    params = {}
    params['cid'] = cid
    params['app'] = app
    params['user'] = user
    params['apps'] = root.myapps.keys()
    params['host'] = 'localhost'
    params['image'] = 'ubuntu'
    if root.request.query.status:
        params['status'] = root.request.query.status
    return root.template('docker',params,instances=instances)

class Container(object):
    """start, stop, and status of Docker containers"""

    def __init__(self, host, image):
        self.conn = docker.Client(base_url=host)
        self.image = image

    def start(self):
        self.conn.create_container(image=self.image)

    def stop(self):
        self.conn.remove_contianer()
