import os, math
import numpy as np
from struct import unpack
import matplotlib.pyplot as plt
from biosppy.signals import bvp

# Visual show peaks
def showPeaks(signal):
    peaks = getPeaks(signal);
    fig = plt.figure(figsize=(30, 3))
    [ plt.axvline(p, color='r', lw=.5) for p in peaks]
    plt.plot(signal)
    plt.show()

# func to get peaks of signal
def getPeaks(signal, hz = 200):
    return bvp.bvp(signal, hz, show=False)['onsets']

# Read signal from file
def loadSignal(filepath):
    file = open(filepath, "rb").read()
    ufile = unpack('10000H', file)
    return np.array(ufile)

def nn_intervals(peaks):
    return np.array([peaks[i + 1] - peaks[i] for i in range(peaks.size-1)])

def nni_diff(peaks):
    return np.array([abs(peaks[i + 1] - peaks[i]) for i in range(peaks.size-1)])

def filterdSignal(signal, hz = 200):
    return bvp.bvp(signal, hz, show=False)["filtered"]

def normalize(signal):
    return np.array([(x - np.mean(signal))/np.std(signal) for x in signal])
