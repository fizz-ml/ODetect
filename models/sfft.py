import models.model as model
import scipy.fftpack as fft
import numpy as np

SAMPLING_RATE = 300.0
class SFFTModel(model.Model):
    def __init__(self,window_size):
        self.window_size = window_size
        self._buffer = np.zeros(window_size)

    def __call__(self,x):
        """Return the next predicted point"""
        self._update_buffer(x)
        b = self._get_buffer()
        fft_bin = np.argmax(np.abs(fft.fft(b)))
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


