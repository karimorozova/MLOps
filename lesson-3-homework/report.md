# Docker Image Comparison Report – PyTorch ML Service

## 1. Overview

We built two Docker images for our PyTorch inference service:

| Image        | Tag    | Size   |
| ------------ | ------ | ------ |
| pytorch-fat  | latest | 8.9 GB |
| pytorch-slim | latest | 1 GB   |

The goal was to compare a "fat" image with all dependencies versus a "slim" optimized image using multi-stage builds.

## 2. Image History Analysis

### **pytorch-fat**

- Total size: **8.9 GB**
- Largest layers:

  - `pip install torch, torchvision, pillow` → 6.87 GB
  - Copying model and scripts → 942 MB

- Base image: `python:3.9`
- Contains full Python environment and system libraries.
- Suitable for full development/testing, but large for deployment.

### **pytorch-slim**

- Total size: **1 GB**
- Largest layers:

  - Copying Python dependencies → 866 MB
  - Copying scripts and model → \~14–15 MB

- Base image: `python:3.9-slim`
- Multi-stage build removed unnecessary build tools and system libraries.
- Optimized for deployment and fast download.

## 3. Observations

1. **Size reduction:**
   Slim image reduced the size from **8.9 GB → 1 GB**, a **\~88% decrease**.
2. **Layer optimization:**
   Slim image has fewer large layers; heavy pip installation layers are isolated in the builder stage.
3. **Dependencies:**
   Fat image includes all dev dependencies, tools, and caches, which increases image size.
4. **Deployment considerations:**
   Slim image is better for production inference; fat image may be useful for local development or debugging.

## 4. Conclusion

The multi-stage slim Docker image successfully minimizes the size without sacrificing the inference functionality. For deployment, **`pytorch-slim`** is highly recommended, while **`pytorch-fat`** can be kept for development and experimentation.
