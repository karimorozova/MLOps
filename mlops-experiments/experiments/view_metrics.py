#!/usr/bin/env python3

import requests
import re
from datetime import datetime

def get_metrics():
    """Get metrics from PushGateway"""
    try:
        response = requests.get('http://localhost:9091/metrics')
        response.raise_for_status()
        return response.text
    except Exception as e:
        print(f"Connection error PushGateway: {e}")
        return None

def parse_mlflow_metrics(metrics_text):
    """Parse MLflow metrics from text"""
    mlflow_metrics = {}
    
    # Find all mlflow_accuracy metrics
    accuracy_pattern = r'mlflow_accuracy\{([^}]+)\} (\d+\.?\d*)'
    accuracy_matches = re.findall(accuracy_pattern, metrics_text)
    
    for labels, value in accuracy_matches:
        # Parse labels
        label_dict = {}
        for label in labels.split(','):
            if '=' in label:
                key, val = label.split('=', 1)
                label_dict[key.strip()] = val.strip('"')
        
        run_id = label_dict.get('run_id', 'unknown')
        experiment = label_dict.get('experiment', 'unknown')
        
        if run_id not in mlflow_metrics:
            mlflow_metrics[run_id] = {
                'experiment': experiment,
                'accuracy': None,
                'loss': None
            }
        
        mlflow_metrics[run_id]['accuracy'] = float(value)
    
    # Find all mlflow_loss metrics
    loss_pattern = r'mlflow_loss\{([^}]+)\} (\d+\.?\d*)'
    loss_matches = re.findall(loss_pattern, metrics_text)
    
    for labels, value in loss_matches:
        # Parse labels
        label_dict = {}
        for label in labels.split(','):
            if '=' in label:
                key, val = label.split('=', 1)
                label_dict[key.strip()] = val.strip('"')
        
        run_id = label_dict.get('run_id', 'unknown')
        
        if run_id in mlflow_metrics:
            mlflow_metrics[run_id]['loss'] = float(value)
    
    return mlflow_metrics

def display_metrics(mlflow_metrics):
    """Display metrics in table"""
    if not mlflow_metrics:
        print("MLflow metrics not found")
        return
    
    print("\nMLflow Metrics from PushGateway")
    print("=" * 80)
    print(f"{'Run ID':<40} {'Experiment':<30} {'Accuracy':<10} {'Loss':<10}")
    print("-" * 80)
    
    for run_id, metrics in mlflow_metrics.items():
        experiment = metrics['experiment'][:28] + "..." if len(metrics['experiment']) > 30 else metrics['experiment']
        accuracy = f"{metrics['accuracy']:.4f}" if metrics['accuracy'] is not None else "N/A"
        loss = f"{metrics['loss']:.4f}" if metrics['loss'] is not None else "N/A"
        
        print(f"{run_id:<40} {experiment:<30} {accuracy:<10} {loss:<10}")
    
    print("-" * 80)
    print(f"All experiments: {len(mlflow_metrics)}")
    
    # Find best result
    if mlflow_metrics:
        best_run = max(mlflow_metrics.items(), key=lambda x: x[1]['accuracy'] if x[1]['accuracy'] is not None else 0)
        print(f"Best result: {best_run[0]} (Accuracy: {best_run[1]['accuracy']:.4f})")

def main():
    print("Get metrics from PushGateway...")
    
    metrics_text = get_metrics()
    if not metrics_text:
        return
    
    print("Metrics received")
    
    mlflow_metrics = parse_mlflow_metrics(metrics_text)
    display_metrics(mlflow_metrics)
    
    print(f"\nPushGateway available: http://localhost:9091")
    print(f"All metrics: http://localhost:9091/metrics")

if __name__ == "__main__":
    main()