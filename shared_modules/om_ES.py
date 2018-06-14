#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Jun 14 04:30:48 2018

@author: atilapaes

Module for Energy-Stacking 
"""
#%%
import pandas, numpy

#%%
def cf_es_selec_gph(ms_data,catalog_gph_3c):
    """
    Module for energy stack
    Based on a list of selected geophones 
    """

    es=numpy.zeros(len(ms_data[0]))

    for gph_index in range(len(catalog_gph_3c)):
        # Adds energy though gph to the stack vection in case the gph status is valid
        if catalog_gph_3c.valid_gph[gph_index]==True:
            es=numpy.add(es,numpy.square(ms_data[catalog_gph_3c.ch_z[gph_index]].data))
            es=numpy.add(es,numpy.square(ms_data[catalog_gph_3c.ch_h1[gph_index]].data))
            es=numpy.add(es,numpy.square(ms_data[catalog_gph_3c.ch_h2[gph_index]].data))
    return(es)

#%%
