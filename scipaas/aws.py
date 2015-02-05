import boto, sys
import boto.ec2
import datetime
import math

class ec2(object):
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
                status['id:'] = inst.id
                status['type'] = inst.instance_type
                status['state'] = inst.state
                status['ip'] = inst.ip_address
                status['public_dns_name'] = inst.public_dns_name
                status['launch_time'] = inst.launch_time
        return status

    def uptime(self,launch_time):
        """given launch time return uptime"""
        lt_datetime = datetime.datetime.strptime(launch_time[:-5], '%Y-%m-%dT%H:%M:%S')
        lt_delta = datetime.datetime.utcnow() - lt_datetime
        return str(lt_delta)

    def charge(self,uptime):
        (hour,minute,second) = uptime.split(':')
        return (int(hour)+1)*self.rate
