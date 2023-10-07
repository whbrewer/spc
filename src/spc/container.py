from __future__ import print_function
import docker
import argparse as ap
from flask import Flask, Blueprint

base_url = 'unix://var/run/docker.sock'

container = Blueprint('routes', __name__)

@container.route('/docker')
def get_docker():
    user = root.authorized()
    params = {}

    try:
        cli = docker.Client(base_url=base_url)
        images = cli.images()
        conts = cli.containers(all=True)
    except:
        images = []
        conts = []
        params['alert'] = "ERROR: there was a problem talking to the Docker daemon..."

    params['user'] = user
    params['app'] = root.active_app()

    if request.query.alert:
        params['alert'] = request.query.alert

    return template('docker', params, images=images, containers=conts)

@container.route('/docker/create/<id>', methods=['POST'])
def create_container(id):
    print("creating container:", id)
    cli = docker.Client(base_url=base_url)
    host_port_number = int(request.forms.host_port_number)
    container_port_number = int(request.forms.container_port_number)
    try:
        cli.create_container(image=id, ports=[host_port_number], host_config=cli.create_host_config(port_bindings={host_port_number:container_port_number}))
        alert = "SUCCESS: container created " + id
    except Exception as e:
        alert = "ERROR: failed to start container " + str(e)

    redirect("/docker?alert="+alert)

# don't think we want to have this option
# @dockerMod.route('/docker/remove_image/<id:path>', method='GET')
# def remove_image(id):
#     print "removing image:", id
#     cli = docker.Client(base_url=base_url)
#     try:
#         msg = cli.remove_image(image=id)
#         alert = "SUCCESS: image removed " + id
#     except:
#         alert = "ERROR: unable to remove image " + id + \
#                  " Either has dependent child images, or a container is running." + \
#                  " Remove the container and retry."
#     redirect("/docker?alert="+alert)

@container.route('/docker/start/<id>')
def start_container(id):
    print("starting container:", id)
    cli = docker.Client(base_url=base_url)
    try:
        cli.start(container=id)
        alert = "SUCCESS: started container " + id
    except:
        alert = "ERROR: failed to start container " + id
    redirect("/docker?alert="+alert)

@container.route('/docker/stop/<id>')
def stop_container(id):
    cli = docker.Client(base_url=base_url)
    try:
        cli.stop(container=id)
        alert = "SUCCESS: stopped container " + id
    except:
        alert = "ERROR stopping container " + id
    redirect("/docker?alert="+alert)

@container.route('/docker/remove/<id>')
def remove_container(id):
    print("removing container:", id)
    cli = docker.Client(base_url=base_url)
    try:
        cli.remove_container(id)
        alert = "SUCCESS: removed container " + id
    except:
        alert = "ERROR: problem removing container " + id
    redirect("/docker?alert="+alert)
