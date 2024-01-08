# Assessing cloud
Writing one off scripts is not a recommended way to assess the Cloud environment. AWS offers services such AWS Config and various OSS (e.g. CloudQuery etc.) or enterprise (e.g. Palo Alto Prisma etc.) tools that can be utilized to continuously monitor cloud environments using codified policies.


This ensures consistent monitoring infrastructure along with ability to execute remediation based on conditions set by the security or SRE team.


Following are basic python scripts that use AWS Boto3 library to query the cloud environment. I have also added `aws cli` commands that can be used to the same effect.


Additionally, I also have included setup of AWS Config service and rdk to deploy custom rules.

## Scripts

Ensure boto3 is installed in your python environmet

`pip install boto3`

### Instance Security
* List all running instances in a specified region.

`python3 list-running-instances-by-region.py`

`aws ec2 describe-instances --region eu-central-1`

* Check if instances are using the latest Amazon Machine Image (AMI).

`python3 check-latest-ami.py`

`aws ec2 describe-instances --query "Reservations[].Instances[].[InstanceId, ImageId, State.Name, LaunchTime]" --output table --region eu-central-1`

* Implement a function to update instances with outdated AMIs.

The updating of an instance would require a new instance to be created. IaC can enforce latest AMI be used when creating a cluster. if an instance is part of an Auto Scaling Cluster, launch config can also can ensure latest AMI used when provisiong new instances. 

* List all environments using instances tags (dev, prod, staging)

`python3 list-instances.tag.py`

`aws ec2 describe-instances --query 'Reservations[].Instances[].[InstanceId,Tags[?Key==`YourTagName`].Value[]]' --output table --region eu-central-1`

### Network Security
* List all security groups in a specified region.

`python3 list-all-sg.py`

`aws ec2 describe-security-groups --region eu-central-1`

*  Identify security groups with overly permissive inbound rules (allowing all traffic) and
print their details.

`python3 list-open-sg.py`

`aws ec2 describe-security-groups --query 'SecurityGroups[?IpPermissions[0].IpRanges[0].CidrIp == `0.0.0.0/0` && IpPermissions[0].FromPort == `22`]' --output table --region eu-central-1`

* Implement a function to update security groups to restrict overly permissive rules

While such a function can be written, a better approach IMO would be to utilize a service like AWS Config, it allows us to write policies along with auto-remediation as demonstrated in config demo.