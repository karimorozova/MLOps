# MLOps Experiments with MLflow and Prometheus

This project demonstrates a complete MLOps lifecycle using **MLflow** for experiment tracking and **Prometheus PushGateway** for metrics monitoring.

## Architecture

The project includes the following components:

- **MLflow Tracking Server** – for logging experiments, parameters, and metrics
- **PostgreSQL** – database for storing experiment metadata
- **MinIO** – S3-compatible storage for model artifacts
- **Prometheus PushGateway** – for collecting metrics from experiments
- **Grafana** – for metrics visualization

## Project Structure

```
mlops-experiments/
├── argocd/
│   └── applications/
│       ├── mlflow.yaml          # MLflow Tracking Server
│       ├── minio.yaml           # MinIO S3 storage
│       ├── postgres.yaml        # PostgreSQL database
│       └── pushgateway.yaml     # Prometheus PushGateway
├── experiments/
│   ├── train_and_push.py        # Script to run experiments
│   └── requirements.txt         # Python dependencies
├── best_model/                  # The best model (created after running experiments)
└── README.md                    # This file
```

## Infrastructure Deployment

### 1. Deployment via ArgoCD

All services are deployed declaratively using **ArgoCD Applications**:

```bash
# Check if ArgoCD is available
kubectl get applications -n infra-tools

# If necessary, create Applications manually
kubectl apply -f argocd/applications/
```

### 2. Check Deployment Status

```bash
# Check pod status
kubectl get pods -n application
kubectl get pods -n monitoring

# Check services
kubectl get svc -n application
kubectl get svc -n monitoring
```

## Local Environment Setup

### 1. Create a virtual environment

```bash
cd experiments/
python3 -m venv venv
source venv/bin/activate  # Linux/macOS
# or
venv\Scripts\activate     # Windows
```

### 2. Install dependencies

```bash
pip install -r requirements.txt
```

## 🌐 Port-Forward Configuration

To access cluster services locally, set up port-forwarding:

```bash
# MLflow UI
kubectl port-forward svc/mlflow 5000:5000 -n application

# MinIO (optional)
kubectl port-forward svc/minio 9000:9000 -n application

# PushGateway
kubectl port-forward svc/pushgateway 9091:9091 -n monitoring

# PostgreSQL (optional)
kubectl port-forward svc/mlflow-postgres-postgresql 5432:5432 -n application
```

## Running Experiments

### 1. Run the script

```bash
cd experiments/
python train_and_push.py
```

### 2. What the script does

The `train_and_push.py` script performs the following steps:

1. **Loads the Iris dataset** – a standard classification dataset
2. **Runs 6 experiments** with different parameters:

   - learning_rate: 0.001, 0.01, 0.05, 0.1
   - epochs: 50, 100, 200

3. **For each experiment:**

   - Logs parameters to MLflow
   - Trains a Logistic Regression model
   - Calculates metrics (accuracy, loss)
   - Logs metrics to MLflow
   - Saves the model as an artifact
   - Sends metrics to PushGateway

4. **Finds the best model** based on accuracy
5. **Saves the best model** in the `best_model/` directory

### 3. Expected output

After a successful run, you’ll see:

```
Experiment 1/6: learning_rate=0.01, epochs=50
Accuracy: 0.9667, Loss: 0.1234
Metrics sent to PushGateway for run_id: 1309...

...

 Best result:
   Run ID: def456...
   Learning Rate: 0.01
   Epochs: 100
   Accuracy: 0.9667
   Loss: 0.0987

✅ Best model saved to best_model/
```

## Viewing Results

### 1. MLflow UI

Open your browser and go to:

```
http://localhost:5000
```

In the MLflow UI you can:

- View all experiments
- Compare metrics between different runs
- Download models
- Inspect parameters of each experiment

### 2. Grafana Metrics

In Grafana, go to **Explore → Prometheus** and run the following queries:

```promql
# Accuracy metric
mlflow_accuracy

# Loss metric
mlflow_loss

# Metrics with labels
mlflow_accuracy{experiment="Iris Classification Experiments"}
```

### 3. PushGateway UI

To check metrics directly in PushGateway:

```
http://localhost:9091
```

## System Validation

### 1. Check MLflow

```bash
# View MLflow logs
kubectl logs -n application deployment/mlflow

# Check availability
curl http://localhost:5000/health
```

### 2. Check PostgreSQL

```bash
# Connect to the database
psql "postgresql://mlflow:mlflowpass@localhost:5432/mlflow"

# List tables
\dt

# View experiments
SELECT * FROM experiments;
```

### 3. Check MinIO

```bash
# Check bucket
curl http://localhost:9000/mlflow-artifacts/
```

### 4. Check PushGateway

```bash
# Check metrics
curl http://localhost:9091/metrics
```
