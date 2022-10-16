import torch
import torchvision.models as models
device1 = torch.device("cuda:0")
data = torch.randn(1, 3, 224, 224)
data = data.to(device1)
model = models.vgg16()
model=model.to(device1)
res = model(data)
print(res)