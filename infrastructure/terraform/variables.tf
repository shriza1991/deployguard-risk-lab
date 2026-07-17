variable "aws_region" {
  type    = string
  default = "us-east-1"
}

variable "environment" {
  type    = string
  default = "dev"
}

variable "vpc_cidr" {
  type    = string
  default = "10.40.0.0/16"
}

variable "public_subnet_cidrs" {
  type    = list(string)
  default = ["10.40.0.0/24", "10.40.1.0/24"]
}

variable "private_subnet_cidrs" {
  type    = list(string)
  default = ["10.40.10.0/24", "10.40.11.0/24"]
}

variable "availability_zones" {
  type    = list(string)
  default = ["us-east-1a", "us-east-1b"]
}

variable "allowed_ingress_cidrs" {
  type        = list(string)
  description = "Approved corporate or VPN CIDR ranges."
  default     = ["203.0.113.10/32"]
}

variable "instance_type" {
  type    = string
  default = "t3.micro"
}

variable "bucket_prefix" {
  type    = string
  default = "deployguard-risk-lab"
}

