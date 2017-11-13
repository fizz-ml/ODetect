import sys
import h5py
import matplotlib.pyplot as plt
from scipy import signal
import numpy as np

# mat_dict = scipy.io.loadmat(sys.argv[1])
with h5py.File(sys.argv[1], 'r') as f:
    segment_length = 50000
    sample_freq = 300.0
    bpm = True

    # Get co2 segment
    co2segment = f['signal']['co2']['y'][0][0:segment_length]
    time = np.arange(0,co2segment.size)/sample_freq

    # Plot
    fig, ax1 = plt.subplots()

    # Plot trough detection
    ax1.set_xlabel("Time in s")
    ax1.plot(time, co2segment, 'r-')
    ax1.set_ylabel("co2")

    plt.show()

