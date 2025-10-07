# ArgoCD for Helm-deploy project

This project demonstrates deploying applications on **AWS EKS** using **Terraform**, **Helm**, and **ArgoCD**.
It includes MLflow, MinIO, Prometheus, Loki, and a demo nginx application deployed automatically via ArgoCD.

## 📁 Project Structure

```
MLOps
├── namespaces
│ ├── application
│ │ ├── mlflow.yaml
│ │ ├── mlflow-postgres.yaml
│ │ ├── minio.yaml
│ │ ├── nginx-demo.yaml
│ │ └── ns.yaml
│ └── infra-tools
│ ├── kube-prometheus-stack.yaml
│ ├── loki.yaml
│ └── ns.yaml
├── README.md
```

- `namespaces/application`: Applications deployed to the `application` namespace.
- `namespaces/infra-tools`: ArgoCD tools and monitoring apps deployed to `infra-tools`.
- Each YAML file is an **ArgoCD Application** describing a Helm deployment or Kubernetes resource.

## ⚙️ Prerequisites

- AWS account with IAM user credentials
- AWS CLI configured: `aws configure --profile default`
- Terraform ≥ 1.5
- kubectl
- Helm (for local testing, optional)

## 1️⃣ Deploy ArgoCD via Terraform

1. Navigate to your Terraform project folder (e.g., `MLOps`):

```bash
cd terraform/argocd
```

2. Initialize Terraform:

```bash
terraform init
```

3. Apply Terraform to deploy ArgoCD:

```bash
terraform apply -var "aws_profile=default"
```

4. Verify ArgoCD pods:

```bash
kubectl get pods -n infra-tools
```

- You should see several pods with prefix `argocd-`, e.g., `argocd-server`, `argocd-repo-server`.

## 2️⃣ Access ArgoCD UI

1. Port-forward the ArgoCD server:

```bash
kubectl port-forward svc/argocd-server -n infra-tools 8080:443
```

2. Open in browser:

```
https://localhost:8080
```

3. Login:

- Username: `admin`
- Password: Check the initial password (from Terraform or ArgoCD secret):

```bash
kubectl get secret argocd-initial-admin-secret -n infra-tools -o jsonpath="{.data.password}" | base64 -d
```

## 3️⃣ Verify Git Applications

All applications are automatically synced via ArgoCD.

1. Check Applications:

```bash
kubectl get applications -n infra-tools
```

2. Verify pods are running in `application` namespace:

```bash
kubectl get pods -n application
```

- Expected pods: `mlflow`, `mlflow-postgres`, `minio`, `nginx-demo`, Prometheus, Loki, Grafana, etc.

## 4️⃣ Access Deployed Services

### MLflow UI

Port-forward MLflow service:

```bash
kubectl port-forward svc/mlflow -n application 5000:5000
```

- Access MLflow: `http://localhost:5000`

### MinIO UI

Port-forward MinIO service:

```bash
kubectl port-forward svc/minio -n application 9000:9000
```

- Access MinIO: `http://localhost:9000`
- Credentials (from valuesObject):

  - Username: `minio`
  - Password: `minio123`

### Prometheus & Grafana

Port-forward Grafana service:

```bash
kubectl port-forward svc/kube-prometheus-stack-grafana -n infra-tools 3000:80
```

- Access Grafana: `http://localhost:3000`
- Admin password: `prom-operator` (from valuesObject)

## 5️⃣ Notes on ArgoCD Applications

- All applications use **auto-sync** and **self-heal**:

  ```yaml
  syncPolicy:
    automated:
      prune: true
      selfHeal: true
  ```

- Helm charts are referenced via `repoURL`, `chart`, `targetRevision`.
- Namespace creation is automatic via `syncOptions: CreateNamespace=true`.

## 6️⃣ References

- [ArgoCD Docs](https://argo-cd.readthedocs.io/en/stable/)
- [ArtifactHub Helm Charts](https://artifacthub.io/)
- [Bitnami Helm Charts](https://bitnami.com/stacks/helm)

## ✅ Summary

- Terraform deploys ArgoCD into `infra-tools` namespace.
- ArgoCD automatically deploys applications from Git repository via Helm charts.
- All apps are auto-synced, self-healing, and namespaces are created automatically.
- Services are accessible via port-forward.
