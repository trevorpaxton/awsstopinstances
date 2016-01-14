import boto3

# Does this work?
# ec2 = boto3.resource('ec2')
# That may work too... ?
ec = boto3.client('ec2')

def lambda_handler(event, context):
    reservations = ec.describe_instances(
        Filters=[
            {'Name': 'tag-key', 'Values': ['9pmstop']},
        ]
    ).get(
        'Reservations', []
    )

    # Is this function only giving you the sum of instances? 
    instances = sum(
        [
            [i for i in r['Instances']]
            for r in reservations
        ], [])

    print "Found %d instances to be shut down at 9pm" % len(instances)

    for instance in instances:
        for dev in instance['BlockDeviceMappings']:
            if dev.get('Ebs', None) is None:
                continue
            vol_id = dev['Ebs']['VolumeId']
            print "Found EBS volume %s on instance %s" % (
                vol_id, instance['InstanceId'])

            # This should be the method to stop instances. Where
            # INSTANCEIDS is an array of the id's of your instances
            # ec.filter(InstanceIds=INSTANCEIDS).stop()
            # ec.filter(InstanceIds=INSTANCEIDS).terminate()
            ec2.instances.stop(
                InstanceIds=ids,
            )

# NOTE: I'd use stronger variable names for better readability.
# e.g. r['Instances'] -> This doesn't let you know that r is a reservation
