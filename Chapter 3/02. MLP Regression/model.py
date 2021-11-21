from torch import nn

class Network(nn.Module):

    def __init__(self):
        super().__init__()
        self.layers = nn.Sequential(
            nn.Linear(8,40), nn.ReLU(),
            nn.Linear(40,24), nn.ReLU(),
            nn.Linear(24,1) )

    def forward (self,x):
        return self.layers(x)
    