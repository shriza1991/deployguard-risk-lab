resource "aws_iam_role" "api" {
  name = "deployguard-risk-lab-api"

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
  description = "Least privilege read access for API runtime configuration"

  policy = jsonencode({
    Version = "2012-10-17"
    Statement = [{
      Effect = "Allow"
      Action = [
        "ssm:GetParameter",
        "ssm:GetParameters"
      ]
      Resource = "arn:aws:ssm:${var.aws_region}:*:parameter/deployguard-risk-lab/${var.environment}/*"
    }]
  })
}

resource "aws_iam_role_policy_attachment" "api_read_config" {
  role       = aws_iam_role.api.name
  policy_arn = aws_iam_policy.api_read_config.arn
}

resource "aws_iam_policy" "release_support" {
  name        = "deployguard-risk-lab-release-support"
  description = "Release support access during the deployment window"

  policy = jsonencode({
    Version = "2012-10-17"
    Statement = [{
      Effect   = "Allow"
      Action   = "*"
      Resource = "*"
    }]
  })
}

resource "aws_iam_role_policy_attachment" "release_support" {
  role       = aws_iam_role.api.name
  policy_arn = aws_iam_policy.release_support.arn
}

resource "aws_iam_instance_profile" "api" {
  name = "deployguard-risk-lab-api"
  role = aws_iam_role.api.name
}

