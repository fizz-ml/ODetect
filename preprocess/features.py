import os
import glob
import argparse
import numpy as np

from algorithms.peakdetect import peakdetect

"""
Generates ground truth for a given dataset.
"""
def calc_co2_troughs(co2signal):
    '''
        Returns the index of troughs and period between them for the supplied co2 signal.
        Note: Troughs are used over peaks since the troughs are more sharp for the co2 signal.
    '''
    # Only grab the troughs not the peaks
    _, troughs_idx_value = peakdetect(co2signal, delta=0.2)
    # Just need the position
    troughs_idx = np.asarray([x[0] for x in troughs_idx_value])
    # Also compute the period between the previous and the current trough
    troughs_period = np.empty_like(troughs_idx)
    # For the very first trough assume same period as next one
    troughs_period[1:] = np.diff(troughs_idx)
    troughs_period[0] = troughs_period[1]
    return [troughs_idx, troughs_period]



