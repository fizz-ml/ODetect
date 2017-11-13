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

    # Get co2 segment
    co2segment = f['signal']['co2']['y'][0][0:segment_length]
    time = np.arange(0,segment_length)/sample_freq

    # Get trough detections
    troughs_idx, troughs_period = calc_co2_troughs(co2segment)
    troughs_time_period = troughs_period/sample_freq
    troughs_time = troughs_idx/sample_freq

    # Plot
    fig, ax1 = plt.subplots()
    ax2 = ax1.twinx()

    # Plot co2 signal
    ax1.plot(time, co2segment, 'b-')
    ax1.set_ylabel("co2", color='b')

    # Put timestamp labels
    for x, y in zip(troughs_time, troughs_time_period):
        ax2.annotate('{:0.2f}'.format(x), xy=(x+0.4,min(troughs_time_period)), textcoords='data', backgroundcolor='w', alpha=0.5)

    # Plot trough detection
    ax2.plot(troughs_time, troughs_time_period, 'rx')

    # Draw timestamp lines
    for trough_time in troughs_time:
        ax2.axvline(x = trough_time, color='red')
    ax2.set_ylabel("period in seconds", color='red')

    # Draw label lines
    label_exp = np.squeeze(f['labels']['co2']['startexp']['x'])
    label_exp = label_exp[0:np.searchsorted(label_exp, segment_length)]/sample_freq
    label_insp = np.squeeze(f['labels']['co2']['startinsp']['x'])
    label_insp = label_insp[0:np.searchsorted(label_insp, segment_length)]/sample_freq

    for t in label_exp:
        ax2.axvline(x = t, color='g')
    for t in label_insp:
        ax2.axvline(x = t, color='y')


    plt.show()

