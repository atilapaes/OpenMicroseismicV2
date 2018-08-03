#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Jul 15 05:00:33 2018
Last Update: Fri Jul 20 23:30

@author: atilapaes

Potential Event Detection (PED) using Energy Stack (ES) - Version Early Aug 2018.

Main file: The main file to be executed. It imports the CSV catalog of files, slice it and send to 
            an especified number of  cores. 

Modules used:
PED_ES_workflow:            The Potential Event Detection workflow. Importing data, processing and exporting
PED_ES_qc_data_analysis:    The workflow for MS data analisys used by processing and plotter
PED_plotter:                An auxiliar module used to plot the Potential events identified by the software
om_sinal_anomaly:           Methods for identify signal anomalies (zero channels, loud or noisy geophones etc) 
                            and flag them to prevent future use at the processing stage

project_files/project_info_ES: the file with processing variables

"""

#%% Lib importing
import pandas, numpy,multiprocessing
import project_files.project_info_ES_qc

# Shared modules path
import sys
sys.path.insert(0,project_files.project_info_ES_qc.shared_modules_path)

# Shared modules import
import PED_ES_qc_workflow

log_file='log.csv'
#%% Input Catalog and pre-process it
catalog_files=pandas.read_csv(project_files.project_info_ES_qc.catalog_ms_files) 

# Attach the last element of previous list to the current list.
catalog_files_sliced=numpy.array_split(catalog_files,project_files.project_info_ES_qc.n_cores)
if project_files.project_info_ES_qc.n_cores != 1:
    for core_index in range(1,(project_files.project_info_ES_qc.n_cores)):
        catalog_files_sliced[core_index]=pandas.concat([catalog_files_sliced[core_index-1][-1:],catalog_files_sliced[core_index]], ignore_index=True)
# slice catalog must have index from zero
        
#%% Split the work among several processors
### MULTICORE PROCESSING

if __name__ == '__main__':
    jobs = []
    for core_index in range(project_files.project_info_ES_qc.n_cores):
    
        #Defingn inputs and outputs of the task to the cores
        p = multiprocessing.Process(target=PED_ES_qc_workflow.PED_from_filelist, args=(catalog_files_sliced[core_index],core_index,log_file))
        jobs.append(p)
        p.start()   

############################################################################### 