#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Jun  9 01:18:26 2018

@author: atilapaes

This module is used as a preliminar evaluation of G.R.P. event catalog. 

It evaluates the signals by calculation the ES SNR, then export the event catalog 
with some measured propetrties of each event, that are strong indicators of event presence


Steps:
1) Review former projects (Based on ATP_main) - DONE
2) Recreate the SNR function in a faster way - DONE
3) Evaluate if event is under a range of parameters - Done
4) Update catalog and export CSV - Done
5) Make processing multicore - Done
6) Function to merge catalogs - Done
    
Future Activities:
7) Export catalog of processed events to obspy.core.event.Catalog

"""

import pandas, obspy, numpy

from tqdm import tqdm # Using fancy loading bar

import RP_data_loading, om_load_data, om_ES

import project_files.project_info


#%%
# Loading catalogs  and project specs
event_catalog=pandas.read_csv('project_files/catalog_events_n_time.csv')    # Events to Repick
event_catalog=event_catalog[:20 ]
event_catalog['valid_event']=None
event_catalog['peak_time']=None
event_catalog['snr']=None
event_catalog['width']=None

catalog_gph_3c=pandas.read_csv('project_files/catalog_gph3c_gc_samples3_selected2.csv')          # Gph information
obspy.core.utcdatetime.UTCDateTime.DEFAULT_PRECISION = 3 # Define time resolution as 0.001 seconds    

#%% ###########################################################################

def PEV_from_catalog(event_catalog): 
    """
    Potential event validation from a Pandas Catalog
    """
    for event_number in tqdm(event_catalog.index.values): # event_number is part of the list of indexes in the sliced Dataframe
        
        #%% DATA LOADING
        # List of files to load
        files2load = RP_data_loading.define_files2load(event_catalog.file_name[event_number],int(event_catalog.sec[event_number]))
    
        #Load sequential files
        ms_data=om_load_data.load_sequential_files(files2load, input_sec=int(event_catalog.sec[event_number]),sec_before=project_files.project_info.sec2load_before, sec_after=project_files.project_info.sec2load_after,bandpass_freqs=project_files.project_info.bandpass_filter,folder=project_files.project_info.ms_file_path)
    
        #%% Signal processing body
    
        # ES calculation
        es=om_ES.cf_es_selec_gph(ms_data,catalog_gph_3c)    
        es_mavg=om_ES.cf_moving_avg(signal=es,samples=50)
    
        # C.F. Analysis 
    
        # Analysis  of es_mavg and picking of index in max peaks
        mph=es_mavg.mean()+project_files.project_info.peak_threshold_std*es_mavg.std()
        mpd=int(project_files.project_info.peak_distance/ms_data[0].stats.delta)
    
        peaks_positions=om_ES.detect_peaks(x=es_mavg,mph=mph,mpd=mpd, show=project_files.project_info.show_plot)
    
        # Processing the case of at least one identified peak
        # In this case it is assumed just a single peak due the signal time-window. Intervals with more than one event
        # Will present a anomalous width (or future ATP) that will be identified and splited from the regular processing.
        # These cases will be processed using more complex softwares.
        if len(peaks_positions)!=0: 
            event_catalog['valid_event'][event_number],event_catalog['snr'][event_number],event_catalog['peak_time'][event_number],event_catalog['width'][event_number] = om_ES.peak_properties(es_mavg,peaks_position=peaks_positions.max(),start_time=ms_data[0].stats.starttime,delta_time=ms_data[0].stats.delta,SNR_threshold=mph,width_min=project_files.project_info.width_min,width_max=project_files.project_info.width_max)
            #print("========",event_catalog['valid_event'][event_number],event_catalog['snr'][event_number],event_catalog['peak_time'][event_number],event_catalog['width'][event_number])
            
        else:
            print('No peak detected')
            event_catalog['valid_event'][event_number],event_catalog['snr'][event_number],event_catalog['peak_time'][event_number],event_catalog['width'][event_number] = False,None,None,None
        
    #%% Legacy code: Export CSV each 100 events (used in single core only)
    #if (event_number % 100 == 0) or (event_number == len(event_catalog)-1):
    #    event_catalog.to_csv('event_catalog_processed.csv',line_terminator='\n',)
    
    return(event_catalog)

#%% ###########################################################################        
def parallelize(data,func):
    """
    Function to split Pandas Dataframe in chunks and process each one in one core
    Source: http://blog.adeel.io/2016/11/06/parallelize-pandas-map-or-apply/
    """
    from multiprocessing import cpu_count, Pool
    partitions=cpu_count()    
    data_split = numpy.array_split(data, partitions) # Split an array into multiple sub-arrays of different sizes
    pool = Pool(processes = partitions )    
    results_df = pandas.concat(pool.map(func, data_split))    
    pool.close()
    pool.join()    
    return(results_df)
###############################################################################        

#%% Main function
if __name__ == '__main__':
    ######
    print('===================== Processing start')
    event_catalog_v2=parallelize(data=event_catalog, func=PEV_from_catalog)
    event_catalog_v2.to_csv('project_files/event_catalog_processed_v6.csv',line_terminator='\n',)
    print(event_catalog_v2)
    print('===================== Processing DONE!')
