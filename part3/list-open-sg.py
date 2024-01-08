import boto3

def get_insecure_security_groups(region_name):
    ec2_client = boto3.client('ec2', region_name=region_name)


    response = ec2_client.describe_security_groups()

    insecure_security_groups = []

    for group in response['SecurityGroups']:
        for ingress_rule in group['IpPermissions']:
            if any(ip_range['CidrIp'] == '0.0.0.0/0' or ip_range['CidrIp'] == '::/0' for ip_range in ingress_rule.get('IpRanges', [])):
                insecure_security_groups.append(group)

    return insecure_security_groups

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

    insecure_security_groups = get_insecure_security_groups(region_name)

    if insecure_security_groups:
        print("Security groups with overly permissive inbound rules:")
        print_security_group_details(insecure_security_groups)
    else:
        print("No security groups with overly permissive inbound rules found.")
