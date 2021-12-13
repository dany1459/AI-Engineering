import torch
import torch.nn as nn
from torch.optim import Adam
from torch.autograd import Variable
from torchsummary import summary

class Model(nn.Module):
    def __init__(self, input_size, hidden_size, n_layers):
        super(Model, self).__init__()
        
        #Defining the layers
        self.hidden_dim = hidden_size
        self.n_layers = n_layers
        
        #RNN layer
         
        self.rnn = nn.RNN(input_size, hidden_size, n_layers, batch_first=True) 
        
        #Fully  connected layer
        
        self.fc = nn.Linear(batches * hidden_size, batches * hidden_size) # batch_size * hidden_size
        self.relu= nn.ReLU()
        
    def foward(self, x):
        
        batch_size = x.size(0)
        
        #intialize hidden state for the first input
        hidden = self.init_hidden(batch_size)
        
        #pass the input and hidden state through the rnn and obtainign outputs
        out, hidden =self.rnn(x, hidden)
        hidden_last = hidden[-1]
        out = self.relu(hidden_last.flatten()) 
        
        out = self.fc(out)
        
        return out
    
    def init_hidden(self, batch_size):
        hidden = Variable(torch.zeros(self.n_layers, batch_size, self.hidden_dim))
        return hidden
        
        