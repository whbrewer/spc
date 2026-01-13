import argparse as ap
import datetime

import docker
from bottle import Bottle, jinja2_template as template, redirect, request

base_url = 'unix://var/run/docker.sock'

def bind(app):
    global root
    root = ap.Namespace(**app)

routes = Bottle()


def _to_timestamp(value):
    if isinstance(value, (int, float)):
        return int(value)
    if isinstance(value, str):
        ts = value.rstrip('Z')
        if '.' in ts:
            ts = ts.split('.')[0]
        try:
            return int(datetime.datetime.fromisoformat(ts).timestamp())
        except ValueError:
            return 0
    return 0


def _client():
    return docker.DockerClient(base_url=base_url)

@routes.get('/docker')
def get_docker():
    user = root.authorized()
    params = {}

    try:
        cli = _client()
        images = []
        for image in cli.images.list():
            attrs = image.attrs or {}
            images.append(
                {
                    'Id': attrs.get('Id', image.id),
                    'RepoTags': attrs.get('RepoTags', []) or [],
                    'Created': _to_timestamp(attrs.get('Created')),
                    'Size': attrs.get('Size', 0),
                }
            )
        conts = []
        for container in cli.containers.list(all=True):
            attrs = container.attrs or {}
            status = attrs.get('State', {}).get('Status', container.status or '')
            if status:
                status = status.capitalize()
            conts.append(
                {
                    'Id': attrs.get('Id', container.id),
                    'Image': attrs.get('Config', {}).get('Image', ''),
                    'Command': attrs.get('Path', ''),
                    'Created': _to_timestamp(attrs.get('Created')),
                    'Status': status,
                    'Names': [attrs.get('Name', '/' + container.name)],
                }
            )
    except:
        images = []
        conts = []
        params['alert'] = "ERROR: there was a problem talking to the Docker daemon..."

    params['user'] = user
    params['app'] = root.active_app()

    if request.query.alert:
        params['alert'] = request.query.alert

    return template('docker', params, images=images, containers=conts)

@routes.post('/docker/create/<id>')
def create_container(id):
    print("creating container:", id)
    cli = _client()
    host_port_number = int(request.forms.host_port_number)
    container_port_number = int(request.forms.container_port_number)
    try:
        ports = {container_port_number: host_port_number}
        cli.containers.run(id, detach=True, ports=ports)
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

@routes.get('/docker/start/<id>')
def start_container(id):
    print("starting container:", id)
    cli = _client()
    try:
        cli.containers.get(id).start()
        alert = "SUCCESS: started container " + id
    except:
        alert = "ERROR: failed to start container " + id
    redirect("/docker?alert="+alert)

@routes.get('/docker/stop/<id>')
def stop_container(id):
    cli = _client()
    try:
        cli.containers.get(id).stop()
        alert = "SUCCESS: stopped container " + id
    except:
        alert = "ERROR stopping container " + id
    redirect("/docker?alert="+alert)

@routes.get('/docker/remove/<id>')
def remove_container(id):
    print("removing container:", id)
    cli = _client()
    try:
        cli.containers.get(id).remove()
        alert = "SUCCESS: removed container " + id
    except:
        alert = "ERROR: problem removing container " + id
    redirect("/docker?alert="+alert)
