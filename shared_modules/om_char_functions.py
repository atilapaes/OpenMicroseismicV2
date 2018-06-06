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
def kurt_1d(signal,samples):
    """
    Calculate the kurtosis for a 1-D signal
    """
    ###########################################################################
    def kurt(index,signal,samples):
    #Kurtosis of the signal at a particular index
        if index < samples:
            return(0)
        else:
            return(stats.kurtosis(signal[index-samples:index], axis=0, fisher=True, bias=True))
    ###########################################################################
    kurt_signal=signal.copy()
    for index in range(len(signal)):
        kurt_signal[index]=kurt(index,signal=signal,samples=samples)
    return(kurt_signal)
#%%



    
