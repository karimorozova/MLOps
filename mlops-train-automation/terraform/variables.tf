variable "aws_region" {
  description = "AWS region for resource deployment"
  type        = string
  default     = "us-east-1"
}

variable "environment" {
  description = "Environment (dev, staging, production)"
  type        = string
  default     = "production"
}

variable "project_name" {
  description = "Project name"
  type        = string
  default     = "mlops-train-automation"
}

# Outputs
output "validate_lambda_arn" {
  description = "ARN Lambda validate functions"
  value       = aws_lambda_function.validate_function.arn
}

output "log_metrics_lambda_arn" {
  description = "ARN Lambda log metrics function"
  value       = aws_lambda_function.log_metrics_function.arn
}

output "step_function_arn" {
  description = "ARN Step Function pipeline"
  value       = aws_sfn_state_machine.mlops_pipeline.arn
}

output "step_function_name" {
  description = "Name of Step Function"
  value       = aws_sfn_state_machine.mlops_pipeline.name
}

output "lambda_role_arn" {
  description = "ARN IAM roles for Lambda functions"
  value       = aws_iam_role.lambda_role.arn
}

output "step_function_role_arn" {
  description = "ARN IAM roles for Step Function"
  value       = aws_iam_role.step_function_role.arn
}