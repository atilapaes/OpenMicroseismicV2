#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue May 29 02:17:55 2018

@author: atilapaes

Repicking project 

Phase 2: Module for MS data loading
Starting on May 30 (with code from previous projects)

Objective: Build a module to get the catalog from Phase 1, load raw data, filter and delivery a MS slice. 
(The idea is to delivery the data to be processes in the next step of ATP)
Guidelines: Use as much legacy code (previous projects) as possible


Step 1: Develop a function to extract the times from G.R.P catalog of events
Step 2: Develop a function that uses a date_time object to load the respective time slice from the raw dataset. Then apply a bandpass filter.
        
"""

#%% Step 0: Loading libraries, catalogs and preproject definitions

# Include path to all modules into shared_modules folder
import sys
sys.path.insert(0,'/Users/atilapaes/Documents/GitHub/OpenMicroseismicV2/shared_modules/')

import pandas, obspy # General Libs

import om_load_data, om_catalog # O.M. shared modules

import project_files.project_info # Project info from nested folder (must create a blank __init__.py in all folders)


obspy.core.utcdatetime.UTCDateTime.DEFAULT_PRECISION = 3 # Define time resolution as 0.001 seconds


#%% Step 0.1: Load project catalogs and prepare it for quick use
# Load catalog of file names and SP time
catalog_event_n_time=pandas.read_csv('project_files/catalog_events_n_time.csv')

# Import CSV catalog contaning strs for file_names and starttimes. Convert starttime to OBSPY date_time class
# Could be considered as Step 2.0
catalog_time_n_files=pandas.read_csv('project_files/catalog_time_n_files.csv')
catalog_time_n_files['date_time']=catalog_time_n_files['date_time'].apply(lambda x: obspy.core.utcdatetime.UTCDateTime(x))


#%% Step 1: Pre process the catalog from G.R.P. and output the date time of event
# OBS: This function was build to consult one event per time

def event_date_time(catalog_event_n_time,event_index):
    """
    Get a event_index and returns its respective date and time in OBSPY format
    """
    
    def file_name2str(file_name): 
        """
        Transforms the file name from catalog into a str suitable to be transformed by obspy datetime format
        """
        return('20'+file_name.split('.')[1]+'-'+file_name.split('.')[2]+'-'+file_name.split('.')[3]+'T'+file_name.split('.')[4]+':'+file_name.split('.')[5]+':'+file_name.split('.')[6]+'.'+'000')

    date_time=None # Variable initialization
    
    if (event_index >= 0) and (event_index < len(catalog_event_n_time)):
        file_name = catalog_event_n_time.file_name[event_index]
        event_second = float("{:.3f}".format(catalog_event_n_time.sec[event_index])) # convert the second from catalof in a 3 decimal places float

        date_time=obspy.core.utcdatetime.UTCDateTime(file_name2str(file_name))+event_second
        
    else:
        print('ERROR! Event_index out of catalog range')

    return(date_time)
        

#%% Setp 2: Load ms data
# OBS: - Work with OBSPY datetime format only. Resolution 1 second

def rp_data_loading(input_time,sec_before,sec_after,catalog_time_n_files,bandpass_freqs=[10,200]):
    # Step 2.1: Get name(s) of file(s) to load
    files2load=om_catalog.time2file_name(input_time,sec_before,sec_after,catalog_time_n_files)

    # Step 2.2: Load, slice and filter data
    ms_data=om_load_data.load_sequential_files(files2load, input_time, sec_before, sec_after,bandpass_freqs,folder=project_files.project_info.ms_file_path)
    
    return(ms_data)

#%% Commands to test the function from Step 3. It is working so far.

#input_time=obspy.core.utcdatetime.UTCDateTime('2016-11-20T06:20:30')
#ms_data=rp_data_loading(input_time,sec_before=15,sec_after=10,catalog_time_n_files=catalog_time_n_files,bandpass_freqs=[10,200])

#%%
def define_files2load(file_name,sec):
    """
    Returns the secondary file to load depenseing on the sec from the event catalog
    
    OBS: Not included the mechanism to prevent loading before catalog initialization of after catalog end
    """    
    df_files=pandas.read_csv('project_files/catalog_time_n_files.csv') # Complete list of file from G.R.P. catalog    
    file_list=[file_name] # Primary file
        
    if sec + project_files.project_info.sec2load_after > 60:        
        file_list.append(df_files.file_name[1+df_files[df_files['file_name']==file_name].index[0]])
    elif sec - project_files.project_info.sec2load_before < 0:
        file_list.append(df_files.file_name[-1+df_files[df_files['file_name']==file_name].index[0]])
    
    return(file_list)

#%%