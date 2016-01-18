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

instance_ids = [ins['InstanceId'] for ins in instances]
response = ec.stop_instances(InstanceIds=instance_ids)
print "Stopping %d instances NOW" % len(response['StoppingInstances']

# NOTE: I'd use stronger variable names for better readability.
# e.g. r['Instances'] -> This doesn't let you know that r is a reservation
