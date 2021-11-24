import data_handler as dh
import data_handler2 as dh2
import model as md
import numpy as np
import torch
from torch.utils.data.dataloader import DataLoader
from torch import nn, optim
from torch.utils.data import random_split

stocks_path = './02. MLP Regression/Stock_data/data/turkish_stocks.csv'

def load_data():        
    dataset = dh2.LoadData(stocks_path)
    train_samples = int(len(dataset) * .8)
    train_set, test_set = random_split(dataset, [train_samples, len(dataset) - train_samples])
    trainloader = DataLoader(dataset=train_set, batch_size=8, shuffle=True)
    testloader = DataLoader(dataset=test_set, batch_size=8)

    return trainloader, testloader

trainloader, testloader = load_data()

model = md.Network()
criterion = nn.L1Loss()
optimizer = optim.Adam(model.parameters(), lr=0.001)

epochs = 5
best_loss = float(np.inf)

for e in range(epochs):
    loss_train, loss_test = 0, 0

    model.train()
    for x_train, y_train in iter(trainloader):
        x_train, y_train = x_train.float(), y_train.float()

        optimizer.zero_grad()
        outputs = model(x_train)
        loss = criterion(outputs, y_train)
        loss.backward()
        optimizer.step()

        loss_train += loss.item()
    
    model.eval()
    with torch.no_grad():
        for x_test, y_test in iter(testloader):
            x_test, y_test = x_test.float(), y_test.float()

            outputs_test = model(x_test)
            loss_test = criterion(outputs_test, y_test)
            loss_train += loss_test.item()

    print(f'Current training loss: {loss_train}, test loss: {loss_test}, epoch: {e}')

    if loss_train < best_loss:
        best_loss = loss_train
        torch.save(model.state_dict(), '02. MLP Regression/model.pth')
