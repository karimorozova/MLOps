terraform {
  required_version = ">= 1.5.0"

  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = ">= 5.0, < 6.0"
    }
  }
}

provider "aws" {
  region  = var.aws_region
  profile = "goit-terraform"

  default_tags {
    tags = {
      Project   = "kari-hw-course"
      ManagedBy = "terraform"
    }
  }
}

