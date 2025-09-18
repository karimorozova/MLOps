variable "cluster_name" {
  description = "EKS cluster name"
  type        = string
  default     = "kari"
}

variable "cluster_version" {
  description = "EKS cluster version"
  type        = string
  default     = "1.31"
}

variable "aws_region" {
  description = "Default AWS region"
  type        = string
  default     = "us-east-1"
}

