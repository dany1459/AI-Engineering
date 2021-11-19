import matplotlib.pyplot as plt
import torch
from torchvision import transforms

import model
import data_handler
from torch import nn
from torch import optim
import torch.nn.functional as F
from torch.utils.data import Dataset, DataLoader
import pandas as pd
from torch.optim.lr_scheduler import StepLR

train_csv = pd.read_csv('/data/fashion-mnist_train.csv')
test_csv = pd.read_csv('/data/fashion-mnist_test.csv')
transf = transforms.Compose([transforms.ToTensor(),transforms.Normalize((0.5,), (0.5,))])
train_set = data_handler.FashionDataset(train_csv, transform=transf)
test_set = data_handler.FashionDataset(test_csv, transform=transf)

batch_size = 100
trainloader = DataLoader(train_set, batch_size=batch_size, shuffle=True)
testloader = DataLoader(test_set, batch_size=batch_size, shuffle=True)
model = model.Network_2()



epochs = 25
criterion = nn.CrossEntropyLoss()
#criterion = nn.NLLLoss()
optimizer = optim.SGD(model.parameters(), lr=0.01)
scheduler = StepLR(optimizer, step_size=20, gamma=0.1)

loss_hist_train = []
loss_hist_test = []


best_acc = 0

for e in range(epochs):
    loss_train = 0
    loss_test = 0
    for i, (images, labels) in enumerate(iter(trainloader)):
        # Flatten MNIST images into a 784 long vector

        model.train()
        optimizer.zero_grad()
        output = model.forward(images)
        #output = torch.exp(output)
        loss = criterion(output, labels)
        loss_train+=loss.item()
        loss.backward()
        optimizer.step()
    loss_hist_train.append(loss_train/len(trainloader.dataset))
    model.eval()
    with torch.no_grad():
        correct = 0
        total = 0
        for i, (images, labels) in enumerate(iter(testloader)):

            test_output = model.forward(images)
            #test_output = torch.exp(test_output)
            loss = criterion(test_output, labels)
            loss_test += loss
            pred_y = torch.max(test_output, 1)[1].data.squeeze()
            correct += (pred_y == labels).float().sum()
            total += len(labels)
            accuracy = (pred_y == labels).sum().item() / float(labels.size(0))

        loss_hist_test.append(loss_test/len(testloader.dataset))
    acc = (correct/total).float()*100
    print(f'epoch {e+1} with LR {scheduler.get_last_lr()} done: accuracy of {acc:.2f}, train_loss:{loss_train/len(trainloader.dataset)} and test_loss: {loss_test/len(testloader.dataset)}')
    model.train()
    scheduler.step()
    if e==0:
        diff_loss = 100
    if abs(loss_test-loss_train) < diff_loss+diff_loss/90 and acc>best_acc:
        diff_loss = abs(loss_test-loss_train)
        best_acc = acc
        torch.save(model.state_dict(), 'model.pth')
        epoch_best = e


print(epoch_best)
fig = plt.figure()
plt.plot(loss_hist_train)
plt.plot(loss_hist_test)
plt.legend(labels=['Train loss', 'Test loss'])
fig.savefig('losses.png')
plt.show()
