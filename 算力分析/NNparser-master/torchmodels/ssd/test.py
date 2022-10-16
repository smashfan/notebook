# Copyright (c) Facebook, Inc. and its affiliates. All Rights Reserved.


import torch
import numpy as np



# from ssd_mobilenet_v1 import create_mobilenetv1_ssd
from ssd_r34 import SSD_R34


model = SSD_R34()
model.eval()


image = torch.rand(1,3,1200,1200)


results = model(image)






