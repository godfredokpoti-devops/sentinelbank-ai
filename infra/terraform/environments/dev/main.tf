terraform {
  required_version = ">= 1.7.0"
  required_providers {
    aws = { source = "hashicorp/aws", version = "~> 5.0" }
  }
}

provider "aws" { region = var.aws_region }

data "aws_caller_identity" "current" {}

module "network" {
  source = "../../modules/network"
  name   = var.name
  cidr   = "10.42.0.0/16"
}

module "ecr" {
  source = "../../modules/ecr"
  name   = var.name
}

module "kms" {
  source = "../../modules/kms"
  name   = var.name
}

module "s3" {
  source = "../../modules/s3"
  name   = var.name
  kms_key_arn = module.kms.key_arn
}

# EKS and RDS modules are intentionally separated because production banks
# typically apply independent lifecycle, network, backup, and approval controls.
