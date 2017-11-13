import sys
import h5py
import matplotlib.pyplot as plt
from scipy import signal
import numpy as np
from preprocess.features import calc_co2_troughs

# mat_dict = scipy.io.loadmat(sys.argv[1])
with h5py.File(sys.argv[1], 'r') as f:
    segment_length = 50000
    sample_freq = 300.0
    bpm = True

    # Get co2 segment
    co2segment = f['signal']['co2']['y'][0][0:segment_length]
    time = np.arange(0,segment_length)/sample_freq

    # Get trough detections
    troughs_idx, troughs_period = calc_co2_troughs(co2segment)
    troughs_time_period = troughs_period/sample_freq
    troughs_time = troughs_idx/sample_freq

    # Plot
    fig, ax1 = plt.subplots()

    # Plot trough detection
    ax1.set_xlabel("Time in s")
    if bpm:
        ax1.plot(troughs_time, np.reciprocal(troughs_time_period)*60.0, 'r.-')
        ax1.set_ylabel("RR in bpm")
    else:
        ax1.plot(troughs_time, np.reciprocal(troughs_time_period), 'r.-')
        ax1.set_ylabel("RR in Hz")

    plt.show()

