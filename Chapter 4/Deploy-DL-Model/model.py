import torch.nn.functional as F
from torch import nn
import cv2

def preprocess(image):
    bgr_image = cv2.imread(image)
    gray_image = cv2.imread(image, 0)
    _, threshold = cv2.threshold(gray_image, 150, 160, type=cv2.THRESH_BINARY_INV+cv2.THRESH_OTSU)
    kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (7, 7))
    threshold = cv2.dilate(threshold, kernel, iterations=2)
    threshold = cv2.resize(threshold, (28,28))
    return threshold, bgr_image

class Network(nn.Module):
    def __init__(self):
        super().__init__()
        self.fc1 = nn.Linear(28*28, 128)
        self.fc2 = nn.Linear(128, 64)
        self.fc3 = nn.Linear(64, 10)
        
    def forward(self, x):
        x = x.view(x.shape[0], 28*28)
        x = F.relu(self.fc1(x))
        x = F.relu(self.fc2(x))
        x = self.fc3(x)
        x = F.softmax(x, dim=1)
        return x
