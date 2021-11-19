import matplotlib.pyplot as plt
import torch
from torchvision import transforms
import numpy as np

import model
import data_handler
from torch import nn
from torch import optim
import torch.nn.functional as F
from torch.utils.data import Dataset, DataLoader
import pandas as pd
from torch.optim.lr_scheduler import StepLR

if __name__ == '__main__':

    test_csv = pd.read_csv('./data/fashion-mnist_test.csv')
    transf = transforms.Compose([transforms.ToTensor(), transforms.Normalize((0.5,), (0.5,))])
    test_set = data_handler.FashionDataset(test_csv, transform=transf)
    testloader = DataLoader(test_set, batch_size=len(test_set), shuffle=True)


    for i, (images, labels) in enumerate(iter(testloader)):

        model = model.Network_2()
        model.load_state_dict(torch.load('model.pth'))
        model.eval()

        output = model(images)
        pred_y = torch.max(output, 1)[1].data.squeeze()
        images_wrong = images[pred_y != labels]
        labels_wrong = labels[pred_y != labels]

    fig = plt.figure()
    plt.hist(labels_wrong.numpy())
    plt.xticks ([0,1,2,3,4,5,6,7,8,9],['T-shirt/top',
                            'Trouser',
                            'Pullover',
                            'Dress',
                            'Coat',
                            'Sandal',
                            'Shirt',
                            'Sneaker',
                            'Bag',
                            'Ankle Boot'], rotation=45
)
    fig.savefig('distribution_errors.png')
    plt.show()