import models.model as model
import scipy.fftpack as fft
import numpy as np

SAMPLING_RATE = 300.0
class SFFTModel(model.Model):
    def __init__(self,window_size):
        self.window_size = window_size
        self._buffer = np.zeros(window_size)
        self._max_freq = 0.6
        self._min_freq = 0.05

    def __call__(self,x):
        """Return the next predicted point"""
        self._update_buffer(x)
        b = self._get_buffer()
        max_bin = np.ceil(self._max_freq / SAMPLING_RATE * self.window_size).astype(np.int32)
        min_bin = np.floor(self._min_freq / SAMPLING_RATE * self.window_size).astype(np.int32)
        fft_bin = np.argmax(np.abs(fft.fft(b))[min_bin:max_bin]) + min_bin
        y = fft_bin * SAMPLING_RATE / self.window_size
        return y

    def reset():
        """Reset the model"""
        self._buffer = np.zeros(window_size)
        self._buffer_point = 0

    def _update_buffer(self,x):
        self._buffer = np.roll(self._buffer,1)
        self._buffer[0] = x

    def _get_buffer(self):
        return self._buffer


