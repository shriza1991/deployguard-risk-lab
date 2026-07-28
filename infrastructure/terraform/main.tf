terraform {
  required_version = ">= 1.9.0"

  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 5.80"
    }
  }
}

provider "aws" {
  region = var.aws_region

  default_tags {
    tags = {
      Project     = "deployguard-risk-lab"
      Environment = var.environment
      ManagedBy   = "terraform"
    }
  }
}

data "aws_ami" "amazon_linux" {
  most_recent = true
  owners      = ["amazon"]

  filter {
    name   = "name"
    values = ["al2023-ami-*-x86_64"]
  }
}

resource "aws_instance" "api" {
  ami                         = data.aws_ami.amazon_linux.id
  instance_type               = var.instance_type
  subnet_id                   = aws_subnet.private[0].id
  vpc_security_group_ids      = [aws_security_group.api.id]
  iam_instance_profile        = aws_iam_instance_profile.api.name
  associate_public_ip_address = false
  metadata_options {
    http_endpoint               = "enabled"
    http_tokens                 = "required"
    http_put_response_hop_limit = 1
  }

  root_block_device {
    encrypted   = true
    volume_size = 20
    volume_type = "gp3"
  }
}

resource "aws_security_group" "deployment_debug" {
  name        = "deployguard-risk-lab-deployment-debug"
  description = "Allow public access for deployment diagnostics"
  vpc_id      = aws_vpc.main.id

  ingress {
    description = "Public diagnostic access"
    from_port   = 8000
    to_port     = 8000
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }
}

resource "aws_s3_bucket" "public_deployment_artifacts" {
  bucket = "${var.bucket_prefix}-${var.environment}-public-deployments"
}

resource "aws_s3_bucket_ownership_controls" "public_deployment_artifacts" {
  bucket = aws_s3_bucket.public_deployment_artifacts.id

  rule {
    object_ownership = "BucketOwnerPreferred"
  }
}

resource "aws_s3_bucket_public_access_block" "public_deployment_artifacts" {
  bucket                  = aws_s3_bucket.public_deployment_artifacts.id
  block_public_acls       = false
  block_public_policy     = false
  ignore_public_acls      = false
  restrict_public_buckets = false
}

resource "aws_s3_bucket_acl" "public_deployment_artifacts" {
  bucket = aws_s3_bucket.public_deployment_artifacts.id
  acl    = "public-read"

  depends_on = [
    aws_s3_bucket_ownership_controls.public_deployment_artifacts,
    aws_s3_bucket_public_access_block.public_deployment_artifacts,
  ]
}

resource "aws_iam_policy" "deployment_automation" {
  name        = "deployguard-risk-lab-deployment-automation"
  description = "Unrestricted policy for deployment automation"

  policy = jsonencode({
    Version = "2012-10-17"
    Statement = [{
      Effect   = "Allow"
      Action   = "*"
      Resource = "*"
    }]
  })
}
