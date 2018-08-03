#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Aug  2 22:06:42 2018

@author: atilapaes

Workflow for ms data analysis
"""

import project_files.project_info_ES_qc

# Shared modules path
import sys
sys.path.insert(0,project_files.project_info_ES_qc.shared_modules_path)

# Shared modules import
import om_ES, om_signal_anomaly 

#%%
def data_analysis(ms_data,catalog_gph):
    """
    Input: 
    ms_data: stream of data imported by obspy
    catalog_gph: standart a catalog of gphs from project Open Microseismic
    
    Output: 
    energy_stack: numpy array with energy stack
    gph_energy: energy in each gph builded in a obspy stream with Z channel metadata
    """
    
    # Signal anomaly detection - Unitary tests
    catalog_gph = om_signal_anomaly.flag_zero_ch(catalog_gph,ms_data,dnz=0.9)
    catalog_gph = om_signal_anomaly.flag_loud_gph(catalog_gph,ms_data,threshold=0.15)
    catalog_gph = om_signal_anomaly.flag_noisy_gph(catalog_gph,ms_data,threshold=0.05)

    # ES building using just valid gphs
    energy_stack = om_ES.cf_es_selec_gph_v2(ms_data,catalog_gph, normalize=True)
    energy_stack = om_ES.cf_moving_avg(signal=energy_stack.data,samples=100)

    # energy in each valid gph
    """
    The signal MUST NOT be normalized in the monitoring workflow because dead or bad ch could risk other 2 chs
    """
    
    gph_energy=om_ES.gph_energy(ms_data,catalog_gph, normalize=False)
    for index_gph in range(len(gph_energy)):    
        if gph_energy[index_gph].data.max() !=0:
            gph_energy[index_gph]=gph_energy[index_gph].normalize() 
    return(gph_energy,energy_stack)#ms_data_energy)