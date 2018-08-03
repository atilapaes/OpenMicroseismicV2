#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Aug  2 21:10:04 2018

@author: atilapaes

An auxiliar module used to load MS data and plot the energy stack curve and the energy over the gphs
"""

#%%
import pandas, obspy
import matplotlib.pyplot as plt
import project_files.project_info_ES_qc

# Shared modules path
import sys
sys.path.insert(0,project_files.project_info_ES_qc.shared_modules_path)

# Shared modules import
import PED_ES_qc_data_analysis

#%% Catalog of file names & parameters to load
catalog=pandas.read_csv('project_files/results/d305-Core0.csv')
index=35 # index of the Potential Event to load into the imported catalog of PE

#%% Data loading and filtering

ms_file_path= project_files.project_info_ES_qc.ms_file_path
ms_file_name=catalog.file_name[index]
ms_data=obspy.read(ms_file_path + ms_file_name)
ms_data=ms_data.filter('bandpass', freqmin=10, freqmax=150, corners=4, zerophase=True)

#%% Preparing the catalog of gph
catalog_gph=pandas.read_csv('project_files/catalog_gph_3c.csv')
catalog_gph['valid_z']  = True
catalog_gph['valid_h1'] = True
catalog_gph['valid_h2'] = True
catalog_gph['report']   = None

#%% Processing the data using the standart workflow
energy_stack=ms_data[0].copy()
gph_energy,energy_stack.data=PED_ES_qc_data_analysis.data_analysis(ms_data,catalog_gph)

#%% Two plots: the Stack of energy and the energy though each gph
plt.figure(index)
energy_stack.plot()
plt.show();plt.close()

plt.figure(index+1)
gph_energy.plot(size=(800,2000),automerge=False)
plt.show();plt.close()