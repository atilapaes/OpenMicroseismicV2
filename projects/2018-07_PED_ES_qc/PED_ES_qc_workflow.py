#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Jul 15 06:11:58 2018

@author: atilapaes

This is the workflow for the PED using ES

It evaluates the signals by calculation the ES SNR in the Z channels, then export the event catalog 
with some measured propetrties of each event, that are strong indicators of event presence

"""
#%%
import pandas
from tqdm import tqdm
import project_files.project_info_ES_qc

# Shared modules path
import sys
sys.path.insert(0,project_files.project_info_ES_qc.shared_modules_path)

# Shared modules import
import om_ES, om_load_data, PED_ES_qc_data_analysis

#%%
def PED_from_filelist(df_catalog,core_index,log_file):
    
    output_file_name= project_files.project_info_ES_qc.output_folder + project_files.project_info_ES_qc.catalog_name + '-Core' + str(core_index) + '.csv'
    
    # Create empty catalog
    event_catalog= pandas.DataFrame(columns=['file_name','peak_time','snr','width'])

    for file_index in tqdm(range(len(df_catalog)-2)): #df_catalog.index.values)):
        #Load sequential files                
        ms_data = om_load_data.load_sequential_border(files2load=[df_catalog.file_name[file_index],df_catalog.file_name[file_index+1]],sec_file2=3,bandpass_freqs=[10,150],folder=project_files.project_info_ES_qc.ms_file_path)
        
        #%% Signal anomaly detection (QC)
        # The catalog of gph info is imported here because it will be used and edited for every chunck f data processed
        catalog_gph=pandas.read_csv('project_files/catalog_gph_3c.csv')
        catalog_gph['valid_z']  = True
        catalog_gph['valid_h1'] = True
        catalog_gph['valid_h2'] = True
        catalog_gph['report']   = None
        
        energy_stack=ms_data[0].copy()
        gph_energy,energy_stack.data=PED_ES_qc_data_analysis.data_analysis(ms_data,catalog_gph)
                
        #%%                
        mph=1.5*energy_stack.data.mean()#+project_files.project_info_ES.peak_threshold_std*es_mavg.std()
        mpd=int(project_files.project_info_ES_qc.peak_distance/ms_data[0].stats.delta)
        
        peaks_positions=om_ES.detect_peaks(x=energy_stack.data,mph=mph,mpd=mpd, show=project_files.project_info_ES_qc.show_plot)
        
        # Processing the case of at least one identified peak
        # In this case it is assumed just a single peak due the signal time-window. Intervals with more than one event
        # Will present a anomalous width (or future ATP) that will be identified and splited from the regular processing.
        # These cases will be processed using more complex softwares.
        if len(peaks_positions)!=0: 
            
            for peak_index in range(len(peaks_positions)):
                valid_event,snr,peak_time,width = om_ES.peak_properties_v2(energy_stack.data,peaks_position = peaks_positions[peak_index],
                        start_time=ms_data[0].stats.starttime,delta_time=ms_data[0].stats.delta,
                        SNR_threshold=mph,width_min=project_files.project_info_ES_qc.width_min,width_max=project_files.project_info_ES_qc.width_max)

                if valid_event==True:
                    event_catalog=event_catalog.append({'file_name':df_catalog.file_name[file_index],'peak_time':peak_time,'snr':snr,'width':width},ignore_index=True) 
            
    
        if (file_index % 10 == 0) or  (file_index == len(df_catalog)-1):
            event_catalog.to_csv(output_file_name,sep=',',line_terminator='\n',index=False)
    
    print('DONE with Core '+str(core_index))

    #%%     
    #if project_files.project_info_ES.os_used=='mac':
    #    os.system('say "Core done"')
    return()