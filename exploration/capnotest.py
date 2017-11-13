import scipy.io
import pdb
import sys
import h5py
import matplotlib.pyplot as plt
from scipy import signal
import numpy as np
from scipy.fftpack import fft, ifft

# mat_dict = scipy.io.loadmat(sys.argv[1])
with h5py.File(sys.argv[1], 'r') as f:
    print( f.keys() )
    fig, (ax1, ax2) = plt.subplots(2, 1, sharey=True)
    ax1.plot(np.arange(0,15000)/300.0, f['signal']['pleth']['y'][0][0:15000])
    print(f['signal']['pleth']['y'].shape)
    ax2.plot(np.arange(0,15000)/300.0, f['signal']['co2']['y'][0][0:15000])
    plt.show()

    # pdb.set_trace()

    '''
    print(f['param']['samplingrate']['co2'][0][0])

    fig, (ax1, ax2) = plt.subplots(2, 1, sharey=True)

    ax1.plot(np.arange(10,100)/10000.0*300.0,(np.abs(fft(f['signal']['pleth']['y'][0][0:10000])[10:100])))

    print((20+np.argmax((np.abs(fft(f['signal']['pleth']['y'][0][0:10000])[10:100]))))/100000.0*300.0)

    ax2.plot(np.arange(10,100)/10000.0*300.0,(np.abs(fft(f['signal']['co2']['y'][0][0:10000])[10:100]))*2)
    plt.show()
    print((20+np.argmax((np.abs(fft(f['signal']['co2']['y'][0][0:10000])[10:100]))))/10000.0*300.0)
    '''

    fig, (ax1, ax2) = plt.subplots(2, 1, sharey=True)
    freq, t, Zxx = signal.stft(f['signal']['co2']['y'][0][0:1500000], 300.0, nperseg=10000)
    print(freq[0:100],t)
    plt.xlabel('Time in s')
    plt.ylabel('Freq in Hz')
    ax1.set_title('co2')
    ax1.pcolormesh(t, freq[0:80], np.abs(Zxx[0:80]), cmap="jet")

    freq, t, Zxx = signal.stft(f['signal']['pleth']['y'][0][0:1500000], 300.0, nperseg=10000)
    print(freq[0:100],t)
    ax2.pcolormesh(t, freq[0:80], np.abs(Zxx[0:80]), cmap="jet")
    ax2.set_title('pleth')
    plt.show()

    widths = np.arange(1, 110)*10
    cwtmatr = signal.cwt(f['signal']['pleth']['y'][0][0:100000], signal.ricker, widths)
    plt.imshow(np.abs(cwtmatr), extent=[-1, 1, 1, 2100], cmap='PRGn', aspect='auto', vmax=np.abs(cwtmatr).max(), vmin=-np.abs(cwtmatr).max())
    plt.show()

    pdb.set_trace()
