variable "cluster_name" {
  description = "EKS Cluster name"
  type        = string
  default     = "kari-hw-eks"
}

variable "cluster_version" {
  description = "EKS Kubernetes version"
  type        = string
  default     = "1.31"
}

variable "aws_region" {
  description = "AWS Region"
  type        = string
  default     = "us-east-1"
}
