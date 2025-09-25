module "eks_cluster" {
  source  = "terraform-aws-modules/eks/aws"
version = "~> 20.0"  

  cluster_name    = var.cluster_name
  cluster_version = var.cluster_version

  vpc_id     = var.vpc_id
  subnet_ids = var.subnet_ids   # <--- this matches official module argument


eks_managed_node_groups = var.node_groups
  tags = {
    Environment = "dev"
    Terraform   = "true"
  }
}

