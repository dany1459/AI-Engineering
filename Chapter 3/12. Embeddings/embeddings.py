import data_handler as dh
import numpy as np
import torch
import torch.nn.functional as F
from torch.autograd import Variable

pairs, len_vocabulary = dh.get_dataset()

def input_layer(word_idx):
	x = torch.zeros(len_vocabulary).float()
	x[word_idx] = 1.0
	return x

def train(n_epochs=20, lr=0.001, embedding_size=5):

    W1 = Variable(torch.randn(len_vocabulary, embedding_size).float(), requires_grad=True)
    W2 = Variable(torch.randn(embedding_size, len_vocabulary).float(), requires_grad=True)

    for epoch in range(n_epochs):
        loss_val = 0

        for data, target in pairs:

            x = Variable(input_layer(data).float())
            y_true = Variable(torch.from_numpy(np.array([target])).long())

            z1 = torch.matmul(x,W1)
            z2 = torch.matmul(z1,W2)

            log_softmax = F.log_softmax(z2, dim=0)
            loss = F.nll_loss(log_softmax.view(1, -1), y_true)
            loss_val += loss
            loss.backward()

            W1.data -= lr * W1.grad.data
            W2.data -= lr * W2.grad.data

            W1.grad.data.zero_()
            W2.grad.data.zero_()

        if epoch % 10 == 0:    
            print(f'Loss at epoch {epoch}: {loss_val/len(pairs)}')

train()
