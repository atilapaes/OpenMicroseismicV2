#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri May 25 16:21:42 2018

@author: atilapaes

This module is part of the Phase 1 in the Repicking (RP) project

The objective is to use the previous catalogs of events and SP ATP from the student G.R.P.
and produce a single catalog containing the file names and an the mean of the SP for each event.


"""
#%% Importing libs and loading catalogs
from tqdm import tqdm
import pandas

catalog_events=pandas.read_csv('FileNameCatalog.csv')
catalog_files=pandas.read_csv('file_list.txt')
catalog_sp=pandas.read_csv('sp.csv')

#%% This block was used to consult if all files contaning events from G.R.P. 
# catalog are present on the list of files into the HD
# -->>> Answer is YES <<<-----
def consult_event_files_on_hd(catalog_events,catalog_files):
    for index in range(len(catalog_events)):
        if not(catalog_events.file_name[index] in catalog_files.file_name.values):
            print('file ',catalog_events.file_name[index],' not present')

    return()
## Call this function to make sure all files from German's Catalog is into the HD
#consult_event_files_on_hd(catalog_events,catalog_files)


#%% The next step is to calculate the mean from the SP ATP from Germans method
# to have a good idea of where to look fot the event

#### Vectorized method: Total time: 127 ms ####################################
def mean_sec(catalog_events,catalog_sp):
    
    catalog_events['sec']=0.0

    def mean_row(row):
        return(row.values.mean())

    catalog_events['sec']=catalog_sp.apply(mean_row,axis=1)
    return(catalog_events)    

#%time mean_sec(catalog_events,catalog_sp) # Measuring the time - For test purposes

catalog_events=mean_sec(catalog_events,catalog_sp) # Apply the function to the Dataframe

###############################################################################

"""
#### Non-vectorized method (for benchmarking purpose only): Total time: 5min 30s (WOW)

def mean_sec_n_vec(catalog_events,catalog_sp):

    catalog_events['sec']=0.0
    for index in tqdm(range(len(catalog_events))):
        catalog_events.sec[index]=catalog_sp[index:index+1].values.mean()   
    return(catalog_events)
%time mean_sec_n_vec(catalog_events,catalog_sp)
"""
###############################################################################


catalog_events.to_csv('project_files/catalog_events_n_time.csv', sep=',', line_terminator='\n', index=False)
# At this point I've merged the catalog of file names and SP time (and save it for backup)

