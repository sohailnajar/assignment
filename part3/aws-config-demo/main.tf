### Enable AWS Config Recorder
resource "aws_config_configuration_recorder" "foo" {
  name     = "CloudSecRecorder"
  role_arn = aws_iam_role.this.arn
}


### Check if SG is open to 0.0.0.0/0
resource "aws_config_config_rule" "this" {
  name = "SGCheckPermissive"

  source {
    owner             = "AWS"
    source_identifier = "VPC_SG_OPEN_ONLY_TO_AUTHORIZED_PORTS"
  }
  depends_on = [aws_config_configuration_recorder.foo]
}
### Ensure encyption is enabled
resource "aws_config_remediation_configuration" "this" {
  config_rule_name = aws_config_config_rule.this.name
  resource_type    = "AWS::EC2::SecurityGroup"
  target_type      = "SSM_DOCUMENT"
  target_id {
    attribute_name = "security_group_id"
    value          = aws_security_group.example.id
  }
  target_version   = "1"

  parameter {
    name           = "authorizedTcpPorts"
    resource_value = "443"
  }

  automatic                  = true
  maximum_automatic_attempts = 10
  retry_attempt_seconds      = 200

  execution_controls {
    ssm_controls {
      concurrent_execution_rate_percentage = 25
      error_percentage                     = 20
    }
  }
}


