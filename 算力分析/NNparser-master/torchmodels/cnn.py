# -*- coding: utf-8 -*-
"""
Created on Mon Aug  3 12:52:15 2020

@author: LL
"""
import torch.nn.functional as F
from torch import nn
import torch

class CNNNet(nn.Module):
    def __init__(self):
        super(CNNNet,self).__init__()
        self.conv1 = nn.Conv2d(in_channels=1,out_channels=4,kernel_size=3,padding=1)
        self.conv2 = nn.Conv2d(in_channels=4,out_channels=8,kernel_size=5)
        self.fc1 = nn.Linear(4*4*8,32)
        self.fc2 = nn.Linear(32,1)
    def forward(self,x):
        x = F.relu(self.conv1(x))
        x = F.relu(self.conv2(x))
        x = x.view(-1,4*4*8)
        x = torch.tanh(self.fc1(x))
        x = self.fc2(x)
        return x    
