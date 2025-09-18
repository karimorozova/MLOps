terraform {
  backend "s3" {
    bucket         = "mlops-tfstate-kari"
    key            = "eks/terraform.tfstate"
    region         = "us-east-1"
    encrypt        = true
     }
}

