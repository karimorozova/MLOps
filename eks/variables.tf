variable "cluster_name" {
  type    = string
  default = "kari-hw-eks"
}

variable "cluster_version" {
  type    = string
  default = "1.31"
}

variable "vpc_id" {
  type = string
}
variable "subnet_ids" {
  type = list(string)
}

variable "node_groups" {
  type = any
 }

variable "tags" {
  type    = map(string)
  default = {}
}

variable "aws_region" {
  type    = string
  default = "us-east-1"
}
