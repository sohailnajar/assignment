import boto3

def list_security_groups(region_name):
    ec2_client = boto3.client('ec2', region_name=region_name)

    response = ec2_client.describe_security_groups()

    security_groups = response['SecurityGroups']

    return security_groups

def print_security_group_details(security_groups):
    for group in security_groups:
        group_id = group['GroupId']
        group_name = group.get('GroupName', 'N/A')
        vpc_id = group['VpcId']
        description = group.get('Description', 'N/A')

        print(f"Security Group ID: {group_id}")
        print(f"Group Name: {group_name}")
        print(f"VPC ID: {vpc_id}")
        print(f"Description: {description}")
        print("Inbound Rules:")

        for ingress_rule in group['IpPermissions']:
            print(f"  {ingress_rule}")

        print("\n" + "-" * 50 + "\n")

if __name__ == "__main__":
    region_name = 'eu-central-1'

    security_groups = list_security_groups(region_name)

    if security_groups:
        print(f"All security groups in {region_name}:")
        print_security_group_details(security_groups)
    else:
        print("No security groups found.")
