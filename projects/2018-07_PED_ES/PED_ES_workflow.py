#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Jul 15 06:11:58 2018

@author: atilapaes

This is the workflow for the PED using ES


It evaluates the signals by calculation the ES SNR, then export the event catalog 
with some measured propetrties of each event, that are strong indicators of event presence

Workflow file: the function which gets a list of files and process it

"""

#%%
import pandas, numpy, os
import matplotlib.pyplot as plt
from tqdm import tqdm

import project_files.project_info_ES

# Shared modules path
import sys
sys.path.insert(0,project_files.project_info_ES.shared_modules_path)

# Shared modules import
import om_ES, om_load_data

#%%
def PED_from_filelist(df_catalog,core_index,log_file):
    catalog_gph_3c=pandas.read_csv('project_files/catalog_gph_3c.csv')
    
    output_file_name= project_files.project_info_ES.output_folder + project_files.project_info_ES.catalog_name + '-Core' + str(core_index) + '.csv'
    
    # Create empty catalog
    event_catalog= pandas.DataFrame(columns=['file_name','peak_time','snr','width'])

    for file_index in tqdm(range(len(df_catalog)-1)): #df_catalog.index.values)):
        #Load sequential files
        
        ms_data = om_load_data.load_sequential_border(files2load=[df_catalog.file_name[file_index],df_catalog.file_name[file_index+1]],sec_file2=10,bandpass_freqs=[10,100],folder=project_files.project_info_ES.ms_file_path)
        
        #print(ms_data[0].stats.starttime,ms_data[0].stats.endtime)
                
        # ES calculation
        es=om_ES.cf_es_selec_gph(ms_data,catalog_gph_3c)    
        es_mavg=om_ES.cf_moving_avg(signal=es,samples=200)
        #plt.figure(file_index)
        #plt.plot(es_mavg)
        #plt.show()
        #plt.close()
        # C.F. Analysis 
    
        # Analysis  of es_mavg and picking of index in max peaks
        mph=es_mavg.mean()+project_files.project_info_ES.peak_threshold_std*es_mavg.std()
        mpd=int(project_files.project_info_ES.peak_distance/ms_data[0].stats.delta)
    
        peaks_positions=om_ES.detect_peaks(x=es_mavg,mph=mph,mpd=mpd, show=project_files.project_info_ES.show_plot)
        
        # Processing the case of at least one identified peak
        # In this case it is assumed just a single peak due the signal time-window. Intervals with more than one event
        # Will present a anomalous width (or future ATP) that will be identified and splited from the regular processing.
        # These cases will be processed using more complex softwares.
        if len(peaks_positions)!=0: 
            
            for peak_index in range(len(peaks_positions)):
                valid_event,snr,peak_time,width = om_ES.peak_properties_v2(es_mavg,peaks_position = peaks_positions[peak_index],
                        start_time=ms_data[0].stats.starttime,delta_time=ms_data[0].stats.delta,
                        SNR_threshold=mph,width_min=project_files.project_info_ES.width_min,width_max=project_files.project_info_ES.width_max)

                if valid_event==True:
                    event_catalog=event_catalog.append({'file_name':df_catalog.file_name[file_index],'peak_time':peak_time,'snr':snr,'width':width},ignore_index=True) 
            
    
        if (file_index % 10 == 0) or  (file_index == len(df_catalog)-1):
            event_catalog.to_csv(output_file_name,sep=',',line_terminator='\n',index=False)
    
    print('DONE with Core '+str(core_index))
    
    if project_files.project_info_ES.os_used=='mac':
        os.system('say "Core done"')
        
    
    #%%     
    return()