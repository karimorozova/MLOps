# EKS VPC Cluster Terraform Project

This project deploys an **Amazon EKS cluster** with **public and private subnets** using **Terraform**, structured in modular directories for VPC and EKS resources.

## Project Structure

```
├── main.tf
├── variables.tf
├── outputs.tf
├── terraform.tf
├── backend.tf
├── vpc/
│   ├── main.tf
│   ├── variables.tf
│   ├── outputs.tf
│   ├── terraform.tf
│   └── backend.tf
├── eks/
│   ├── main.tf
│   ├── variables.tf
│   ├── outputs.tf
│   ├── terraform.tf
│   └── backend.tf
```

- **Root directory**: orchestrates the deployment of modules (`vpc` and `eks`).
- **vpc/**: creates VPC, subnets, route tables, NAT gateways, and security groups.
- **eks/**: deploys the EKS cluster, node groups, and IAM roles for the cluster.

## Prerequisites

- Terraform v1.6+
- AWS CLI configured (`aws configure`)
- kubectl installed
- jq (optional) for JSON parsing

## Step 1: Initialize Terraform in Each Module

1. **Root folder:**

```bash
cd .
terraform init
```

2. **VPC module:**

```bash
cd vpc
terraform init
```

3. **EKS module:**

```bash
cd ../eks
terraform init
```

> This ensures providers and backend configurations are correctly initialized per module.

## Step 2: Plan Terraform Deployment

- **Root folder:**

```bash
terraform plan
```

- **VPC module:**

```bash
cd vpc
terraform plan
```

- **EKS module:**

```bash
cd ../eks
terraform plan
```

## Step 3: Apply Terraform Configuration

- **VPC module:**

```bash
cd vpc
terraform apply
```

- **EKS module:**

```bash
cd ../eks
terraform apply
```

Confirm with `yes` when prompted. Terraform will create:

- VPC with public and private subnets
- Internet Gateway and NAT gateways
- Security groups
- EKS cluster and managed node groups

**Outputs** will include:

```text
eks_cluster_arn
eks_cluster_endpoint
vpc_id
public_subnets
private_subnets
```

## Step 4: Configure `kubectl`

Generate kubeconfig for the EKS cluster:

```bash
aws eks --region <your-region> update-kubeconfig --name <cluster-name>
```

Verify connection:

```bash
kubectl get nodes
```

> If you encounter TLS handshake errors, make sure **public endpoint access** is enabled and security groups allow your IP.

## Step 5: Destroy Infrastructure

To remove all resources:

```bash
terraform destroy
```

> Make sure to save any critical data before destroying resources.

## Notes

- Terraform state is modular and may use S3 backend per module.
- Node groups are managed automatically through EKS.
- Modular structure allows easy extension of additional VPCs, subnets, or node groups.
