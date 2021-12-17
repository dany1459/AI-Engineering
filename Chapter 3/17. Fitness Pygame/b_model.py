import torch.nn.functional as F
from torch import nn

class Network(nn.Module):
    def __init__(self):
        super().__init__()
        self.fc1 = nn.Linear(132, 100)
        self.fc2 = nn.Linear(100, 50)
        self.fc3 = nn.Linear(50, 4)
 
    def forward(self, x):
        x = x.view(x.shape[0], 132)
        x = F.relu(self.fc1(x))
        x = F.relu(self.fc2(x))
        x = self.fc3(x)
        x = F.softmax(x, dim=1)
        return x
