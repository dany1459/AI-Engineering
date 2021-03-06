import pandas as pd
import numpy as np

def pairing(data, sequence_length=6): # 0 to 5, 6 not included
    # generate sequences from first 6 rows & try to predict the next element 7th
    # measurement of 10 min --> 6 rows = 1 hour
    
    x = []
    y = []

    # iterate through the data in steps
    # start at 0, end 1 seq_len+1 before the end --> so we are not out of range
    # step size: seq_len+1=7
    for i in range(0, (data.shape[0] - sequence_length + 1), sequence_length + 1):
        # define a sequence with seq_len rows, and data.shape[1] cols
        sequence = np.zeros( (sequence_length, data.shape[1]) )

        # iterate through the seq_len to fill the sequence/matrix
        for j in range(sequence_length):
            sequence[j] = data.values[i + j] # fill the matrix with the data, and add i to make the jump to the next seq


        x.append(sequence.flatten()) # to make it 1 dimensional
        y.append(data['Temperature'][i + sequence_length])

    return np.array(x), np.array(y)


# data = pd.read_csv('C:/Users/Igor/Documents/GitHub/AI-Engineering/Chapter 2/14. TimeSeries/climate.csv')
# data = data.drop(['Date Time'], axis=1)

# print(data.shape)

# x, y = pairing(data)

# print(x.shape)
# print(y.shape)
# print(y[0])
# print(y[1])
