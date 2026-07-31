resource "aws_iam_role" "api" {
  name = "deployguard-risk-lab-api"

  tags = {
    Environment = var.environment
    ManagedBy   = "terraform"
    Service     = "deployguard-api"
  }

  assume_role_policy = jsonencode({
    Version = "2012-10-17"
    Statement = [{
      Effect = "Allow"
      Principal = {
        Service = "ec2.amazonaws.com"
      }
      Action = "sts:AssumeRole"
    }]
  })
}

resource "aws_iam_policy" "api_read_config" {
  name        = "deployguard-risk-lab-api-read-config"
  description = "Read runtime configuration from Parameter Store"

  policy = jsonencode({
    Version = "2012-10-17"
    Statement = [{
      Sid    = "ReadRuntimeParameters"
      Effect = "Allow"
      Action = [
        "ssm:GetParameter",
        "ssm:GetParameters"
      ]
      Resource = "arn:aws:ssm:${var.aws_region}:*:parameter/deployguard-risk-lab/${var.environment}/*"
    }]
  })
}