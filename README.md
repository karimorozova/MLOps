# PyTorch Image Classifier in Docker

## Prerequisites

- Python 3.9+ (for local inference)
- Docker installed
- Optional: virtual environment for Python dependencies

## Quickstart

### 1. Export model

```bash
python export_model.py
```

### 2. Run inference locally

```bash
python inference.py example.jpg
```

> Make sure `example.jpg` exists in the project folder or download a sample image.

### 3. Build and run fat image

```bash
docker build -t pytorch-fat -f Dockerfile.fat .
docker run --rm -v $(pwd):/app pytorch-fat /app/example.jpg
```

> The fat image includes all dependencies and is larger (\~8.9 GB).

### 4. Build and run slim image

```bash
docker build -t pytorch-slim -f Dockerfile.slim .
docker run --rm -v $(pwd):/app pytorch-slim /app/example.jpg
```

> The slim image is optimized for deployment (\~1 GB).

## Report

See [report.md](report.md) for Docker image size comparison and analysis.
