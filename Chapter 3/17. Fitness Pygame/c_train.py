import numpy as np
import pandas as pd
import torch
from torch import nn
from torch import optim
from torch.utils.data import DataLoader, random_split

import a_data_loader as data_loader
import b_model as md

data = pd.read_csv('data/coordinates.csv')
dataset = data_loader.LoadData(data)
train_samples = int(len(dataset) * 0.8)
train_set, test_set = random_split(dataset, [train_samples, len(dataset) - train_samples])
trainloader = DataLoader(dataset=train_set, batch_size=8, shuffle=True)
testloader = DataLoader(dataset=test_set, batch_size=8)

model = md.Network()
optimizer = optim.Adam(model.parameters(), lr=0.001)
criterion = nn.CrossEntropyLoss()

epochs = 20
best_loss = float(np.inf)

for e in range(epochs):
    loss_train, loss_test = 0, 0
    model.train()
    for x_train, y_train in iter(trainloader):
        x_train, y_train = x_train.float(), y_train.float().long()

        optimizer.zero_grad()
        output = model(x_train)
        loss = criterion(output, y_train)
        loss.backward()
        optimizer.step()
        loss_train += loss.item()
    
    total, correct = 0, 0
    model.eval()
    with torch.no_grad():
        for x_test, y_test in iter(testloader):
            x_test, y_test = x_test.float(), y_test.float().long()

            output = model(x_test)
            loss = criterion(output, y_test)
            loss_test += loss.item()
            _, predicted = torch.max(output.data, 1)
            total += y_test.size(0)
            correct += (predicted == y_test).sum().item()

    print(f'Epoch: {e+1}, Training Loss: {loss_train}, Test Loss: {loss_test}, Accuracy: {correct/total}')

    if loss_train < best_loss:
        best_loss = loss_train
        torch.save(model.state_dict(), 'models/poses_model.pth')
