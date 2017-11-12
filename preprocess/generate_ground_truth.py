from ..algorithms.peakdetect import peakdetect

"""
Generates ground truth for a given dataset.
"""

def calc_co2_periods(data):
    '''
        Calculates all periods of the co2 signal.
    '''
    co2signal = data.
    peaks = peakdetect(co2signal)


