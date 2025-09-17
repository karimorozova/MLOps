import torch
import torchvision.transforms as transforms
from PIL import Image
import sys

# Load model
model = torch.jit.load("model.pt")
model.eval()

# Image preprocessing
preprocess = transforms.Compose([
    transforms.Resize(256),
    transforms.CenterCrop(224),
    transforms.ToTensor(),
    transforms.Normalize(mean=[0.485, 0.456, 0.406],
                         std=[0.229, 0.224, 0.225]),
])

def predict(image_path):
    image = Image.open(image_path).convert("RGB")
    input_tensor = preprocess(image).unsqueeze(0)

    with torch.no_grad():
        output = model(input_tensor)
        probs = torch.nn.functional.softmax(output[0], dim=0)

    top3 = torch.topk(probs, 3)
    print("Top-3 predictions:", top3.indices.tolist(), top3.values.tolist())

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python inference.py <image_path>")
        sys.exit(1)

    predict(sys.argv[1])
