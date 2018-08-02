#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Dec 12 15:35:50 2017

@author: atilapaes

This module contains tools for deal with catalog of microseismic files

"""

#%% Load libs
import pandas, obspy, numpy
from tqdm import tqdm
from shutil import copyfile



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
    
#%%
def time2file_name_v2(input_time,sec_before,sec_after,catalog_time_n_files):
    """
    Created on May 31 01:20, Last update on May 31 01:25
    Used on project(s): GRP_repicking

    This module get a input_time and returns which file(s) contain(s) the 
    time window from [input_time - sec_before, input_time - sec_after]
    
    INPUTS:
    input_time: pandas.tslib.Timestamp or Obspy datetime
    sec_before: number of seconds before input time (int)
    sec_after: number of seconds after input time (int)
    catalog_time_n_files: contains 2 columns: file_name(str), date_time(MUST BE pandas datetime type)
    
    OUTPUT:
    files2load: list of 1 or 2 file names to load
    """
    
    # Step 1: Get catalog index for input_time.
    catalog_index=catalog_time_n_files[(catalog_time_n_files['date_time'] <= input_time) & ((catalog_time_n_files['date_time'] + 59) >= input_time) ].index[0]
    
    # STEP 2: Get file name of specified index and a secondary file (before or after) if necessary
    files2load=[catalog_time_n_files.file_name[catalog_index]]
    if input_time.second-sec_before < 0:
        files2load.append(catalog_time_n_files.file_name[catalog_index-1])
    elif input_time.second+sec_after > 60:
        files2load.append(catalog_time_n_files.file_name[catalog_index+1])
    
    return(files2load)


##############################################################################
##############################################################################
##############################################################################

### Example how to use the functions
#create_file_catalog(ms_file_path,ms_file_format,catalog_name)

# Load catalog
#file_catalog=load_file_catalog(catalog_name)

# Consult file name
#file_name=search_time_into_catalog(time2search,file_catalog)

#%%
def copy_files_from_catalog(catalog,src_folder,dst_folder):
    """
    Copy all files into the catalog.file_name from src_folder to dst_folder
    """
    from tqdm import tqdm
    from shutil import copyfile
    for file_index in tqdm(range(len(catalog))):
        src=src_folder + str(catalog.file_name[file_index])
        dst=dst_folder + str(catalog.file_name[file_index])
        copyfile(src, dst)
    print('Done!')
    return()

#%%
def slice_catalog_by_day(catalog,attach_previous_file):
    """
    Slice main catalog into days and export as new csv. Append last file from previous catalog
    to the beggining of the catalog for days != of the first one
    """
    # Calculate day of the year for each file name into the catalog
    
    catalog['date_time2']=pandas.to_datetime(catalog['date_time'])
    catalog['day']=catalog['date_time2'].apply(lambda x: x.dayofyear)

    days=list(set(catalog.day))

    for day_index in range(len(days)):
        catalog_sliced = catalog.copy()
        catalog_sliced = catalog_sliced[catalog_sliced.day==days[day_index]]
    
        if day_index !=0 and attach_previous_file == True:
            catalog_sliced_aux = catalog.copy()
            catalog_sliced_aux = catalog_sliced_aux[catalog_sliced_aux.day==days[day_index-1]]
            catalog_sliced_aux=catalog_sliced_aux.tail(1)
            catalog_sliced=pandas.concat([catalog_sliced_aux,catalog_sliced],ignore_index=True)
            
        catalog_sliced=catalog_sliced.drop('date_time2',axis=1)
        catalog_sliced.to_csv('catalog_d'+str(days[day_index])+'.csv',sep=',',line_terminator='\n', index=False)

    return()
#catalog=pandas.read_csv('catalog_time_n_files.csv')
#slice_catalog_by_day(catalog,attach_previous_file=True)