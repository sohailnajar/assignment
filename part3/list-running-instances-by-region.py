import boto3

def list_running_instances(region_name):

    ec2_client = boto3.client('ec2', region_name=region_name)


    # Use describe_instances to get a list of all instances with 'running' state
    response = ec2_client.describe_instances(Filters=[{'Name': 'instance-state-name', 'Values': ['running']}])

    running_instances = []

    for reservation in response['Reservations']:
        for instance in reservation['Instances']:
            running_instances.append(instance)

    return running_instances

def print_instance_details(instances):
    for instance in instances:
        instance_id = instance['InstanceId']
        state = instance['State']['Name']

        print(f"Instance ID: {instance_id}, State: {state}")

# Example usage
region_name = 'eu-central-1'

running_instances = list_running_instances(region_name)
print(f"Running instances in {region_name}:")
print_instance_details(running_instances)
