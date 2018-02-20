"""
Script for testing the model.
"""
import models.learning.causalconvs.model as causalconv
import scipy.fftpack as fft
import numpy as np
import matplotlib.pyplot as plt
from torch.autograd import Variable
from torch import FloatTensor
from scipy import signal

def simple_causal_test():
    causcnn = causalconv.CausalCNN()
    x = np.random.randn(1600)/10+np.sin(np.arange(1600)/30)
    x = x.reshape(1,1,1600)
    y = causcnn(Variable(FloatTensor(x))).data.numpy()
    plt.plot(np.squeeze(x))
    plt.plot(np.arange(100)*16, np.squeeze(y))
    plt.show()

def simple_causal_learn_test():
    causcnn = causalconv.CausalCNN()
    x = np.random.randn(1600)/10+np.sin(np.arange(1600)/30)
    x = x.reshape(1,1,1600)
    y = causcnn(Variable(FloatTensor(x)))

    y = causcnn(Variable(FloatTensor(x))).data.numpy()
    plt.plot(np.squeeze(x))
    plt.plot(np.arange(100)*16, np.squeeze(y))
    plt.show()

def simple_signal():
    # x = np.random.randn(800)/10+np.sin(np.arange(800)/30)
    fs = 300
    N = 1600
    amp = 2 * np.sqrt(2)
    noise_power = 0.01 * fs / 2
    time = np.arange(N) / float(fs)
    mod = 500*np.cos(2*np.pi*0.25*time)
    carrier = amp * np.sin(2*np.pi*3e3*time + mod)
    noise = np.random.normal(scale=np.sqrt(noise_power),
                             size=time.shape)
    noise *= np.exp(-time/5)
    x = carrier + noise
    f,t, Zxx = signal.stft(x, fs=300, nperseg=300, noverlap=250)
    plt.pcolormesh(t, f, np.abs(Zxx))
    plt.show()


simple_signal()
# simple_causal_learn_test()
