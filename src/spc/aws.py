from bottle import Bottle, jinja2_template as template, redirect, request
import argparse as ap
import sys
import time
import traceback

try:
    import boto3
    from botocore.exceptions import BotoCoreError, ClientError
except Exception as exc:
    boto3 = None
    boto_import_error = exc
from datetime import datetime

from . import config
from .model import aws_creds, aws_instances, db, users

routes = Bottle()

def bind(app):
    global root
    root = ap.Namespace(**app)

def aws_conn(id):
    """create a connection to the EC2 machine and return the handle"""
    user = root.authorized()
    if boto3 is None:
        raise RuntimeError("AWS support unavailable: boto3 import failed: {}".format(boto_import_error))
    uid = users(user=user).id
    try:
        creds = db(db.aws_creds.uid==uid).select().first()
        account_id = creds['account_id']
        secret = creds['secret']
        key = creds['key']
        instances = db(db.aws_instances.id==id).select().first()
        instance = instances['instance']
        region = instances['region']
        rate = instances['rate'] or 0.
        return EC2(key, secret, account_id, instance, region, rate)

    except:
        return template('error', err="problem validating AWS credentials")


class EC2(object):
    """start, stop, and status of EC2 instances"""

    def __init__(self, key, secret, account_id, instance, region, rate):
        # Connect to region
        session = boto3.Session(
            aws_access_key_id=key,
            aws_secret_access_key=secret,
        )
        self.conn = session.client('ec2', region_name=region)
        self.instance = instance
        self.rate = float(rate)

    def start(self):
        self.conn.start_instances(InstanceIds=[self.instance])

    def stop(self):
        self.conn.stop_instances(InstanceIds=[self.instance])

    def status(self):
        try:
            reservations = self.conn.describe_instances(InstanceIds=[self.instance]).get('Reservations', [])
        except (BotoCoreError, ClientError) as exc:
            raise RuntimeError("AWS status failed: {}".format(exc))
        status = {}
        for r in reservations:
            for inst in r.get('Instances', []):
                if inst.get('InstanceId') == self.instance:
                    status['id:'] = inst.get('InstanceId')
                    status['type'] = inst.get('InstanceType')
                    status['state'] = inst.get('State', {}).get('Name')
                    status['ip'] = inst.get('PublicIpAddress')
                    status['public_dns_name'] = inst.get('PublicDnsName')
                    launch_time = inst.get('LaunchTime')
                    if launch_time:
                        status['launch_time'] = launch_time.strftime('%Y-%m-%dT%H:%M:%S')
                        self.launch_time = status['launch_time']
        return status

    def uptime(self,launch_time):
        """given launch time return uptime"""
        lt_datetime = datetime.strptime(launch_time[:-5], '%Y-%m-%dT%H:%M:%S')
        lt_delta = datetime.utcnow() - lt_datetime
        return lt_delta

    def uptime_seconds(self,launch_time):
        """given launch time return uptime"""
        lt_datetime = datetime.strptime(launch_time[:-5], '%Y-%m-%dT%H:%M:%S')
        lt_delta = datetime.utcnow() - lt_datetime
        return lt_delta.total_seconds()

    def charge(self,uptime):
        cost = self.uptime_seconds(self.launch_time)/3600.*self.rate
        return '${:,.2f}'.format(cost)

@routes.get('/aws')
def get_aws():
    if boto3 is None:
        return template('error', err="AWS support unavailable: boto3 import failed.")
    user = root.authorized()
    cid = request.query.cid
    app = request.query.app or root.active_app()
    uid = db(users.user==user).select(users.id).first()
    #creds = db().select(db.aws_creds.ALL)
    creds = db(aws_creds.uid==uid).select()
    # look for aws instances registered by the current user
    # which means first need to get the uid
    instances = db(aws_instances.uid==uid).select()
    params = {}
    params['cid'] = cid
    params['app'] = app
    params['user'] = user
    if request.query.status:
        params['status'] = request.query.status
    return template('aws', params, creds=creds, instances=instances)

@routes.post('/aws/creds')
def post_aws_creds():
    user = root.authorized()
    if boto3 is None:
        return template('error', err="AWS support unavailable: boto3 import failed.")
    a = request.forms.account_id
    s = request.forms.secret
    k = request.forms.key
    uid = users(user=user).id
    db.aws_creds.insert(account_id=a, secret=s, key=k, uid=uid)
    db.commit()
    redirect('/aws')

@routes.delete('/aws/creds/<id>')
def aws_cred_del(id):
    root.authorized()
    if boto3 is None:
        return template('error', err="AWS support unavailable: boto3 import failed.")
    del db.aws_creds[id]
    db.commit()
    redirect('/aws')

@routes.post('/aws/instance')
def create_instance():
    """create instance"""
    user = root.authorized()
    if boto3 is None:
        return template('error', err="AWS support unavailable: boto3 import failed.")
    instance = request.forms.instance
    itype = request.forms.itype
    region = request.forms.region
    rate = request.forms.rate
    uid = users(user=user).id
    db.aws_instances.insert(instance=instance, itype=itype, region=region, rate=rate, uid=uid)
    db.commit()
    redirect('/aws')

@routes.delete('/aws/instance/<aid>')
def del_instance(aid):
    root.authorized()
    if boto3 is None:
        return "false"
    try:
        del aws_instances[aid]
        db.commit()
        return "true"
    except:
        exc_type, exc_value, exc_traceback = sys.exc_info()
        print(traceback.print_exception(exc_type, exc_value, exc_traceback))
        return "false"

@routes.get('/aws/status/<aid>')
def aws_status(aid):
    user = root.authorized()
    if boto3 is None:
        return template('error', err="AWS support unavailable: boto3 import failed.")
    cid = request.query.cid
    app = request.query.app
    params = {}
    params['aid'] = aid
    params['cid'] = cid
    params['app'] = app
    params['user'] = user
    params['port'] = config.port

    a = aws_conn(aid)

    if users(user=user).id != aws_instances(aid).uid:
        return template('error', err="access forbidden")

    try:
        astatus = a.status()
        if astatus['state'] == "running":
            astatus['uptime'] = a.uptime(astatus['launch_time'])
            astatus['charge since last boot'] = a.charge(astatus['uptime'])
        return template('aws_status', params, astatus=astatus)
    except:
        exc_type, exc_value, exc_traceback = sys.exc_info()
        print(traceback.print_exception(exc_type, exc_value, exc_traceback))
        return template('error', err="There was a problem connecting to the AWS machine. Check the credentials and make sure the machine is running.")

@routes.post('/aws/<aid>')
def aws_start(aid):
    root.authorized()
    if boto3 is None:
        return template('error', err="AWS support unavailable: boto3 import failed.")
    a = aws_conn(aid)
    a.start()
    # takes a few seconds for the status to change on the Amazon end
    time.sleep(15)

@routes.delete('/aws/<aid>')
def aws_stop(aid):
    root.authorized()
    if boto3 is None:
        return template('error', err="AWS support unavailable: boto3 import failed.")
    a = aws_conn(aid)
    a.stop()
    # takes a few seconds for the status to change on the Amazon end
    time.sleep(10)
