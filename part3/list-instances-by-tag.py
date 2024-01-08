import boto3

def list_instances_by_tag(tag_key, tag_value):
    ec2_client = boto3.client('ec2')

    # Use describe_instances to get a list of all instances
    response = ec2_client.describe_instances()

    # Filter instances based on the specified tag
    filtered_instances = []

    for reservation in response['Reservations']:
        for instance in reservation['Instances']:
            tags = {tag['Key']: tag['Value'] for tag in instance.get('Tags', [])}
            if tags.get(tag_key) == tag_value:
                filtered_instances.append(instance)

    return filtered_instances

def print_instance_details(instances):
    for instance in instances:
        instance_id = instance['InstanceId']
        state = instance['State']['Name']
        tags = {tag['Key']: tag['Value'] for tag in instance.get('Tags', [])}

        print(f"Instance ID: {instance_id}, State: {state}, Tags: {tags}")

# Example usage
tag_key = 'env'
tag_value = 'dev'

dev_instances = list_instances_by_tag(tag_key, tag_value)
print(f"Instances in {tag_value} environment:")
print_instance_details(dev_instances)
