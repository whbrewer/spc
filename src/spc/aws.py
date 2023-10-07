from __future__ import print_function
from __future__ import absolute_import
import boto, sys, traceback, time, argparse as ap
import boto.ec2
from datetime import datetime

from .model import db, users, aws_creds, aws_instances
from . import config

from flask import Flask, Blueprint

aws = Blueprint('routes', __name__)

def aws_conn(id):
    """create a connection to the EC2 machine and return the handle"""
    user = root.authorized()
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
        self.conn = boto.ec2.connect_to_region(region, aws_access_key_id=key,
                                               aws_secret_access_key=secret)
        self.instance = instance
        self.rate = float(rate)

    def start(self):
        self.conn.start_instances(instance_ids=[self.instance])

    def stop(self):
        self.conn.stop_instances(instance_ids=[self.instance])

    def status(self):
        reservations = self.conn.get_all_instances()
        status = {}
        for r in reservations:
            for inst in r.instances:
                if inst.id == self.instance:
                    status['id:'] = inst.id
                    status['type'] = inst.instance_type
                    status['state'] = inst.state
                    status['ip'] = inst.ip_address
                    status['public_dns_name'] = inst.public_dns_name
                    status['launch_time'] = inst.launch_time
                    self.launch_time = inst.launch_time
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

@aws.route('/aws')
def get_aws():
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

@aws.route('/aws/creds', methods=['POST'])
def post_aws_creds():
    user = root.authorized()
    a = request.forms.account_id
    s = request.forms.secret
    k = request.forms.key
    uid = users(user=user).id
    db.aws_creds.insert(account_id=a, secret=s, key=k, uid=uid)
    db.commit()
    redirect('/aws')

@aws.route('/aws/creds/<id>', methods=['DELETE'])
def aws_cred_del(id):
    root.authorized()
    del db.aws_creds[id]
    db.commit()
    redirect('/aws')

@aws.route('/aws/instance', methods=['POST'])
def create_instance():
    """create instance"""
    user = root.authorized()
    instance = request.forms.instance
    itype = request.forms.itype
    region = request.forms.region
    rate = request.forms.rate
    uid = users(user=user).id
    db.aws_instances.insert(instance=instance, itype=itype, region=region, rate=rate, uid=uid)
    db.commit()
    redirect('/aws')

@aws.route('/aws/instance/<aid>', methods=['DELETE'])
def del_instance(aid):
    root.authorized()
    try:
        del aws_instances[aid]
        db.commit()
        return "true"
    except:
        exc_type, exc_value, exc_traceback = sys.exc_info()
        print(traceback.print_exception(exc_type, exc_value, exc_traceback))
        return "false"

@aws.route('/aws/status/<aid>')
def aws_status(aid):
    user = root.authorized()
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

@aws.route('/aws/<aid>', methods=['POST'])
def aws_start(aid):
    root.authorized()
    a = aws_conn(aid)
    a.start()
    # takes a few seconds for the status to change on the Amazon end
    time.sleep(15)

@aws.route('/aws/<aid>', methods=['DELETE'])
def aws_stop(aid):
    root.authorized()
    a = aws_conn(aid)
    a.stop()
    # takes a few seconds for the status to change on the Amazon end
    time.sleep(10)
