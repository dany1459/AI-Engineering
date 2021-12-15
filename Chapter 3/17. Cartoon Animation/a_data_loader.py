from torch.utils.data import Dataset

class LoadData(Dataset):
    def __init__(self, data):
        super().__init__()
        labels = data['class'].replace(['DBZ', 'Breathtaking', 'Victory', 'DBZ-Loki'], [0,1,2,3])
        self.x = data.drop(['class'], axis=1).values
        self.y = labels.values
        self.n_samples = len(self.x)

    def __getitem__(self, index):
        return self.x[index], self.y[index]
        
    def __len__(self):
        return self.n_samples
