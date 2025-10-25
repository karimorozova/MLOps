import json
import boto3
from datetime import datetime

def lambda_handler(event, context):
    """
    Lambda function for validating data before training the model
    """
    print("Data validation...")
    
    # Getting params from event
    source = event.get('source', 'unknown')
    commit = event.get('commit', 'unknown')
    timestamp = datetime.now().isoformat()
    
    print(f"Validation params:")
    print(f"   Source: {source}")
    print(f"   Commit: {commit}")
    print(f"   Timestamp: {timestamp}")
    
    # Simulate data validation
    validation_results = {
        "status": "success",
        "data_quality": "good",
        "sample_count": 1000,
        "features_count": 10,
        "missing_values": 0,
        "outliers_detected": 5,
        "validation_score": 0.95
    }
    
    print(f"Validation completed:")
    print(f"   Status: {validation_results['status']}")
    print(f"   Data quality: {validation_results['data_quality']}")
    print(f"   Sample count: {validation_results['sample_count']}")
    print(f"   Features count: {validation_results['features_count']}")
    print(f"   Missing values: {validation_results['missing_values']}")
    print(f"   Outliers: {validation_results['outliers_detected']}")
    print(f"   Validation score: {validation_results['validation_score']}")
    
    # Return the result for the next step
    return {
        "statusCode": 200,
        "body": {
            "validation_passed": True,
            "validation_results": validation_results,
            "source": source,
            "commit": commit,
            "timestamp": timestamp,
            "next_step": "log_metrics"
        }
    }