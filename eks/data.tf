data "terraform_remote_state" "vpc" {
  backend = "s3"

  config = {
    bucket = "mlops-tfstate-kari"
    key    = "vpc/terraform.tfstate"
    region = "us-east-1"
  }
}

