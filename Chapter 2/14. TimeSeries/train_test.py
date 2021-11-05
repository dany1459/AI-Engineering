import os
import random

def control_split(test_size = 0.2):
    for file in os.listdir('Data/control/'):

        if random.random() <= test_size:   
            os.system('mv Data/control/' +file+ ' split_data/test/control/' +file)

        else:
            os.system('mv Data/control/' +file+ ' split_data/train/control/' +file)


control_split(test_size=0.2)