terraform {
  required_version = ">= 1.0"
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 5.0"
    }
  }
}

provider "aws" {
  region = var.aws_region
}

# IAM role for Lambda functions
resource "aws_iam_role" "lambda_role" {
  name = "mlops-lambda-role"

  assume_role_policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Action = "sts:AssumeRole"
        Effect = "Allow"
        Principal = {
          Service = "lambda.amazonaws.com"
        }
      }
    ]
  })
}

# IAM policy for Lambda functions
resource "aws_iam_role_policy" "lambda_policy" {
  name = "mlops-lambda-policy"
  role = aws_iam_role.lambda_role.id

  policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Effect = "Allow"
        Action = [
          "logs:CreateLogGroup",
          "logs:CreateLogStream",
          "logs:PutLogEvents"
        ]
        Resource = "arn:aws:logs:*:*:*"
      },
      {
        Effect = "Allow"
        Action = [
          "cloudwatch:PutMetricData",
          "cloudwatch:GetMetricStatistics",
          "cloudwatch:ListMetrics"
        ]
        Resource = "*"
      }
    ]
  })
}

# Lambda function for data validation 
resource "aws_lambda_function" "validate_function" {
  filename         = "lambda/validate.zip"
  function_name    = "mlops-validate-data"
  role            = aws_iam_role.lambda_role.arn
  handler         = "validate.lambda_handler"
  runtime         = "python3.9"
  timeout         = 30

  source_code_hash = filebase64sha256("lambda/validate.zip")

  environment {
    variables = {
      ENVIRONMENT = "production"
    }
  }

  tags = {
    Name        = "MLOps Validate Function"
    Environment = "production"
    Project     = "mlops-train-automation"
  }
}

# Lambda function for logging metrics
resource "aws_lambda_function" "log_metrics_function" {
  filename         = "lambda/log_metrics.zip"
  function_name    = "mlops-log-metrics"
  role            = aws_iam_role.lambda_role.arn
  handler         = "log_metrics.lambda_handler"
  runtime         = "python3.9"
  timeout         = 30

  source_code_hash = filebase64sha256("lambda/log_metrics.zip")

  environment {
    variables = {
      ENVIRONMENT = "production"
    }
  }

  tags = {
    Name        = "MLOps Log Metrics Function"
    Environment = "production"
    Project     = "mlops-train-automation"
  }
}

# IAM role for Step Function
resource "aws_iam_role" "step_function_role" {
  name = "mlops-step-function-role"

  assume_role_policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Action = "sts:AssumeRole"
        Effect = "Allow"
        Principal = {
          Service = "states.amazonaws.com"
        }
      }
    ]
  })
}

# IAM policy for Step Function
resource "aws_iam_role_policy" "step_function_policy" {
  name = "mlops-step-function-policy"
  role = aws_iam_role.step_function_role.id

  policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Effect = "Allow"
        Action = [
          "lambda:InvokeFunction"
        ]
        Resource = [
          aws_lambda_function.validate_function.arn,
          aws_lambda_function.log_metrics_function.arn
        ]
      },
      {
        Effect = "Allow"
        Action = [
          "logs:CreateLogGroup",
          "logs:CreateLogStream",
          "logs:PutLogEvents"
        ]
        Resource = "arn:aws:logs:*:*:*"
      }
    ]
  })
}

# Step Function for MLOps pipeline
resource "aws_sfn_state_machine" "mlops_pipeline" {
  name     = "mlops-training-pipeline"
  role_arn = aws_iam_role.step_function_role.arn

  definition = jsonencode({
    Comment = "MLOps Training Pipeline with Data Validation and Metrics Logging"
    StartAt = "ValidateData"
    States = {
      ValidateData = {
        Type     = "Task"
        Resource = aws_lambda_function.validate_function.arn
        Next     = "LogMetrics"
        Retry = [
          {
            ErrorEquals = ["Lambda.ServiceException", "Lambda.AWSLambdaException", "Lambda.SdkClientException"]
            IntervalSeconds = 2
            MaxAttempts = 6
            BackoffRate = 2.0
          }
        ]
        Catch = [
          {
            ErrorEquals = ["States.ALL"]
            Next = "ValidationFailed"
            ResultPath = "$.error"
          }
        ]
      }
      LogMetrics = {
        Type     = "Task"
        Resource = aws_lambda_function.log_metrics_function.arn
        End      = true
        Retry = [
          {
            ErrorEquals = ["Lambda.ServiceException", "Lambda.AWSLambdaException", "Lambda.SdkClientException"]
            IntervalSeconds = 2
            MaxAttempts = 6
            BackoffRate = 2.0
          }
        ]
        Catch = [
          {
            ErrorEquals = ["States.ALL"]
            Next = "LoggingFailed"
            ResultPath = "$.error"
          }
        ]
      }
      ValidationFailed = {
        Type = "Fail"
        Cause = "Data validation failed"
      }
      LoggingFailed = {
        Type = "Fail"
        Cause = "Metrics logging failed"
      }
    }
  })

  tags = {
    Name        = "MLOps Training Pipeline"
    Environment = "production"
    Project     = "mlops-train-automation"
  }
}

# CloudWatch Log Group for Step Function
resource "aws_cloudwatch_log_group" "step_function_logs" {
  name              = "/aws/stepfunctions/mlops-training-pipeline"
  retention_in_days = 14

  tags = {
    Name        = "MLOps Step Function Logs"
    Environment = "production"
    Project     = "mlops-train-automation"
  }
}