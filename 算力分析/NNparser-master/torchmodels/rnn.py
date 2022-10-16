# -*- coding: utf-8 -*-
"""
Created on Mon Aug  3 12:52:15 2020

@author: LL
"""
from torch import nn

class RNNNet(nn.Module):
    """ Batch-first LSTM model. """
    def __init__(self, vocab_size=32, embed_dim=300, hidden_dim=512, num_layers=2):
        super().__init__()
        self.hidden_dim = hidden_dim
        self.embedding = nn.Embedding(vocab_size, embed_dim)
        self.encoder = nn.RNN(embed_dim, hidden_dim, num_layers=num_layers, batch_first=True)
        self.decoder = nn.Linear(hidden_dim, vocab_size)

    def forward(self, x):
        embed = self.embedding(x)
        out, hidden = self.encoder(embed)
        out = self.decoder(out)
        out = out.view(-1, out.size(2))
        return out, hidden
