# AIOps Quality Project

## Description

A FastAPI service with a **drift detector**, **Prometheus metrics**, a **Helm chart**, and **GitOps deployment** via ArgoCD.
The **CI pipeline in GitHub** performs: `retrain → build → push → bump Helm chart`.

## Local Run

```bash
python -m venv .venv && . .venv/Scripts/activate
pip install -r requirements.txt
python model/train.py
uvicorn app.main:app --reload
# Example request: POST /predict {"data": [13.1,9.9,16.11,25.2]}
```

## Helm Deploy (Cluster)

```bash
helm upgrade --install aiops ./helm -n application --create-namespace \
--set image.repository=docker.io/karimorozova/quality-service \
--set image.tag=latest
```

## ArgoCD

- The application is defined in `argocd/application.yaml` with **auto-sync enabled**.
- The reviewer (or user) should replace `repoURL` with their own Git repository URL.

## Monitoring

- `/metrics` — automatically exposed (via `prometheus_fastapi_instrumentator`)
- Grafana dashboard is located at `grafana/dashboards.json` (shows **request rate**, **P95 latency**, and **drift detector activations** via the metric `app_drift_events_total`).

## Logs

- The service’s **stdout logs** are collected by **Promtail** (default DaemonSet configuration).
- Additional annotations are provided for the Service/Pod for better log identification.

## GitLab CI

- The `retrain-model` job can be **triggered manually**, **on schedule**, or **on push**.
- Steps: `retrain → build → push → update image.tag in Helm → commit`.
- Required variables:

  - `CI_REGISTRY_USER`
  - `CI_REGISTRY_PASSWORD`
    (and an enabled **Container Registry** in the GitLab project)
