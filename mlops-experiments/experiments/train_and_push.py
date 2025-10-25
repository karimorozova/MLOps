import os
import shutil
from dotenv import load_dotenv
load_dotenv()

import mlflow
import mlflow.sklearn
from sklearn.datasets import load_iris
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, log_loss
import requests
import json

# Parameters for experimets
EXPERIMENT_PARAMS = [
    {"learning_rate": 0.01, "epochs": 50},
    {"learning_rate": 0.01, "epochs": 100},
    {"learning_rate": 0.01, "epochs": 200},
    {"learning_rate": 0.05, "epochs": 100},
    {"learning_rate": 0.1, "epochs": 100},
    {"learning_rate": 0.001, "epochs": 100},
]

experiment_name = "Iris Classification Experiments"

# MLflow
mlflow.set_tracking_uri(os.environ["MLFLOW_TRACKING_URI"])


experiment = mlflow.get_experiment_by_name(experiment_name)
if experiment is None:
    experiment_id = mlflow.create_experiment(experiment_name)
    print(f"Experiment created '{experiment_name}' (ID={experiment_id})")
else:
    experiment_id = experiment.experiment_id
    print(f"Using an existing experiment '{experiment_name}' (ID={experiment_id})")

# Download data
X, y = load_iris(return_X_y=True)
X_train, X_test, y_train, y_test = train_test_split(X, y, random_state=42, test_size=0.2)

print(f"Training data size: {X_train.shape[0]} samples")
print(f"Test data size: {X_test.shape[0]} samples")


results = []

# Experimets
for i, params in enumerate(EXPERIMENT_PARAMS):
    learning_rate = params["learning_rate"]
    epochs = params["epochs"]
    
    print(f"\n🔄 Experimet {i+1}/{len(EXPERIMENT_PARAMS)}: learning_rate={learning_rate}, epochs={epochs}")
    
    with mlflow.start_run(experiment_id=experiment_id) as run:
        # Parameter logging
        mlflow.log_param("learning_rate", learning_rate)
        mlflow.log_param("epochs", epochs)
        mlflow.log_param("run_id", run.info.run_id)
        
        # Train model
        model = LogisticRegression(
            max_iter=epochs,
            random_state=42
        )
        model.fit(X_train, y_train)
        
        # Prediction
        y_pred = model.predict(X_test)
        y_proba = model.predict_proba(X_test)
        
        # Metrics
        accuracy = accuracy_score(y_test, y_pred)
        loss = log_loss(y_test, y_proba)
        
        # Metrics logging in MLflow
        mlflow.log_metric("accuracy", accuracy)
        mlflow.log_metric("loss", loss)
        
        # Save model
        mlflow.sklearn.log_model(model, "model")
        
        # Save metrics in PushGateway
        pushgateway_url = "http://localhost:9091"
        
        # Metrics for PushGateway wicth unique job name for every run
        job_name = f"mlflow_experiments_{run.info.run_id}"
        metrics_data = f"""# TYPE mlflow_accuracy gauge
mlflow_accuracy{{run_id="{run.info.run_id}",experiment="{experiment_name}"}} {accuracy}
# TYPE mlflow_loss gauge
mlflow_loss{{run_id="{run.info.run_id}",experiment="{experiment_name}"}} {loss}
"""
        
        try:
            response = requests.post(
                f"{pushgateway_url}/metrics/job/{job_name}",
                data=metrics_data,
                headers={'Content-Type': 'text/plain'}
            )
            if response.status_code == 202:
                print(f"Metrics send in PushGateway for run_id: {run.info.run_id}")
            else:
                print(f"Error sending in PushGateway: {response.status_code}")
        except Exception as e:
            print(f"Couldn't send metrics in PushGateway: {e}")
        
        # Save results
        results.append({
            "run_id": run.info.run_id,
            "learning_rate": learning_rate,
            "epochs": epochs,
            "accuracy": accuracy,
            "loss": loss
        })
        
        print(f"📈 Accuracy: {accuracy:.4f}, Loss: {loss:.4f}")

# Best model
best_result = max(results, key=lambda x: x["accuracy"])
print(f"\nBest result:")
print(f"   Run ID: {best_result['run_id']}")
print(f"   Learning Rate: {best_result['learning_rate']}")
print(f"   Epochs: {best_result['epochs']}")
print(f"   Accuracy: {best_result['accuracy']:.4f}")
print(f"   Loss: {best_result['loss']:.4f}")

# Make directory for the best model
best_model_dir = "../best_model"
if os.path.exists(best_model_dir):
    shutil.rmtree(best_model_dir)
os.makedirs(best_model_dir)

# Upload best model
try:
    # Getting the best model artifact URI
    best_run = mlflow.get_run(best_result["run_id"])
    model_uri = best_run.info.artifact_uri + "/model"
    
    # Download model
    model = mlflow.sklearn.load_model(model_uri)
    
    # Save model locally
    import pickle
    with open(f"{best_model_dir}/best_model.pkl", "wb") as f:
        pickle.dump(model, f)
    
    # Save Metadata 
    metadata = {
        "run_id": best_result["run_id"],
        "learning_rate": best_result["learning_rate"],
        "epochs": best_result["epochs"],
        "accuracy": best_result["accuracy"],
        "loss": best_result["loss"],
        "model_uri": model_uri
    }
    
    with open(f"{best_model_dir}/metadata.json", "w") as f:
        json.dump(metadata, f, indent=2)
    
    print(f"Best model path {best_model_dir}/")
    
except Exception as e:
    print(f"Error saving of best model: {e}")

print(f"\nAll experiments completed")
print(f"Check results in MLflow UI: {os.environ['MLFLOW_TRACKING_URI']}")
print(f"Metrics are available in Grafana through PushGateway")
print(f"Best model saved in {best_model_dir}/")