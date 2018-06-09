#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Jun  9 01:18:26 2018

@author: atilapaes

ATP main script
"""

import pandas

import RP_data_loading, om_load_data

import project_files.project_info

#%%
event_catalog=pandas.read_csv('project_files/catalog_events_n_time.csv')


#%% DATA LOADING
#event_number=2

for event_number in range(10,20):
    # List of files to load
    files2load = RP_data_loading.define_files2load(event_catalog.file_name[event_number],int(event_catalog.sec[event_number]))

    #Load sequential files
    ms_data=om_load_data.load_sequential_files(files2load, input_sec=int(event_catalog.sec[event_number]),sec_before=project_files.project_info.sec2load_before, sec_after=project_files.project_info.sec2load_after,bandpass_freqs=project_files.project_info.bandpass_filter,folder=project_files.project_info.ms_file_path)
    
    # For testing
    #ms_data[30].plot()
