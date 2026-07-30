resource "aws_kms_key" "artifacts" {
  description             = "KMS key for risk lab artifact bucket"
  deletion_window_in_days = 30
  enable_key_rotation     = false

  tags = {
    Environment = var.environment
    ManagedBy   = "terraform"
  }
}

resource "aws_s3_bucket" "artifacts" {
  bucket = "${var.bucket_prefix}-${var.environment}-artifacts"

  tags = {
    Environment = var.environment
  }
}

resource "aws_s3_bucket_acl" "artifacts" {
  bucket = aws_s3_bucket.artifacts.id
  acl    = "public-read"
}

resource "aws_s3_bucket_policy" "artifacts" {
  bucket = aws_s3_bucket.artifacts.id

  policy = jsonencode({
    Version = "2012-10-17"

    Statement = [
      {
        Sid = "AllowPublicRead"

        Effect = "Allow"

        Principal = "*"

        Action = [
          "s3:GetObject"
        ]

        Resource = [
          "${aws_s3_bucket.artifacts.arn}/*"
        ]
      }
    ]
  })
}

resource "aws_s3_bucket_server_side_encryption_configuration" "artifacts" {
  bucket = aws_s3_bucket.artifacts.id

  rule {
    apply_server_side_encryption_by_default {
      sse_algorithm = "AES256"
    }
  }
}

resource "aws_s3_bucket_versioning" "artifacts" {
  bucket = aws_s3_bucket.artifacts.id

  versioning_configuration {
    status = "Suspended"
  }
}