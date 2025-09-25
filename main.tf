module "vpc" {
  source = "./vpc"
}

module "eks" {
  source = "./eks"

  cluster_name    = var.cluster_name
  cluster_version = var.cluster_version

  vpc_id     = module.vpc.vpc_id
  subnet_ids = module.vpc.public_subnets

  node_groups = {
    cpu_nodes = {
      instance_types   = ["t3.micro"]
      desired_size = 2
      min_size     = 1
      max_size     = 2
    }
    gpu_nodes = {
      instance_types   = ["g4dn.xlarge"]
      desired_size = 0
      min_size     = 0
      max_size     = 1
    }
  }

  tags = {
    Environment = "dev"
    Terraform   = "true"
  }
}

