# MLOps Training Automation

This project demonstrates the automation of ML model training using **AWS Step Functions**, **Lambda functions**, and **GitLab CI/CD**.

## Architecture

The project includes the following components:

- **AWS Step Function** – orchestrates the training pipeline
- **Lambda functions** – perform individual stages (data validation, metric logging)
- **Terraform** – Infrastructure as Code for deploying AWS resources
- **GitLab CI** – automatically triggers the pipeline on repository push

### Pipeline Diagram

```
GitLab CI Push → Step Function → ValidateData → LogMetrics → CloudWatch Logs
```

## Project Structure

```
mlops-train-automation/
├── terraform/
│   ├── main.tf                 # Main Terraform configuration
│   ├── variables.tf            # Variables and outputs
│   └── lambda/
│       ├── validate.py         # Lambda function for validation
│       ├── log_metrics.py      # Lambda function for logging metrics
│       ├── validate.zip        # Archive for validate function
│       └── log_metrics.zip     # Archive for log_metrics function
├── .gitlab-ci.yml              # GitLab CI configuration with OIDC
└── README.md                   # This file
```

## Quick Start

### Prerequisites

1. **AWS CLI** configured with valid credentials
2. **Terraform** version ≥ 1.0
3. **GitLab** repository with CI/CD configured
4. **OIDC variable** `AWS_ROLE_ARN` in GitLab CI settings (set automatically)

### 1. Build Lambda Archives

```bash
cd terraform/lambda

# Create archives for Lambda functions
zip validate.zip validate.py
zip log_metrics.zip log_metrics.py

# Check created archives
ls -la *.zip
```

**Result:**

- `validate.zip` (938 bytes) – contains `validate.py`
- `log_metrics.zip` (1,424 bytes) – contains `log_metrics.py`

**Important:** The archives must include only the Python files — no directories!

### 2. Deploy Infrastructure with Terraform

```bash
cd terraform

terraform init       # Initialize Terraform
terraform plan       # Review deployment plan
terraform apply      # Deploy infrastructure
terraform output     # Check created resources
```

**Created resources:**

- 2 Lambda functions: `mlops-validate-data`, `mlops-log-metrics`
- 2 IAM roles: `mlops-lambda-role`, `mlops-step-function-role`
- 1 Step Function: `mlops-training-pipeline`
- 1 CloudWatch Log Group: `/aws/stepfunctions/mlops-training-pipeline`

**Important:** Ensure AWS CLI is configured with the correct credentials!

---

### 3. Configure GitLab CI

#### OIDC Setup (recommended)

**OIDC is already configured automatically!**
It uses secure authentication via AWS IAM roles.

**Required variable in GitLab CI Settings:**

- `AWS_ROLE_ARN` = `arn:aws:iam::317144351228:role/GitLab-CI-Role`

**To add the variable:**

1. Go to **Settings → CI/CD → Variables**
2. Click **Add variable**
3. **Key:** `AWS_ROLE_ARN`
4. **Value:** `arn:aws:iam::317144351228:role/GitLab-CI-Role`
5. Enable **Protect variable**
6. Enable **Expand variable reference**

#### GitLab CI Pipeline Flow

**Stages:**

1. **deploy** – Deploys infrastructure (manual)
2. **train** – Trains the model (auto-triggered on push)

**Job: train_model**

- **Triggers:** Push to main/develop, merge requests, manual run
- **Process:** Fetch ARN → Create JSON → Start Step Function → Monitor progress
- **Authentication:** OIDC tokens via `AWS_ROLE_ARN`

### 4. Manual Step Function Run

```bash
# Get Step Function ARN
STEP_FUNCTION_ARN=$(aws stepfunctions list-state-machines \
  --query "stateMachines[?name=='mlops-training-pipeline'].stateMachineArn" \
  --output text)

# Create input JSON
INPUT_JSON='{
  "source": "manual",
  "commit": "manual-test",
  "branch": "main",
  "pipeline_id": "manual",
  "job_id": "manual",
  "triggered_by": "manual",
  "timestamp": "'$(date -u +%Y-%m-%dT%H:%M:%SZ)'"
}'

# Start execution
aws stepfunctions start-execution \
  --state-machine-arn "$STEP_FUNCTION_ARN" \
  --name "manual-test-$(date +%s)" \
  --input "$INPUT_JSON"
```

## Example JSON Parameters

### Manual Run

```json
{
  "source": "manual",
  "commit": "manual-test",
  "branch": "main",
  "pipeline_id": "manual",
  "job_id": "manual",
  "triggered_by": "manual",
  "timestamp": "2024-10-26T01:30:00Z"
}
```

### GitLab CI Run

```json
{
  "source": "gitlab-ci",
  "commit": "abc123def456",
  "branch": "main",
  "pipeline_id": "12345678",
  "job_id": "87654321",
  "triggered_by": "gitlab-ci",
  "timestamp": "2024-10-26T01:30:00Z"
}
```

### Parameter Fields

- **source:** Execution source (`manual`, `gitlab-ci`)
- **commit:** Git commit SHA
- **branch:** Git branch name
- **pipeline_id:** GitLab pipeline ID
- **job_id:** GitLab job ID
- **triggered_by:** Who triggered it (`manual`, `gitlab-ci`)
- **timestamp:** Execution time in ISO format

## Component Details

### Lambda Functions

#### `validate.py`

- **Purpose:** Validate data before training
- **Input:** JSON metadata (commit, branch, timestamp)
- **Output:** Validation results and readiness status
- **Logic:** Simulates data quality checks (sample count, missing values, etc.)

#### `log_metrics.py`

- **Purpose:** Log metrics after training
- **Input:** Validation results from previous step
- **Output:** Training metrics and completion status
- **Logic:** Simulates metric calculation and logs results to CloudWatch

### Step Function

**Pipeline Structure:**

1. **ValidateData** → Lambda for validation
2. **LogMetrics** → Lambda for metric logging
3. **Error Handling** → Managed at each step

### Terraform Configuration

#### IAM Roles & Policies

- **Lambda role:** Permissions for CloudWatch logs & metrics
- **Step Function role:** Permission to invoke Lambda functions
- **Least privilege principle** applied

#### Lambda Functions

- **Runtime:** Python 3.9
- **Timeout:** 30 seconds
- **Environment variables:** Configurable
- **Tags:** Resource management metadata

#### Step Function

- **State Machine:** Two-state JSON definition
- **Error Handling:** Catch blocks for failures
- **Retry Logic:** Automatic retries

## GitLab CI Pipeline

### Stages

1. **deploy** – Manual infrastructure deployment
2. **train** – Automatic model training

**train_model Job:**

1. Fetch Step Function ARN
2. Generate execution name
3. Build JSON input
4. Start Step Function
5. Monitor execution status
6. Display results

## 🔍 System Validation

### 1. Test Lambda Functions

```bash
aws lambda list-functions --query 'Functions[?contains(FunctionName, `mlops`)].{Name:FunctionName,Runtime:Runtime,LastModified:LastModified}'

aws lambda invoke \
  --function-name mlops-validate-data \
  --payload '{"source":"test","commit":"test123"}' \
  response.json

cat response.json | jq .
```

### 2. Test Step Function

```bash
aws stepfunctions list-state-machines

aws stepfunctions list-executions \
  --state-machine-arn $(aws stepfunctions list-state-machines --query "stateMachines[?name=='mlops-training-pipeline'].stateMachineArn" --output text) \
  --max-items 5
```

### 3. Check CloudWatch Logs

```bash
aws logs describe-log-groups --log-group-name-prefix "/aws/lambda/mlops"
aws logs describe-log-groups --log-group-name-prefix "/aws/stepfunctions"
```
