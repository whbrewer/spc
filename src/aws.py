import boto, sys
import boto.ec2
from datetime import datetime, timedelta
import math

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
        instances = [i for r in reservations for i in r.instances]
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
        return lt_delta.total_seconds()

    def charge(self,uptime):
        cost = self.uptime(self.launch_time)/3600.*self.rate
        return '${:,.2f}'.format(cost)
