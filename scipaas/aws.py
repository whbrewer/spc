import boto, sys
import boto.ec2

class ec2(object):
    """start, stop, and status of EC2 instances"""

    def __init__(self, key, secret, account_id, instance, region):
        # Connect to region
        self.conn = boto.ec2.connect_to_region(region, aws_access_key_id=key, 
                                               aws_secret_access_key=secret)
        self.instance = instance

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
