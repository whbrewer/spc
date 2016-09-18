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
    params = {}

    try:
        cli = docker.Client(base_url='unix://var/run/docker.sock')
        images = cli.images()
        conts = cli.containers(all=True)
    except:
        images = []
        conts = []
        params['status'] = "there was a problem talking to the Docker daemon... Are you sure Docker is running?"

    params['user'] = user
    # params['apps'] = root.myapps.keys()
    params['host'] = 'localhost'
    params['image'] = 'ubuntu'
    instances = root.db(containers.uid==uid).select()

    if root.request.query.status:
        params['status'] = root.request.query.status
    return root.template('docker', params, images=images, instances=instances, containers=conts)

@dockerMod.route('/docker/create/<id>', method='GET')
def create_container(id):
    print "image id is:", id
    cli = docker.Client(base_url='unix://var/run/docker.sock')
    try:
        cli.create_container(image=id)
        status = "SUCCESS: container created " + id
    except:
        status = "ERROR: failed to start container ", id
    redirect("/docker?status="+status)

@dockerMod.route('/docker/start/<id>', method='GET')
def start_container(id):
    print "container_id is:", id
    cli = docker.Client(base_url='unix://var/run/docker.sock')
    try:
        cli.start(container=id)
        status = "SUCCESS: started container " + id
    except:
        status = "ERROR: failed to start container " + id
    redirect("/docker?status="+status)

@dockerMod.route('/docker/stop/<id>', method='GET')
def stop_container(id):
    cli = docker.Client(base_url='unix://var/run/docker.sock')
    try:
        cli.stop(container=id)
        status = "SUCCESS: stopped container " + id
    except:
        status = "ERROR stopping container " + id
    root.redirect("/docker?status="+status)

@dockerMod.route('/docker/remove/<id>', method='GET')
def container_status(id):
    cli = docker.Client(base_url='unix://var/run/docker.sock')
    # return json.dumps(cli.containers())
    try: 
        cli.remove_container(id)
        status = "SUCCESS: removed container " + id
    except:
        status = "ERROR: problem removing container " + id
    redirect("/docker?status="+status)


# the following code is not currently used...
# it is based on the concept that we were going to store the containers in the DB
# which is not necessary if we can communicate directly with the Docker daemon

def get_container_id(id):
    return root.db(containers.id==id).select(containers.containerid).first()['containerid']

def get_image(id):
    return root.db(containers.id==id).select(containers.image).first()

@dockerMod.route('/docker/container', method='POST')
def get_docker():
    global root
    if not root.authorized(): root.redirect('/login')
    user = root.getuser()    
    cid = request.forms.containerid
    img = request.forms.image
    cmd = request.forms.command
    user = root.getuser()
    uid = root.db(users.user==user).select(users.id).first()
    root.db.containers.insert(containerid=cid, image=img, command=cmd, uid=uid)
    db.commit()
    redirect("/docker")

class Container(object):
    """start, stop, and status of Docker containers"""

    def __init__(self, host, image):
        self.conn = docker.Client(base_url=host)
        self.image = image

    def start(self):
        self.conn.create_container(image=self.image)

    def stop(self):
        self.conn.remove_container()
