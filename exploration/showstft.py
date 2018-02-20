from models.sfft import SFFTModel
import argparse
from glob import glob
import numpy as np
import os
import evaluation.loss_functions as loss_functions
import h5py
import matplotlib.pyplot as plt
import scipy.signal as signal
from preprocess.features import calc_co2_troughs

"""
Visualizes the short time fourier transform of the signal.
Produces graphs for each signal in the specified dataset.
The graphs are composed of one plot of the ppg and co2 waveforms and one plot of the 2D STFT spectrogram.
Red points on the spectrogram correspond to the equivalent instantaneous frequency derived from the labels.
"""

def visualize_dataset(dataset_path):
    for sample_path in glob(os.path.join(dataset_path, '*.mat')):
        print(sample_path)
        with h5py.File(sample_path, 'r') as data:
            max_length = 140000
            ppg_signal = np.squeeze(data['signal']['pleth']['y'][0:max_length])[0:max_length]
            inhale_idx = np.squeeze(data['labels']['co2']['startinsp']['x'])

            # Plot
            fig, [ax1, ax2] = plt.subplots(2,1)
            sample_freq = 300

            # Frequency
            max_bin = 60
            f,t, Zxx = signal.stft(ppg_signal, fs=sample_freq, nperseg=18000, noverlap=17950)
            ax2.pcolormesh(t, f[2:max_bin]*60, np.sqrt(np.abs(Zxx)[2:max_bin]))#/f[2:30, np.newaxis])
            inhale_period = np.empty_like(inhale_idx)
            inhale_period[1:] = np.diff(inhale_idx)
            inhale_period[0] = inhale_period[1]
            inhale_period = inhale_period/sample_freq
            ax2.set_xlabel("Time in s")
            ax2.plot(inhale_idx/sample_freq, np.reciprocal(inhale_period)*60.0, 'r.')
            ax2.set_ylabel("RR in bpm")
            ax2.set_ylim(f[2]*60, f[max_bin]*60)
            ax2.set_xlim(0, max_length/sample_freq)


            # Time
            co2segment = data['signal']['co2']['y'][0][0:max_length]
            time = np.arange(0,max_length)/sample_freq
            ax1.plot(time, co2segment)
            ax1.plot(time, ppg_signal)

            # Artif
            co2_artifs = data['labels']['co2']['artif']['x']
            pleth_artifs = data['labels']['pleth']['artif']['x']
            itartif = iter(co2_artifs)
            for x in itartif:
                ax1.axvspan(x/sample_freq, next(itartif)/sample_freq, color="blue", alpha=0.5)
            itartif = iter(pleth_artifs)
            for x in itartif:
                ax1.axvspan(x/sample_freq, next(itartif)/sample_freq, color="orange", alpha=0.5)

            ax1.set_xlim(0, max_length/sample_freq)

            figManager = plt.get_current_fig_manager()
            figManager.window.showMaximized()
            plt.show()

if __name__ == "__main__":
    # Parse Arguments
    parser = argparse.ArgumentParser(description='Process some integers.')
    parser.add_argument('dataset_name', type=str, help='Name of the dataset under raw containing the data folder of h5 files to be processed.')
    args = parser.parse_args()

    dataset_name = args.dataset_name

    # Load some data
    input_path = os.path.join('data', dataset_name, 'raw')
    print(visualize_dataset(input_path))
