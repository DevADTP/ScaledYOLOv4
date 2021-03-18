ALL = ['MishCuda']

import torch

class MishCuda(torch.nn.Module):
    def __init__(self):
        super(MishCuda, self).__init__()

    def forward(self, x):
        return x * torch.tanh(torch.nn.functional.softplus(x))
