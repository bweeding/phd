# -*- coding: utf-8 -*-
"""
Created on Fri Jan 22 10:41:55 2021

@author: weedingb
"""

import os
from netCDF4 import Dataset
import numpy as np
import pandas as pd
import time
from plotnine import *
import matplotlib.pyplot as plt
import matplotlib.dates as mdates

#%% declare functions

def mrt_C(globe_temp_C,windspeed_ms,air_temp_C,globe_diameter_mm=150,globe_emissivity=0.95):
    """ Calculates mean radiant temperature from a black globe thermometer following Thorsson et al. 2007."""
    
    mean_convection_coefficient = (1.1E8 * windspeed_ms**0.6)
    
    mrt_C_output =  -273.15 + ((globe_temp_C+273.15)**4 +  mean_convection_coefficient/(globe_emissivity*globe_diameter_mm**0.4) * (globe_temp_C-air_temp_C))**0.25
    
    return mrt_C_output


#%% prepare data

os.chdir('C:/Campbellsci/PC200W')

# read in data from Campbell CR1000
data_0 = pd.read_csv('C:/Campbellsci/PC200W/CR1000_33158_METdata_trial_190121.dat',header=[1],skiprows=[2,3])

data_0.set_index('RECORD')

# calculate the globe temperature according to envirodata
data_0['globe_temp_C'] = -20 + 2*data_0['Pulse']

# insert the measured windspeeds from the fan
data_0.loc[data_0.index[31:48], ['WS_ms']] = 2.8

# add mean radiant temperature to the dataframe
data_0['mean_radiant_temp_C'] = mrt_C(data_0['globe_temp_C'],data_0['WS_ms'],data_0['AirTC'])

sub_data_0 = data_0.iloc[1:101,:].copy()

# convert strings to datetimes
sub_data_0['TIMESTAMP'] = pd.to_datetime(sub_data_0['TIMESTAMP'])


#%% plot data

fig,ax = plt.subplots()

#fig.autofmt_xdate()

ax.plot(sub_data_0['TIMESTAMP'],sub_data_0['globe_temp_C'],label="Globe")
ax.plot(sub_data_0['TIMESTAMP'],sub_data_0['AirTC'],label="Air")
ax.plot(sub_data_0['TIMESTAMP'],sub_data_0['mean_radiant_temp_C'],label="Radiant")
ax.set_ylabel('°C')
ax.fmt_xdata = mdates.DateFormatter('%H')

ax2=ax.twinx()
ax2.plot(sub_data_0['TIMESTAMP'],sub_data_0['WS_ms'],label="Windspeed",linestyle="dashed")
ax2.set_ylabel('m/s')
#ax2.fmt_xdata = mdates.DateFormatter('%M:%S')

fig.legend(bbox_to_anchor=(1,1), bbox_transform=ax.transAxes)


(ggplot(sub_data_0)         # defining what data to use
 + aes(x='class')    # defining what variable to use
 + geom_bar(size=20) # defining the type of plot to use
)



(ggplot(sub_data_0, aes(x='TIMESTAMP')) +       # Create ggplot2 plot
  geom_line(aes(y = 'globe_temp_C'), color = "globe_temp_C") +
  geom_line(aes(y ='AirTC'), color = "AirTC")# +
  #scale_colour_manual(values=c("globe_temp_c"="red","AirTC"="blue"),breaks = c("globe_temp_c","AirTC"))
)

(ggplot(sub_data_0,            # Create ggplot2 plot
  aes(x = ,
  y = value,
  color = variable)) +
  geom_line()
)








