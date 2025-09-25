terraform {
  backend "s3" {
    bucket = "mlops-tfstate-kari-hw"
    key    = "root/terraform.tfstate"
    region = "us-east-1"
    encrypt = true
  }
}

