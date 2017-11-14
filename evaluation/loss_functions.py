import torch
import numpy as np
def CO2_timestamptofreq(X, sample_freq=300):
    """Takes an array of trough index-stamps and returns the frequency, computed using last n time-stamps
    """
    Y = np.empty((X.shape[0],1))
    for i in range(X.shape[0]-1):
        Y[i+1,:] =  (1/sample_freq)*(X[i+1,:] - X[i,:])

    Y[0] = Y[1]

    return Y




def RMSE(Y_, Y):
    """ Returns root mean squared error between Y_ and Y 
    """
    return torch.nn.MSELoss(Y_,Y)



