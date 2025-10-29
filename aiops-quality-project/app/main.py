from fastapi import FastAPI, Request
import joblib
import numpy as np
from sklearn.datasets import load_iris
import logging
import time
from prometheus_fastapi_instrumentator import Instrumentator
from prometheus_client import Counter

app = FastAPI()
logger = logging.getLogger("uvicorn")
Instrumentator().instrument(app).expose(app)

DRIFT_EVENTS = Counter("app_drift_events_total", "Number of drift detections")

# Load model 
model = joblib.load("model/model.pkl")

# Train statistics 
data = load_iris()
train_mean = np.mean(data.data, axis=0)

DRIFT_THRESHOLD = 0.5  

@app.get("/health")
async def health():
    return {"status": "ok"}


# Predict endpoint 
@app.post("/predict")
async def predict(request: Request):
    body = await request.json()
    features = np.array(body["data"]).reshape(1, -1)

    # Predict
    start_time = time.time()
    pred = model.predict(features)[0]
    latency = time.time() - start_time

    # Logging for Loki
    logger.info(
        f"Prediction requested: {body['data']} → {pred} (latency={latency:.4f}s)"
    )

    # Drift detection
    diff = np.abs(features - train_mean)
    drift_score = float(np.mean(diff))

    drift_detected = drift_score > DRIFT_THRESHOLD

    if drift_detected:
        DRIFT_EVENTS.inc()
        logger.warning(f"Drift detected! drift_score={drift_score:.4f}")

    return {
        "prediction": int(pred),
        "latency": latency,
        "drift_score": drift_score,
        "drift_detected": drift_detected,
    }