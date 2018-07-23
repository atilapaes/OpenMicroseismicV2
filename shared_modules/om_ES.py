#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Jun 14 04:30:48 2018

@author: atilapaes

Functions for microseismic event detection based on Energy-Stacking 
"""
#%%
import pandas, numpy

#%% Characteristic functions 
def cf_es_selec_gph(ms_data,catalog_gph_3c):
    """
    Module for energy stack
    Based on a list of selected geophones 
    """

    es=numpy.zeros(len(ms_data[0]))

    for gph_index in range(len(catalog_gph_3c)):
        # Adds energy though gph to the stack vection in case the gph status is valid
        if catalog_gph_3c.valid_gph[gph_index]==True:
            es=numpy.add(es,numpy.square(ms_data[catalog_gph_3c.ch_z[gph_index]].data))
            es=numpy.add(es,numpy.square(ms_data[catalog_gph_3c.ch_h1[gph_index]].data))
            es=numpy.add(es,numpy.square(ms_data[catalog_gph_3c.ch_h2[gph_index]].data))
    return(es)
###############################################################################

def cf_moving_avg(signal,samples=50):
    """
    This function calculates the moving average of a provided 1-C signal (array).
        
    """
    signal_ma = numpy.zeros((len(signal),))
    
    #Regular signal
    for index in range(samples//2, len(signal)-samples//2):
        signal_ma[index] = (numpy.sum(signal[index-samples//2:(index+samples//2)]))/samples
         
    #Borders of the signal
    
    signal_ma[0:samples//2] = 0
    signal_ma[len(signal)-samples//2:len(signal)] = 0
    signal_ma=signal_ma/signal_ma.max()
    
    return (signal_ma)
###############################################################################

#%% Specific funtions

def peak_properties(es_mavg,peaks_position,start_time,delta_time,SNR_threshold,width_min,width_max):
    """
    Calculates the SNR and Width of the peak. Then decide if peak is into the defined parameters range.
    
    These loops finds the left and right indexes where the ES curve reaches the threshold
    """
    for index in range(peaks_position,len(es_mavg),1):
        right_index = len(es_mavg)
        if (es_mavg[index] <= SNR_threshold): #The ast part includes signal border as well
            right_index = index
            break

    for index in range(peaks_position,-1,-1): # Runs loop backward until zero
        left_index = 0
        if (es_mavg[index] <= SNR_threshold):
            left_index=index
            break

    peak_time = start_time + numpy.argmax(es_mavg)*delta_time
    SNR = es_mavg.max()/es_mavg.mean()
    width = (right_index - left_index)*delta_time
    
    #print("============",SNR,peak_time,width)
    
    if (SNR >= SNR_threshold) and (width >= width_min) and (width <= width_max):
        return([True,SNR,peak_time,width])
    else:
        return([False,None,None,None])
###############################################################################


def peak_properties_v2(es_mavg,peaks_position,start_time,delta_time,SNR_threshold,width_min,width_max):
    """
    Calculates the SNR and Width of the peak. Then decide if peak is into the defined parameters range.
    
    These loops finds the left and right indexes where the ES curve reaches the threshold
    """
    for index in range(peaks_position,len(es_mavg),1):
        right_index = len(es_mavg)
        if (es_mavg[index] <= SNR_threshold): #The ast part includes signal border as well
            right_index = index
            break

    for index in range(peaks_position,-1,-1): # Runs loop backward until zero
        left_index = 0
        if (es_mavg[index] <= SNR_threshold):
            left_index=index
            break

    peak_time = start_time + peaks_position*delta_time
    snr = es_mavg[peaks_position]/es_mavg.mean()
    width = (right_index - left_index)*delta_time
    
    #print("============",SNR,peak_time,width)
    
    if (snr >= SNR_threshold) and (width >= width_min) and (width <= width_max):
        return([True,snr,peak_time,width])
    else:
        return([False,None,None,None])
###############################################################################


def detect_peaks(x, mph=None, mpd=1, threshold=0, edge='rising',
                 kpsh=False, valley=False, show=False, ax=None):

    import numpy

    """Detect peaks in data based on their amplitude and other features.
    
    
    Detect peaks in data based on their amplitude and other features.
    http://nbviewer.jupyter.org/github/demotu/BMC/blob/master/notebooks/DetectPeaks.ipynb

    Atila's example
    u=detect_peaks.detect_peaks(data1, mph=numpy.mean(data1)+1.5*numpy.std(data1), mpd=100, show=True)
    
    
    Parameters
    ----------
    x : 1D array_like
        data.
    mph : {None, number}, optional (default = None)
        detect peaks that are greater than minimum peak height.
    mpd : positive integer, optional (default = 1)
        detect peaks that are at least separated by minimum peak distance (in
        number of data).
    threshold : positive number, optional (default = 0)
        detect peaks (valleys) that are greater (smaller) than `threshold`
        in relation to their immediate neighbors.
    edge : {None, 'rising', 'falling', 'both'}, optional (default = 'rising')
        for a flat peak, keep only the rising edge ('rising'), only the
        falling edge ('falling'), both edges ('both'), or don't detect a
        flat peak (None).
    kpsh : bool, optional (default = False)
        keep peaks with same height even if they are closer than `mpd`.
    valley : bool, optional (default = False)
        if True (1), detect valleys (local minima) instead of peaks.
    show : bool, optional (default = False)
        if True (1), plot data in matplotlib figure.
    ax : a matplotlib.axes.Axes instance, optional (default = None).

    Returns
    -------
    ind : 1D array_like
        indeces of the peaks in `x`.

    Notes
    -----
    The detection of valleys instead of peaks is performed internally by simply
    negating the data: `ind_valleys = detect_peaks(-x)`
    
    The function can handle NaN's 

    See this IPython Notebook [1]_.

    References
    ----------
    .. [1] http://nbviewer.ipython.org/github/demotu/BMC/blob/master/notebooks/DetectPeaks.ipynb

    """

    x = numpy.atleast_1d(x).astype('float64')
    if x.size < 3:
        return numpy.array([], dtype=int)
    if valley:
        x = -x
    # find indices of all peaks
    dx = x[1:] - x[:-1]
    # handle NaN's
    indnan = numpy.where(numpy.isnan(x))[0]
    if indnan.size:
        x[indnan] = numpy.inf
        dx[numpy.where(numpy.isnan(dx))[0]] = numpy.inf
    ine, ire, ife = numpy.array([[], [], []], dtype=int)
    if not edge:
        ine = numpy.where((numpy.hstack((dx, 0)) < 0) & (numpy.hstack((0, dx)) > 0))[0]
    else:
        if edge.lower() in ['rising', 'both']:
            ire = numpy.where((numpy.hstack((dx, 0)) <= 0) & (numpy.hstack((0, dx)) > 0))[0]
        if edge.lower() in ['falling', 'both']:
            ife = numpy.where((numpy.hstack((dx, 0)) < 0) & (numpy.hstack((0, dx)) >= 0))[0]
    ind = numpy.unique(numpy.hstack((ine, ire, ife)))
    # handle NaN's
    if ind.size and indnan.size:
        # NaN's and values close to NaN's cannot be peaks
        ind = ind[numpy.in1d(ind, numpy.unique(numpy.hstack((indnan, indnan-1, indnan+1))), invert=True)]
    # first and last values of x cannot be peaks
    if ind.size and ind[0] == 0:
        ind = ind[1:]
    if ind.size and ind[-1] == x.size-1:
        ind = ind[:-1]
    # remove peaks < minimum peak height
    if ind.size and mph is not None:
        ind = ind[x[ind] >= mph]
    # remove peaks - neighbors < threshold
    if ind.size and threshold > 0:
        dx = numpy.min(numpy.vstack([x[ind]-x[ind-1], x[ind]-x[ind+1]]), axis=0)
        ind = numpy.delete(ind, numpy.where(dx < threshold)[0])
    # detect small peaks closer than minimum peak distance
    if ind.size and mpd > 1:
        ind = ind[numpy.argsort(x[ind])][::-1]  # sort ind by peak height
        idel = numpy.zeros(ind.size, dtype=bool)
        for i in range(ind.size):
            if not idel[i]:
                # keep peaks with the same height if kpsh is True
                idel = idel | (ind >= ind[i] - mpd) & (ind <= ind[i] + mpd) \
                    & (x[ind[i]] > x[ind] if kpsh else True)
                idel[i] = 0  # Keep current peak
        # remove the small peaks and sort back the indices by their occurrence
        ind = numpy.sort(ind[~idel])

    if show:
        if indnan.size:
            x[indnan] = numpy.nan
        if valley:
            x = -x
        _plot(x, mph, mpd, threshold, edge, valley, ax, ind)

    return ind


def _plot(x, mph, mpd, threshold, edge, valley, ax, ind):
    """Plot results of the detect_peaks function, see its help."""
    import numpy
    try:
        import matplotlib.pyplot as plt
    except ImportError:
        print('matplotlib is not available.')
    else:
        if ax is None:
            _, ax = plt.subplots(1, 1, figsize=(8, 4))

        ax.plot(x, 'b', lw=1)
        if ind.size:
            label = 'valley' if valley else 'peak'
            label = label + 's' if ind.size > 1 else label
            ax.plot(ind, x[ind], '+', mfc=None, mec='r', mew=2, ms=8,
                    label='%d %s' % (ind.size, label))
            ax.axhline(mph,color='cyan')
            
            ax.legend(loc='best', framealpha=.5, numpoints=1)
        ax.set_xlim(-.02*x.size, x.size*1.02-1)
        ymin, ymax = x[numpy.isfinite(x)].min(), x[numpy.isfinite(x)].max()
        yrange = ymax - ymin if ymax > ymin else 1
        ax.set_ylim(ymin - 0.1*yrange, ymax + 0.1*yrange)
        ax.set_xlabel('data #', fontsize=14)
        ax.set_ylabel('Amplitude', fontsize=14)
        mode = 'Valley detection' if valley else 'Peak detection'
        ax.set_title("%s (mph=%s, mpd=%d, threshold=%s, edge='%s')"
                     % (mode, str(mph), mpd, str(threshold), edge))
        # plt.grid()
        plt.show()
#%%   