# PyTorch Image Classifier in Docker

## Quickstart

### 1. Export model

```bash
python export_model.py
```

### 2. Run inference locally

```bash
python inference.py example.jpg
```

### 3. Build and run fat image

```bash
docker build -t pytorch-fat -f Dockerfile.fat .
docker run --rm -v $(pwd):/app pytorch-fat /app/example.jpg
```

### 4. Build and run slim image

```bash
docker build -t pytorch-slim -f Dockerfile.slim .
docker run --rm -v $(pwd):/app pytorch-slim /app/example.jpg
```

## Report

See [report.md](report.md)
