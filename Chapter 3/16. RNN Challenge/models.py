from __future__ import unicode_literals, print_function, division
import torch
import torch.nn as nn
import torch.nn.functional as F

device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
MAX_LENGTH = 10

class EncoderLSTM(nn.Module):
    def __init__(self, input_size, hidden_size, num_layers):
        super(EncoderLSTM, self).__init__()
        self.hidden_size = hidden_size
        self.num_layers = num_layers

        self.embedding = nn.Embedding(input_size, hidden_size)
        self.lstm = nn.LSTM(hidden_size, hidden_size, num_layers, batch_first=True)
        self.linear = nn.Linear(hidden_size, hidden_size)

    def forward(self, input, hidden):
        h0 = torch.zeros(self.num_layers, input, self.hidden_size).requires_grad_()
        c0 = torch.zeros(self.num_layers, input, self.hidden_size).requires_grad_()

        embedded = self.embedding(input).view(1, 1, -1)
        output = embedded
        output, (hidden, cn) = self.lstm(output, (h0.detach(), c0.detach()))

        output = self.linear(output[:,-1,:])
        return output, hidden

    def initHidden(self):
        return torch.zeros(1, 1, self.hidden_size, device=device)


class DecoderLSTM(nn.Module):
    def __init__(self, hidden_size, output_size, num_layers):
        super(DecoderLSTM, self).__init__()
        self.hidden_size = hidden_size
        self.num_layers = num_layers

        self.embedding = nn.Embedding(output_size, hidden_size)
        self.lstm = nn.LSTM(hidden_size, hidden_size, num_layers, batch_first=True)
        
        self.out = nn.Linear(hidden_size, output_size)
        self.softmax = nn.LogSoftmax(dim=1)

    def forward(self, input, hidden):
        h0 = torch.zeros(self.num_layers, input, self.hidden_size).requires_grad_()
        c0 = torch.zeros(self.num_layers, input, self.hidden_size).requires_grad_()

        output = self.embedding(input).view(1, 1, -1)
        output = F.relu(output)
        output, (hidden, cn) = self.lstm(output, (h0.detach(), c0.detach()))

        output = self.out(output[:,-1,:])
        output = self.softmax(self.out(output[0]))
        return output, hidden

    def initHidden(self):
        return torch.zeros(1, 1, self.hidden_size, device=device)


class AttnDecoderLSTM(nn.Module):
    def __init__(self, hidden_size, output_size, num_layers, dropout_p=0.1, max_length=MAX_LENGTH):
        super(AttnDecoderLSTM, self).__init__()
        self.hidden_size = hidden_size
        self.output_size = output_size
        self.num_layers = num_layers
        self.dropout_p = dropout_p
        self.max_length = max_length

        self.embedding = nn.Embedding(self.output_size, self.hidden_size)
        self.attn = nn.Linear(self.hidden_size * 2, self.max_length)
        self.attn_combine = nn.Linear(self.hidden_size * 2, self.hidden_size)
        self.dropout = nn.Dropout(self.dropout_p)
        self.lstm = nn.LSTM(self.hidden_size, self.hidden_size, num_layers, batch_first=True)
        self.out = nn.Linear(self.hidden_size, self.output_size)

    def forward(self, input, hidden, encoder_outputs):
        h0 = torch.zeros(self.num_layers, input, self.hidden_size).requires_grad_()
        c0 = torch.zeros(self.num_layers, input, self.hidden_size).requires_grad_()

        embedded = self.embedding(input).view(1, 1, -1)
        embedded = self.dropout(embedded)

        attn_weights = F.softmax(self.attn(torch.cat((embedded[0], hidden[0]), 1)), dim=1)
        attn_applied = torch.bmm(attn_weights.unsqueeze(0), encoder_outputs.unsqueeze(0))

        output = torch.cat((embedded[0], attn_applied[0]), 1)
        output = self.attn_combine(output).unsqueeze(0)

        output = F.relu(output)
        output, (hidden, cn) = self.lstm(output, (h0.detach(), c0.detach()))

        output = F.log_softmax(self.out(output[0]), dim=1)
        return output, hidden, attn_weights

    # def initHidden(self):
    #     return torch.zeros(1, 1, self.hidden_size, device=device)

