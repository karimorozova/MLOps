import torch
import torchvision.models as models

# Load pretrained model
model = models.mobilenet_v2(weights=models.MobileNet_V2_Weights.DEFAULT)
model.eval()

# Dummy input for tracing
dummy_input = torch.randn(1, 3, 224, 224)

# Export to TorchScript
traced_model = torch.jit.trace(model, dummy_input)
traced_model.save("model.pt")

print("Model saved to model.pt")
