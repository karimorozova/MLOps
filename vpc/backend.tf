terraform {
  backend "s3" {
    bucket = "mlops-tfstate-kari-hw"
    key    = "vpc/terraform.tfstate"
    region = "us-east-1"
  }
}

