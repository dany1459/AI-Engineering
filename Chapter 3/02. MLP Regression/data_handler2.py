import pandas as pd
from torch.utils.data import Dataset

class LoadData(Dataset):

    def __init__(self, pth):
        super().__init__()
        data = pd.read_csv(pth)
        data.drop(['date'], axis=1, inplace=True)

        self.x = data.drop(['DAX'], axis=1).values
        self.y = data['DAX'].values
        self.n_samples = len(self.x)

    def __getitem__(self, index):
        return self.x[index], self.y[index]

    def __len__(self):
        return self.n_samples
