#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue May 29 12:36:04 2018

@author: atilapaes

This module plots the raw waveform of an MS event from XXXX dataset
It will be used on R.W. thesis proposal

"""

import obspy, numpy
import matplotlib.pyplot as plt

file_name='26972.16.10.31.23.32.00.dat' # Name of the file to be loaded

ms_data=obspy.read('project_files/'+file_name)
ms_data=ms_data.slice(ms_data[0].stats.starttime+28,ms_data[0].stats.starttime+34)
ms_data=ms_data.normalize()

time=numpy.arange(ms_data[0].stats.starttime.second, ms_data[0].stats.endtime.second+0.5*ms_data[0].stats.delta,ms_data[0].stats.delta)

#%%

plt.figure(1,figsize=(3.9,6.3))

plt.subplot(1,3,1)
plt.title('Z channel', fontweight='semibold', size='medium')
for gph_index in range(69):
    plt.plot(time,0.65*ms_data[gph_index].data+gph_index*numpy.ones(len(ms_data[0])),'r',lw=0.15)
  
plt.ylabel('Gph ID',fontweight='medium')
plt.ylim(-1,69)
plt.xlabel('Time (s)',fontweight='medium')
plt.xticks([28,30,32,34],size='x-small')


plt.subplot(1,3,2)
plt.title('H1 channel', fontweight='semibold', size='medium')
for gph_index in range(69):
    plt.plot(time,0.65*ms_data[gph_index+69].data+gph_index*numpy.ones(len(ms_data[0])),'b',lw=0.15)

plt.yticks([])
plt.ylim(-1,69)
plt.xlabel('Time (s)',fontweight='medium')
plt.xticks([28,30,32,34],size='x-small')


plt.subplot(1,3,3)
plt.title('H2 channel', fontweight='semibold', size='medium')
for gph_index in range(69):
    plt.plot(time,0.65*ms_data[gph_index+69*2].data+gph_index*numpy.ones(len(ms_data[0])),'g',lw=0.15)

plt.yticks([])
plt.ylim(-1,69)
plt.xlabel('Time (s)',fontweight='medium')
plt.xticks([28,30,32,34],size='x-small')

plt.tight_layout()
#plt.savefig('raw_waveform.eps',format='eps',dpi=300) # For high image qualify
plt.savefig('raw_waveform.jpg',format='jpg',dpi=100) # For low image qualify (demostration)
plt.show()
plt.close()