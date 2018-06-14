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

plt.figure(1,figsize=(16,9))

plt.subplot(1,3,1)
plt.title('Z channel', fontweight='semibold', size='medium')
for gph_index in range(69):
    plt.plot(time,0.65*ms_data[gph_index].data+gph_index*numpy.ones(len(ms_data[0])),'r',lw=0.4)
  
plt.ylabel('Gph ID',fontweight='medium')
plt.ylim(-1,69)
plt.xlabel('Time (s)',fontweight='medium')
plt.xticks([28,29,30,31,32,33,34],size='x-small')


plt.subplot(1,3,2)
plt.title('H1 channel', fontweight='semibold', size='medium')
for gph_index in range(69):
    plt.plot(time,0.65*ms_data[gph_index+69].data+gph_index*numpy.ones(len(ms_data[0])),'b',lw=0.4)

plt.yticks([])
plt.ylim(-1,69)
plt.xlabel('Time (s)',fontweight='medium')
plt.xticks([28,29,30,31,32,33,34],size='x-small')


plt.subplot(1,3,3)
plt.title('H2 channel', fontweight='semibold', size='medium')
for gph_index in range(69):
    plt.plot(time,0.65*ms_data[gph_index+69*2].data+gph_index*numpy.ones(len(ms_data[0])),'g',lw=0.4)

plt.yticks([])
plt.ylim(-1,69)
plt.xlabel('Time (s)',fontweight='medium')
plt.xticks([28,29,30,31,32,33,34],size='x-small')

plt.tight_layout()
#plt.savefig('raw_waveform.eps',format='eps',dpi=300) # For high image qualify
plt.savefig('raw_waveform.jpg',format='jpg',dpi=300) # For low image qualify (demostration)
plt.show()
plt.close()

#%%

plt.figure(2,figsize=(8,3))
plt.subplot(1,2,1)

for gph_index in range(69):
    plt.plot(0.65*ms_data[gph_index].data+gph_index*numpy.ones(len(ms_data[0])),time,'r',lw=0.4)
  
plt.xlabel('Z',fontweight='bold')
plt.xlim(-1,69)
plt.ylim(29,32)
plt.ylabel('Time (s)')#,fontweight='small')
plt.yticks([29,30,31,32],size='x-small')
plt.gca().invert_yaxis()
plt.xticks([])

plt.subplot(1,2,2)
for gph_index in range(69):
    plt.plot(0.65*ms_data[gph_index+69].data+gph_index*numpy.ones(len(ms_data[0])),time,'b',lw=0.4)

plt.yticks([])
plt.xlim(-1,69)
plt.ylim(29,32)
plt.xlabel('H1',fontweight='bold')
plt.yticks([29,30,31,32],size='x-small')
plt.yticks([])
plt.xticks([])
plt.gca().invert_yaxis()


plt.tight_layout()
plt.savefig('raw_waveform_v2.tiff',format='tiff',dpi=300)
plt.show()
plt.close()
#%%