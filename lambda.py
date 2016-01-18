import boto3

ec2 = boto3.client('ec2')

def lambda_handler(event, context):
    reservations = ec2.describe_instances(
        Filters=[
            {'Name': 'tag-key', 'Values': ['9pmstop']},
        ]
    ).get(
        'Reservations', []
    )

    # use the `sum` function to flatten the list-of-lists-of-instances into a
    # list of instances
    instances = sum(
        [
            [instance for instance in reservation['Instances']]
            for reservation in reservations
        ], [])

    print "Found %d instances to be shut down at 9pm" % len(instances)

    # pull out all instance IDs from the instance list
    instance_ids = [ins['InstanceId'] for ins in instances]
    response = ec2.stop_instances(InstanceIds=instance_ids)
    print "Stopping %d instances NOW" % len(response['StoppingInstances'])
