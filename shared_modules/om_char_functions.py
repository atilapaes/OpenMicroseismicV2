#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jun  5 19:15:46 2018

@author: atilapaes
"""

import obspy, numpy, pandas
import multiprocessing as mp
import matplotlib.pyplot as plt
from scipy import stats

ms_data=obspy.read("project_files/26972.16.10.31.23.32.00.dat")
#%% FUNCTIONS FOR KURTOSIS
##############################################################################
def kurt_1d(signal_1d,samples):
    """
    Calculate the kurtosis for a 1-D signal
    """
    #=============================================
    def kurt(index,signal_1d,samples):
    #Kurtosis of the signal at a particular index
        if index < samples:
            return(0)
        else:
            return(stats.kurtosis(signal_1d[index-samples:index], axis=0, fisher=True, bias=True))
    #=============================================
    kurt_signal=signal_1d.copy()
    for index in range(len(signal_1d)):
        kurt_signal[index]=kurt(index,signal_1d=signal_1d,samples=samples)
    return(kurt_signal)

##############################################################################
def kurt_nd(signal_nd, samples):
    """
    Apply the kurtosis function to all traces in a OBSPY stream
    """
    kurt_array=signal_nd.copy()
    for index in range(len(signal_nd)):
        kurt_array[index].data=kurt_1d(signal_1d=signal_nd[index].data,samples=samples)
    return(kurt_array)

#%% FUNCTIONS FOR STREAM AND DF EXCHANGE
##############################################################################
def stream2df(stream):
    """
    Transforms a OBSPY stream into a Pandas datafram
    The traces from OBPSY stream become columns in the Pandas DataFrame
    """
    df=pandas.DataFrame(0,index=numpy.arange(len(stream[0])),columns=numpy.arange(len(stream)))
    for trace in range(len(stream)):
        df[trace]=stream[trace].data
    return(df)


def df2stream(stream,df):
    """
    Transforms the columns of a df on the traces on a OBSPY stream
    """
    for trace in range(len(df.columns)):
        stream[trace].data=df[trace].values
    return(stream)
#%%
