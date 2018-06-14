#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Jun 14 04:30:48 2018

@author: atilapaes

Module for Energy-Stacking 
"""
#%%
import pandas, numpy

#%%
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

#%%
def cf_moving_avg(signal,samples=100):
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
#%%