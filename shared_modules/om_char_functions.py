#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jun  5 19:15:46 2018

@author: atilapaes
"""

import obspy, numpy
import matplotlib.pyplot as plt
from scipy import stats

#%%
def kurt_1d(signal_1d,samples):
    """
    Calculate the kurtosis for a 1-D signal
    """
    ###########################################################################
    def kurt(index,signal_1d,samples):
    #Kurtosis of the signal at a particular index
        if index < samples:
            return(0)
        else:
            return(stats.kurtosis(signal_1d[index-samples:index], axis=0, fisher=True, bias=True))
    ###########################################################################
    kurt_signal=signal_1d.copy()
    for index in range(len(signal_1d)):
        kurt_signal[index]=kurt(index,signal_1d=signal_1d,samples=samples)
    return(kurt_signal)
#%%
def kurt_nd(signal_nd, samples):
    """
    Apply the kurtosis function to all traces in a OBSPY stream
    """
    kurt_array=signal_nd.copy()
    for index in range(len(signal_nd)):
        kurt_array[index].data=kurt_1d(signal_1d=signal_nd[index].data,samples=samples)
    return(kurt_array)
#%%
