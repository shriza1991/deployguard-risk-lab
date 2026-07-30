resource "aws_cloudwatch_log_group" "api" {
  name              = "/aws/app/deployguard-risk-lab-${var.environment}"
  retention_in_days = 90

  tags = {
    Environment = var.environment
    Service     = "risk-lab-api"
    ManagedBy   = "terraform"
  }
}
