#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Dec 12 15:35:50 2017

@author: atilapaes

This module contains tools for preparing the input files to be used in a OpenMicroseismic project
"""

#%% Load libs
import pandas, obspy, numpy


#%%
def create_file_catalog(ms_file_path,ms_file_format,catalog_name):
    ################################################################
    def list_ms_files(ms_file_path,ms_file_format):
        """
        This function list all MS files of certain extension into the speciefied folder
        """
        import os
        file_list=[]
        for file in os.listdir(ms_file_path):
            if file.endswith('.'+ms_file_format):
                file_list.append(file)
        return(file_list)
    ################################################################
    """
    This function outputs a CSV catalog of file names, start and endtime
    """

    # Create file and time catalog
    file_list=list_ms_files(ms_file_path,ms_file_format)       

    date_time_start_list=[]
    date_time_end_list=[]

    for file in file_list:
        ms_data=obspy.read(ms_file_path+file)
        date_time_start_list.append(ms_data[0].stats.starttime)
        date_time_end_list.append(ms_data[0].stats.endtime)

    # Create dataframe from file list
    file_catalog=pandas.DataFrame(file_list,columns=['file_name'])
    file_catalog['date_time_start']=date_time_start_list
    file_catalog['date_time_end']=date_time_end_list
    
    # Export catalog as CSV    
    file_catalog.to_csv('catalog_'+'catalog_name'+ '.csv',sep=',',line_terminator='\n', index=False)

#%% 
def load_file_catalog(catalog_name):
    """
    Load catalog of file names and date time. Convert date-time string to datetime64
    catalog_name - project's name (str)
    """
    csv_catalog_name='catalog_'+catalog_name+'.csv' #csv file name contaningn the catalog
    file_catalog=pandas.read_csv(csv_catalog_name)

    # Convert date_time columns to time
    file_catalog['date_time_start']=file_catalog['date_time_start'].astype('datetime64[ms]')
    file_catalog['date_time_end']=file_catalog['date_time_end'].astype('datetime64[ms]')    
    return(file_catalog)

#%% 
def time2file_name(time2search,file_catalog):
    """
    search file name into a pandas dataframe catalog
    """
    # Convert time to datetime format
    time2search=numpy.datetime64(time2search)
    
    # Consult filename
    spec_file=file_catalog[(file_catalog['date_time_start'] <= time2search) & (file_catalog['date_time_end'] >= time2search)].reset_index(drop=True)

    return(spec_file.file_name[0])

#%% 
def time_window2file_name(time2search,file_catalog):
    """
    Search file name(s) for a interval around time2search
    """
    import om_param 
    file_name1=time2file_name(time2search-om_param.load_sec_before,file_catalog)
    file_name2=time2file_name(time2search+om_param.load_sec_after,file_catalog)
    
    if file_name1==file_name2:
        file_list=[file_name1]
    else:
        file_list=[file_name1,file_name2]

    return(file_list)
    

##############################################################################
##############################################################################
##############################################################################

### Example how to use the functions
#create_file_catalog(ms_file_path,ms_file_format,catalog_name)

# Load catalog
#file_catalog=load_file_catalog(catalog_name)

# Consult file name
#file_name=search_time_into_catalog(time2search,file_catalog)