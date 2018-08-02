#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Aug  1 15:44:25 2018

@author: atilapaes

This functions are used to flag channels and gph with signal anomalies
The output is a updated catalog_gph focused in the column 'valid_gph'
"""
import obspy, numpy

#%% 
def flag_zero_ch(catalog_gph,ms_data,dnz=0.9):
    """
    This function identifies the channels with more than 10% measurements equal zero and flag them as zero channels then its flag the GPH as not valid
    
    dnz = decimate non-zero (default = 0.9)
    """
    for gph_index in range(len(catalog_gph)):
        if (numpy.count_nonzero(ms_data[catalog_gph.ch_z[gph_index]].data) < len(ms_data[catalog_gph.ch_z[gph_index]].data)*dnz):
            catalog_gph.valid_z[gph_index] = False
            if catalog_gph.report[gph_index]==None:
                catalog_gph.report[gph_index]=[]
            catalog_gph.report[gph_index].append('z_zero')
        
        if (numpy.count_nonzero(ms_data[catalog_gph.ch_h1[gph_index]].data) < len(ms_data[catalog_gph.ch_h1[gph_index]].data)*dnz):
            catalog_gph.valid_h1[gph_index] = False
            if catalog_gph.report[gph_index]==None:
                catalog_gph.report[gph_index]=[]
            catalog_gph.report[gph_index].append('h1_zero')
        
        if (numpy.count_nonzero(ms_data[catalog_gph.ch_h2[gph_index]].data) < len(ms_data[catalog_gph.ch_h2[gph_index]].data)*dnz):
            catalog_gph.valid_h2[gph_index] = False
            if catalog_gph.report[gph_index]==None:
                catalog_gph.report[gph_index]=[]
            catalog_gph.report[gph_index].append('h2_zero')  
    
    for gph_index in range(len(catalog_gph)):
        catalog_gph.valid_gph[gph_index]=(catalog_gph.valid_z[gph_index] and catalog_gph.valid_h1[gph_index] and catalog_gph.valid_h2[gph_index])
    return(catalog_gph)
    
#%% 
def flag_loud_gph(catalog_gph,ms_data,threshold=0.15):
    """
    This function identifies the loud geophones and flag them to avoid their subsequent use. Designed for 3C gphs    
    This copy is used initially for keep metadata and time/data equivanlency
    It is based on Z channels
    
    theshold = max decimante for integral of energy
    """
    ms_data_energy = obspy.core.stream.Stream(traces=[ms_data[catalog_gph.ch_z.values[0]]])
    for gph_index in range(1,len(catalog_gph.ch_z.values)):
        ms_data_energy.append(ms_data[catalog_gph.ch_z.values[gph_index]])
        
    for gph_index in range(len(ms_data_energy)):
        ms_data_energy[gph_index].data = numpy.add(numpy.square(ms_data[catalog_gph.ch_z[gph_index]].data),numpy.add(numpy.square(ms_data[catalog_gph.ch_h1[gph_index]].data),numpy.square(ms_data[catalog_gph.ch_h2[gph_index]].data)))
         
    energy_ch = numpy.zeros(len(catalog_gph))
    for index_ch in range(len(ms_data_energy)):
        energy_ch[index_ch] = (numpy.trapz(ms_data_energy[index_ch].data))
        
    energy_ch_relative=energy_ch/numpy.sum(energy_ch)
    for index_ch in range(len(ms_data_energy)):
        print('gph ',index_ch,'. Relative energy ',energy_ch_relative[index_ch])

    """
    plt.figure(1)
    plt.plot(energy_ch_relative,'.r')
    plt.show(); plt.close()
    """    
    for gph_index in range(len(catalog_gph)):
        if energy_ch_relative[gph_index] >= threshold:
            catalog_gph.valid_gph[gph_index]=False
            if catalog_gph.report[gph_index]==None:
                catalog_gph.report[gph_index]=[]
            catalog_gph.report[gph_index].append('loud_gph')  
    return(catalog_gph)   

#%%
"""
catalog_gph = flag_zero_ch(catalog_gph,ms_data,dnz=0.9)
catalog_gph = flag_loud_gph(catalog_gph,ms_data,threshold=0.15)
"""