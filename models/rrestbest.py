#import models.model as model
from scipy.signal import lfilter,sosfilt 
from scipy.signal import cheby1,butter 
import numpy as np
SAMPLING_RATE = 300.0
THRESHOLD = 0.2

output = open("output.txt","w")

class RRESTModel():
    def __init__(self,buffer_time,lbe,pd_threshold):
        self._pd_threshold = pd_threshold
        self._buffer_time = buffer_time*SAMPLING_RATE

        self._init_vars()
        
    def _init_vars(self):
        #first peak detector
        self._peak_to_peak_time = 0
        self._last_through_amplitude = 0
        self._last_peak_amplitude  = 0
        self._last_peak = 0
        self._last_through = 0
        self.max = 0
        self.min = 0
        self._peak = True
        self._rising = False

        #bandpass filter from 0.1 to 0.5 HZ
        critical_frequencies = (0.1*2/SAMPLING_RATE,0.5*2/SAMPLING_RATE)
        #filter_parameters
        n = 10
        self._fsos = butter(n,critical_frequencies,btype="bandpass",output="sos")
        print(self._fsos.shape)
        #filter_states
        self._fs = np.zeros((3,n,2))

        #buffer
        self._buffer = np.zeros((3,int(self._buffer_time)))

    def __call__(self,x):
        """Return the next predicted point"""
        self._update_buffer(x)
        y = self.get_respiratory_rate()
        return y

    def reset(self):
        """Reset the model"""
        self._init_vars()

    def _update_buffer(self,x):

        current_val = x
        #check for peak 
        if (self._peak and current_val < self.max - self._pd_threshold):
            self.min = current_val
            self._peak_to_peak_time = self._last_peak
            self._last_peak = -1
            self._last_peak_amplitude = current_val
            self._peak = False
        #check for through
        if (not self._peak and current_val > self.min + self._pd_threshold):
            self.max = current_val
            self._last_through = -1
            self._last_through_amplitude = current_val
            self._peak = True 

        self._last_peak += 1
        self._last_through += 1

        #update min and max
        if (self.max < current_val):
            self.max = current_val
        if (self.min > current_val):
            self.min = current_val

        #update buffers
        self._buffer = np.roll(self._buffer,1)

        self._buffer[0,-1],self._fs[0] = sosfilt(self._fsos,[self._peak_to_peak_time],zi=self._fs[0])
        self._buffer[1,-1],self._fs[1] = sosfilt(self._fsos,[(self._last_through_amplitude + self._last_peak_amplitude)/2],zi=self._fs[1])
        self._buffer[2,-1],self._fs[2] = sosfilt(self._fsos,[(self._last_through_amplitude - self._last_peak_amplitude)],zi=self._fs[2])


    def get_respiratory_rate(self):
        means = []
        for i in range(3):
            peaks, troughs = self._find_peaks_troughts(self._buffer[i])
            peak_amplitudes = self._buffer[i][peaks]
            trough_amplitudes = self._buffer[i][troughs]
            m, sd = self._count_resp(peaks,troughs,peak_amplitudes,trough_amplitudes)
            
            if sd < 4:
                means.append(m)

        return np.mean(means)


    def _find_peaks_troughts(self,signal):
        """naive_peak_detector"""
        a = signal[:-2]
        b = signal[1:-1]
        c = signal[2:]
        peaks = np.array(np.where(np.logical_and(a < b, b > c) != 0))+1
        troughs = np.array(np.where(np.logical_and(a > b, b < c) != 0))+1
        return peaks[0,:], troughs[0,:]
    
    def _count_resp(self,peaks,troughs,peak_amplitudes,trough_amplitudes):
        if (len(peaks) < 2 or len(troughs) < 1):
            return np.nan,np.nan
        sorted_amplitudes = np.sort(peak_amplitudes)
        q_3 = sorted_amplitudes[len(peak_amplitudes)*3//4]
        threshold = q_3*THRESHOLD
        #identify main peaks
        breaths = []
        main_peaks = peaks[peak_amplitudes > q_3*0.2 ]
        for i in range(len(main_peaks)-1):
            first = main_peaks[i]
            second = main_peaks[i+1]
            inter_troughs = np.where(np.logical_and(first < troughs, troughs < second))[0]
            inter_peaks = np.where(np.logical_and(first < peaks, peaks < second))[0]

            if len(inter_peaks) == 0 and len(inter_troughs) == 1 and \
                    trough_amplitudes[inter_troughs[0]] < 0:
                breaths.append(second-first)

        freqs = SAMPLING_RATE/np.array(breaths)
        print(freqs)
        mean = np.mean(freqs)
        std_dev = np.std(freqs)
        return mean,std_dev











    
