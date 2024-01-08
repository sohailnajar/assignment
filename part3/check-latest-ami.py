import boto3

# latest amis by amazon
def get_latest_ami_id(region_name, image_name):
    ec2_client = boto3.client('ec2', region_name=region_name)

    response = ec2_client.describe_images(
        Filters=[{'Name': 'name', 'Values': [image_name]}],
        Owners=['amazon']
    )

    
    images = sorted(response['Images'], key=lambda x: x['CreationDate'], reverse=True)

    if images:
        return images[0]['ImageId']
    else:
        return None

def get_instance_ami_id(ec2_client, instance_id):

    response = ec2_client.describe_instances(InstanceIds=[instance_id])


    ami_id = response['Reservations'][0]['Instances'][0]['ImageId']

    return ami_id

def check_instances_for_latest_ami(region_name, image_name):
    ec2_client = boto3.client('ec2', region_name=region_name)

    latest_ami_id = get_latest_ami_id(region_name, image_name)

    if not latest_ami_id:
        print(f"No AMIs found with the name '{image_name}' in region {region_name}")
        return

    response = ec2_client.describe_instances()

    for reservation in response['Reservations']:
        for instance in reservation['Instances']:
            instance_id = instance['InstanceId']
            instance_ami_id = get_instance_ami_id(ec2_client, instance_id)

            if instance_ami_id == latest_ami_id:
                print(f"Instance {instance_id} is using the latest AMI.")
            else:
                print(f"Instance {instance_id} is not using the latest AMI. Current AMI: {instance_ami_id}, Latest AMI: {latest_ami_id}")

if __name__ == "__main__":

    region_name = 'eu-central-1'
    ami_name = 'al2023-ami-2023.2.20231018.2-kernel-6.1-x86_64' 
    
    check_instances_for_latest_ami(region_name, ami_name)
