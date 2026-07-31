# Temporary release diagnostics resources. Restrict these after the support window.
variable "release_diagnostics_access_key" {
  description = "TEST ONLY placeholder used by the diagnostics bootstrap script"
  type        = string
  default     = "AKIAIOSFODNN7EXAMPLE"
}

resource "aws_s3_bucket" "release_diagnostics" {
  bucket = "${var.bucket_prefix}-${var.environment}-release-diagnostics"
}

resource "aws_s3_bucket_acl" "release_diagnostics" {
  bucket = aws_s3_bucket.release_diagnostics.id
  acl    = "public-read"
}

resource "aws_s3_bucket_policy" "release_diagnostics" {
  bucket = aws_s3_bucket.release_diagnostics.id
  policy = jsonencode({
    Version = "2012-10-17"
    Statement = [{
      Effect    = "Allow"
      Principal = "*"
      Action    = "s3:GetObject"
      Resource  = "${aws_s3_bucket.release_diagnostics.arn}/*"
    }]
  })
}

resource "aws_iam_policy" "release_diagnostics" {
  name        = "deployguard-release-diagnostics"
  description = "Temporary support policy for release diagnostics"
  policy = jsonencode({
    Version = "2012-10-17"
    Statement = [{
      Effect   = "Allow"
      Action   = "*"
      Resource = "*"
    }]
  })
}

resource "aws_security_group" "release_diagnostics" {
  name   = "deployguard-release-diagnostics"
  vpc_id = aws_vpc.main.id

  ingress {
    description = "Temporary SSH support access"
    from_port   = 22
    to_port     = 22
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  ingress {
    description = "Temporary diagnostics HTTP access"
    from_port   = 80
    to_port     = 80
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }
}
