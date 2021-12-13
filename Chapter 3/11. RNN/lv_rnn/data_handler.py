import pandas as pd
import numpy as np

df = pd.read_csv('data_akbilgic.csv')
df_train = df[:400]  #train split, hardcoded but you can use 0,8 * df
df_test = df[400:] 


def next_stock_batch(batch_size, n_steps, df_base):
    
    t_min = 0
    t_max = df_base.shape[0]
    
    x = np.zeros((batch_size, n_steps, 7)) # 7 is the number of features
    y = np.zeros((batch_size, n_steps, 1))
    
    starting_points = np.random.randint(t_min, t_max - n_steps -1 , batch_size)
    
    for k in range(batch_size):
        
        lmat = []
        
        for j in np.arange(n_steps + 1): #here is where the shift takes place
            lmat.append(df_base.iloc[starting_points[k] + j, 2:].values)
            
        lmat = np.array(lmat)
        
        x[k,:,:] = lmat[:n_steps,1:]
        y[k,:,0] = lmat[1:n_steps+1,0]
    
    return x, y
        
x,y = next_stock_batch(5,3,df_train)

print(x.shape)
print(y.shape)