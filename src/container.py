import sys
import docker
import datetime
import math
import json
import argparse as ap
from model import *
from bottle import Bottle, request, redirect

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
    # params['cid'] = cid
    # params['app'] = app
    params['user'] = user
    params['apps'] = root.myapps.keys()
    params['host'] = 'localhost'
    params['image'] = 'ubuntu'
    if root.request.query.status:
        params['status'] = root.request.query.status
    return root.template('docker', params, instances=instances)

@dockerMod.route('/docker/start/<id>', method='GET')
def start_container(id):
    cid = get_container_id(id)
    print "container_id is:", cid
    cli = docker.Client(base_url='unix://var/run/docker.sock')
    try:
        cli.start(container=cid)
        return "OK"
    except:
        return "ERROR: failed to start container"

def get_container_id(id):
    return root.db(containers.id==id).select(containers.containerid).first()['containerid']

def get_image(id):
    return root.db(containers.id==id).select(containers.image).first()

@dockerMod.route('/docker/status/<id>', method='GET')
def container_status(id):
    cli = docker.Client(base_url='unix://var/run/docker.sock')
    # return json.dumps(cli.containers())
    try: 
        return cli.containers()[0]['Status']
    except:
        return "no containers running"

@dockerMod.route('/docker/stop/<id>', method='GET')
def stop_container(id):
    cid = get_container_id(id)
    cli = docker.Client(base_url='unix://var/run/docker.sock')
    try:
        cli.stop(container=cid)
        return "SUCCESS: stopped container", cid
    except:
        return "ERROR stopping container"

@dockerMod.route('/docker/container', method='POST')
def get_docker():
    # user = authorized()
    cid = request.forms.containerid
    img = request.forms.image
    cmd = request.forms.command
    user = root.getuser()
    uid = root.db(users.user==user).select(users.id).first()
    root.db.containers.insert(containerid=cid, image=img, command=cmd, uid=uid)
    db.commit()
    # if root.request.query.status:
    #     params['status'] = root.request.query.status
    #redirect("/docker?app="+app+"&cid="+str(cid))
    redirect("/docker")


class Container(object):
    """start, stop, and status of Docker containers"""

    def __init__(self, host, image):
        self.conn = docker.Client(base_url=host)
        self.image = image

    def start(self):
        self.conn.create_container(image=self.image)

    def stop(self):
        self.conn.remove_contianer()
