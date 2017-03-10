import sys
import docker
import datetime
import math
import json
import argparse as ap
import config
from model import *
from bottle import Bottle, request, redirect

root = 0
base_url = 'unix://var/run/docker.sock'

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
        cli = docker.Client(base_url=base_url)
        images = cli.images()
        conts = cli.containers(all=True)
    except:
        images = []
        conts = []
        params['status'] = "there was a problem talking to the Docker daemon..."

    params['user'] = user
    params['app'] = root.active_app()

    if root.request.query.status:
        params['status'] = root.request.query.status
    return root.template('docker', params, images=images, containers=conts)

@dockerMod.route('/docker/create/<id>', method='post')
def create_container(id):
    print "creating container:", id
    cli = docker.Client(base_url=base_url)
    host_port_number = int(request.forms.host_port_number)
    container_port_number = int(request.forms.container_port_number)
    try:
        cli.create_container(image=id, ports=[host_port_number], host_config=cli.create_host_config(port_bindings={host_port_number:container_port_number}))
        status = "SUCCESS: container created " + id
    except Exception as e:
        status = "ERROR: failed to start container " + str(e)

    redirect("/docker?status="+status)

# don't think we want to have this option
# @dockerMod.route('/docker/remove_image/<id:path>', method='GET')
# def remove_image(id):
#     print "removing image:", id
#     cli = docker.Client(base_url=base_url)
#     try:
#         msg = cli.remove_image(image=id)
#         status = "SUCCESS: image removed " + id
#     except:
#         status = "ERROR: unable to remove image " + id + \
#                  " Either has dependent child images, or a container is running." + \
#                  " Remove the container and retry."
#     redirect("/docker?status="+status)

@dockerMod.route('/docker/start/<id>', method='GET')
def start_container(id):
    print "starting container:", id
    cli = docker.Client(base_url=base_url)
    try:
        cli.start(container=id)
        status = "SUCCESS: started container " + id
    except:
        status = "ERROR: failed to start container " + id
    redirect("/docker?status="+status)

@dockerMod.route('/docker/stop/<id>', method='GET')
def stop_container(id):
    cli = docker.Client(base_url=base_url)
    try:
        cli.stop(container=id)
        status = "SUCCESS: stopped container " + id
    except:
        status = "ERROR stopping container " + id
    root.redirect("/docker?status="+status)

@dockerMod.route('/docker/remove/<id>', method='GET')
def container_status(id):
    print "removing container:", id
    cli = docker.Client(base_url=base_url)
    try:
        cli.remove_container(id)
        status = "SUCCESS: removed container " + id
    except:
        status = "ERROR: problem removing container " + id
    redirect("/docker?status="+status)
