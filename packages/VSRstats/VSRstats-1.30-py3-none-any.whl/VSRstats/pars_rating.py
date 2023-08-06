import numpy as np
from peakutils import peak
from struct import unpack
import math
import os

from pyhrv import tools
import matplotlib.pyplot as plt
from VSRstats.tools import *
from VSRstats.time_domain import time_domain

class pars_rating:
    
    def __init__(self, data, hz = 200, peaks=None):
        self.hz = hz if not(hz is None) else 200
        self.peaks = peaks
        if type(data) == list:
            data = np.array(data)
        if type(data) == np.ndarray:
            self.stats = (self._computeSignal(data) if
                           data.ndim == 1 else self._computeSignals(data))
        else:
            raise TypeError('Signal should be an np.ndarray')

    def _computeSignals(self, signals):
        return np.array([self.computeSignal(s) for s in signals])

    def _firstParam(self, M):       
        if (M <= 660):
            return 2
        elif (M <= 800):
            return 1
        elif (M >= 1000):
            return -1
        elif (M >= 1200):
            return -2
        return 0

    def _secoundParam(self, sdnn, vr, cv):
        if (sdnn <= 20 and vr <= .1 and cv <= 2):
            return 2
        elif (sdnn >= 100 and vr >= .3 and cv >= 8):
            return 1
        elif (vr >= .1 and vr <= .3):
            return 0
        elif (sdnn >= 100 and vr >= .45 and cv >= 8):
            return -1
        elif (vr >= .6):
            return -2
        return 0

    def _thirdParam(self, vr, am, IN):
        if(vr <= 60 and am >= 80 and IN >= 500):
            return 2
        elif(vr <= 150 and am >= 50 and IN >= 200):
            return 1
        elif(vr >= 300 and am <= 30 and IN <= 50):
            return -1
        elif(vr >= 500 and am <= 15 and IN <= 25):
            return -2
        return 0
    
    def _fourthParam(self, cv):
        if(cv <= 3):
            return 2
        if(cv >= 6):
            return -2
        return 0
    
    def _fifthParam(self, vlf, lf, hf):
        if(vlf >= 70 and lf >= 25 and hf <= 5):
            return 2
        elif(vlf >= 60 and hf <= 20):
            return 1
        elif(vlf <= 40 and hf >= 30):
            return -1
        elif(vlf <= 20 and hf >= 40):
            return -2
        return 0

    def _computeSignal(self, signal):
        obj = {}
        parsCount = 0

        HZstep = 1000 / self.hz
        
        stats = time_domain(signal, self.hz).stats

        peaks = (getPeaks(signal, self.hz)\
                if(self.peaks is None) else self.peaks)
        peaks_diff = nn_intervals(peaks)
        peaks_diff_ms = peaks_diff * HZstep

        M = np.mean(peaks_diff_ms)

        sdnn_ms = np.std(peaks_diff_ms)
        cv = (sdnn_ms / M) * 100

        n, bins, _ = plt.hist(peaks_diff_ms)
        M0 = bins[np.argmax(n)]
        AM0 = (sum(n) / 100) * max(n)
        vr = np.var(bins)
        IN = AM0 / (2 * M0 * vr)

        parsCount += abs(self._firstParam(M))
        parsCount += abs(self._secoundParam(sdnn_ms, vr/M, cv))
        parsCount += abs(self._thirdParam(vr, AM0, IN))       
        parsCount += abs(self._fourthParam(cv))
        parsCount += abs(self._fifthParam(stats['VLF'], stats['LF'], stats['HF']))
        return parsCount
