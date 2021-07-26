# -*- coding: utf-8 -*-
"""
Created on Wed Nov 11 10:04:40 2020

@author: weedingb
"""

import os
from netCDF4 import Dataset
import numpy as np
import pandas as pd
import time
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import matplotlib
#from labellines import labelLine, labelLines

os.chdir('C:/Users/weedingb/Desktop/solweig sample output')

data_1 = pd.read_csv('C:\\Users\\weedingb\\Desktop\\COC_sol_jan\\POI_1.txt',sep='\s+')

data_2 = pd.read_csv('C:\\Users\\weedingb\\Desktop\\COC_sol_jan\\POI_2.txt',sep='\s+')

data_1['time_stamp'] = pd.to_datetime(data_1['yyyy'],format='%Y') + pd.to_timedelta(data_1['dectime']-1,unit='D')

#data_2['time_stamp'] = pd.to_datetime(data_2['yyyy'],format='%Y') + pd.to_timedelta(data_2['dectime']-1,unit='D')

fig, axs = plt.subplots(2, 1)

#pd.date_range(data_1['time_stamp'][1],data_1['time_stamp'][-1],10)

#plt.hlines(y=45, xmin=data_1['time_stamp'].iloc[0], xmax=data_1['time_stamp'].iloc[-1])
axs[0].plot(data_1['time_stamp'],data_1['Tmrt'],label='MRT',color='salmon')
axs[0].plot(data_1['time_stamp'],data_1['Ta'],label='Ta',color='red')
axs[0].set_ylabel('°C')
axs[0].grid(True)
#plt.legend(loc='lower right')
#set ticks every week
#axs[0].xaxis.set_major_locator(mdates.WeekdayLocator())
#set major ticks format
axs[0].xaxis.set_major_formatter(mdates.DateFormatter(''))
#axs[0].axhline(y=)#, xmin=data_1['time_stamp'].iloc[0], xmax=data_1['time_stamp'].iloc[-1])

axs[0].set_yticks(range(0,51,10))

#axs[0].legend()

fig.suptitle('Point 1 (shaded) Jan Week 1 2017')

axs[1].plot(data_1['time_stamp'],data_1['PET'],label='Physiologically equivalent temperature',color='violet')
axs[1].set_ylabel('Physiologically \n equivalent \n temperature °C')
axs[1].grid(True)
axs[1].set_ylim([0,50])
#plt.legend(loc='lower right')
#set ticks every week
#axs[1].xaxis.set_major_locator(mdates.WeekdayLocator())
#set major ticks format
axs[1].xaxis.set_major_formatter(mdates.DateFormatter('%d %b'))
axs[1].axhline(y=29,linestyle='--',linewidth=1)
axs[1].axhline(y=35,linestyle='--',linewidth=1)
axs[1].axhline(y=41,linestyle='--',linewidth=1)

axs[1].set_yticks(range(0,51,10))

axs[1].xaxis.set_major_formatter(mdates.DateFormatter(''))
axs[1].text(data_1['time_stamp'].iloc[-65],42,'extreme',fontsize=8)
axs[1].text(data_1['time_stamp'].iloc[-65],36,'strong',fontsize=8)
axs[1].text(data_1['time_stamp'].iloc[-65],30,'moderate',fontsize=8)
axs[1].text(data_1['time_stamp'].iloc[0],42,'heat stress levels',fontsize=8)


#labelLine(l1,0.6,label='extreme',ha='left',va='bottom',align = False)

#labelLine(l1,data_1['time_stamp'].iloc[0],label='extreme',fontsize=8,ha='left',va='bottom',align = False)
plt.show()
fig.savefig('Jan 2019.jpg',dpi=300,bbox_inches='tight')









# ax.plot(data_1['time_stamp'],data_1['Ta'],label='Air temp')
# ax.plot(data_1['time_stamp'],data_1['PET'],label='PET')
# ax.plot(data_0['time_stamp'],data_0['PET'],label='PET')

idx_choice = slice(0,100)

#ax.plot(data_0['time_stamp'][idx_choice],data_1['PET'][idx_choice]-data_0['PET'][idx_choice],label='PET')


