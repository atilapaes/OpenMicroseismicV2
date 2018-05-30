#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue May 29 02:17:55 2018

@author: atilapaes

Repicking project 

Phase 2: Module for MS data loading
Starting on May 30 (with legacy code)

Objective: Build a module to get the catalog from Phase 1, load raw data, filter and delivery a MS slice
Guidelines: Use as much legacy code (previous projects) as possible



Part 1: Develop a function to create the whole table of files/time to load
Part 2: 
    Develop a function that uses this table to to to de loadind and everything else
        
"""

#%% Step 0: Loading libraries, catalogs and peojrct definitions

import pandas, numpy, obspy


obspy.core.utcdatetime.UTCDateTime.DEFAULT_PRECISION = 3 # Define time resolution as 0.001 seconds

# Load catalog of file names and SP time
catalog_event_n_time=pandas.read_csv('project_files/catalog_events_n_time.csv')

# Load catalog of files and times from project
#?????

#%% Step 2: Pre process the catalog from G.R.P. and output the date time of event
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
        
#%% Step 3: Use the previously developed scripts to load the raw SGY files
event_index=0


#%% 

#%% Step 4: load, slice and retunr


