# AWS Config Remediation PoC

This is a PoC for AWS Config remediation on one targeted account and region using predefined remediation runbook owned by AWS.

Ideally we would enable Config service as a part of AWS Orgnisation services to ensure coberage on all member accounts and regions.

In this poc we demonstrate deployment of managed AWS Config Rule and its predefined remediation action.


## To Apply this

1. Ensure AWS profile has necessary permissions on the target account

from the cli run:

`export AWS_PROFILE=profilename` 

`export AWS_REGION=eu-central-1` 

2. Run Terraform

`terraform init`

`terraform apply`

3. Auto-remediation

Use RDK to create and deploy custom rules

`git clone https://github.com/awslabs/aws-config-rdk`






