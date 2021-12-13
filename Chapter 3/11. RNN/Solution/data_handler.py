import pandas as pd
import numpy as np


df = pd.read_csv('data_akbilgic.csv')

df_train = df[:431]
df_test = df[431:]


def next_stock_batch(batch_size, n_steps, df_base):
    t_min = 0
    t_max = df_base.shape[0]
  
    # The inputs will be formed by 8 sequences taken from
    # 8 time series [ISE.1,SP,DAX,FTSE,NIKKEI,BOVESPA,EU,EM]
    x = np.zeros((batch_size,n_steps,7))
    
    # We want to predict the returns of the Istambul stock
    # taken into consideration the previous n_steps days
    y = np.zeros((batch_size,n_steps,1))

    # We chose batch_size random points from time series x-axis

    starting_points = np.random.randint(0,t_max-n_steps-1,size=batch_size)    
    #print(starting_points)

    # We create the batches for x using all time series (8) between t and t+n_steps    
    # We create the batches for y using only one time series between t+1 and t+n_steps+1
    
    for k in np.arange(batch_size):
        lmat = []
        for j in np.arange(n_steps+1):
            lmat.append(df_base.iloc[starting_points[k]+j,2:].values)  
            mat = np.array(lmat)
        # The x values include all columns (mat[:n_steps,:]), these are ([ISE.1,SP,DAX,FTSE,NIKKEI,BOVESPA,EU,EM])
        # and TS values in mat between 0 and n_steps
        x[k,:,:] = mat[:n_steps,1:]
        
        # The y values include only column 0 (mat[1:n_steps+1,0]), this is ([ISE.1]) 
        # and TS values in mat between 1 and n_steps+1
        y[k,:,0] = mat[1:n_steps+1,0]
   

    return x,y
