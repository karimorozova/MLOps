import json
import boto3
from datetime import datetime

def lambda_handler(event, context):
    """
    Lambda function for logging metrics after training the model
    """
    print("logging metrics...")
    
    # Getting the validation results from the previous step
    validation_results = event.get('validation_results', {})
    source = event.get('source', 'unknown')
    commit = event.get('commit', 'unknown')
    timestamp = datetime.now().isoformat()
    
    print(f"Logging params:")
    print(f"   Source: {source}")
    print(f"   Commit: {commit}")
    print(f"   Timestamp: {timestamp}")
    
    # Simulation of training metrics
    training_metrics = {
        "model_accuracy": 0.92,
        "model_precision": 0.89,
        "model_recall": 0.91,
        "model_f1_score": 0.90,
        "training_time_seconds": 45,
        "validation_score": validation_results.get('validation_score', 0.95),
        "model_size_mb": 2.5,
        "training_samples": validation_results.get('sample_count', 1000),
        "features_used": validation_results.get('features_count', 10)
    }
    
    print(f"Metrics saved:")
    print(f"   Model accuracy: {training_metrics['model_accuracy']:.2%}")
    print(f"   Precision: {training_metrics['model_precision']:.2%}")
    print(f"   Recall: {training_metrics['model_recall']:.2%}")
    print(f"   F1-score: {training_metrics['model_f1_score']:.2%}")
    print(f"   Training time: {training_metrics['training_time_seconds']} сек")
    print(f"   Model size: {training_metrics['model_size_mb']} MB")
    
    # Simulation of saving in CloudWatch Logs
    try:
        cloudwatch = boto3.client('logs')
        log_group_name = '/aws/lambda/mlops-training'
        
        # Create a log group if it does not exist
        try:
            cloudwatch.create_log_group(logGroupName=log_group_name)
        except cloudwatch.exceptions.ResourceAlreadyExistsException:
            pass
        
        # Creating a log stream
        log_stream_name = f"training-{commit}-{int(datetime.now().timestamp())}"
        try:
            cloudwatch.create_log_stream(
                logGroupName=log_group_name,
                logStreamName=log_stream_name
            )
        except cloudwatch.exceptions.ResourceAlreadyExistsException:
            pass
        
        # Send log
        log_events = [{
            'timestamp': int(datetime.now().timestamp() * 1000),
            'message': json.dumps({
                "event_type": "training_completed",
                "metrics": training_metrics,
                "source": source,
                "commit": commit,
                "timestamp": timestamp
            })
        }]
        
        cloudwatch.put_log_events(
            logGroupName=log_group_name,
            logStreamName=log_stream_name,
            logEvents=log_events
        )
        
        print(f"Metrics saved in CloudWatch Logs: {log_group_name}/{log_stream_name}")
        
    except Exception as e:
        print(f"Error saving in CloudWatch: {e}")
    
    # Give a result
    return {
        "statusCode": 200,
        "body": {
            "metrics_logged": True,
            "training_metrics": training_metrics,
            "source": source,
            "commit": commit,
            "timestamp": timestamp,
            "pipeline_status": "completed"
        }
    }