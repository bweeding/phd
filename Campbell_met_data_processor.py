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
import matplotlib.cbook as cbook
from mizani.breaks import date_breaks
from mizani.formatters import date_format

#%% declare functions

def mrt_C(globe_temp_C,windspeed_ms,air_temp_C,globe_diameter_mm=150,globe_emissivity=0.95):
    """ Calculates mean radiant temperature from a black globe thermometer following Thorsson et al. 2007."""
    
    mean_convection_coefficient = (1.1E8 * windspeed_ms**0.6)
    
    mrt_C_output =  -273.15 + ((globe_temp_C+273.15)**4 +  mean_convection_coefficient/(globe_emissivity*globe_diameter_mm**0.4) * (globe_temp_C-air_temp_C))**0.25
    
    return mrt_C_output


#%% prepare data

os.chdir('C:/Campbellsci/PC200W')

# read in data from Campbell CR1000
#data_0 = pd.read_csv('C:/Campbellsci/PC200W/CR1000_33158_METdata_trial_190121.dat',header=[1],skiprows=[2,3])

data_0 = pd.read_csv('C:/Campbellsci/PC200W/CR1000_27599_METdata_trial_190121.dat',header=[1],skiprows=[2,3])

data_0.set_index('RECORD')

# calculate the globe temperature according to envirodata
data_0['globe_temp_C'] = -20 + 2*data_0['Pulse']

# insert the measured windspeeds from the fan
#data_0.loc[data_0.index[31:48], ['WS_ms']] = 2.8

# add mean radiant temperature to the dataframe
data_0['mean_radiant_temp_C'] = mrt_C(data_0['globe_temp_C'],data_0['WS_ms'],data_0['AirTC'])

sub_data_0 = data_0.iloc[1::,:].copy()

#sub_data_0 = data_0.copy()

# convert strings to datetimes
sub_data_0['TIMESTAMP'] = pd.to_datetime(sub_data_0['TIMESTAMP'])


#%% plot data in matplotlib

fig, axs = plt.subplots(2, 1, sharex=True, sharey=False)

#fig.autofmt_xdate()



axs[0].plot(sub_data_0['TIMESTAMP'],sub_data_0['globe_temp_C'],label="Globe",color="black")
axs[0].plot(sub_data_0['TIMESTAMP'],sub_data_0['AirTC'],label="Air",color="gold")
axs[0].plot(sub_data_0['TIMESTAMP'],sub_data_0['mean_radiant_temp_C'],label="Radiant",color="firebrick")
axs[0].set_ylabel('°C')
axs[0].set_ylim([10,50])
axs[0].yaxis.set_ticks(np.linspace(10,50,5))
axs[0].grid()

axs[0].set_xlim([sub_data_0['TIMESTAMP'][1],sub_data_0['TIMESTAMP'].iloc[-1]])

axs[1].plot(sub_data_0['TIMESTAMP'],sub_data_0['WS_ms'],label="Windspeed",color="seagreen")
axs[1].set_ylabel('m/s')
axs[1].grid()
axs[1].set_ylim([0,5])
axs[1].yaxis.set_ticks(np.linspace(0,5,6))

axs2=axs[1].twinx()
axs2.plot(sub_data_0['TIMESTAMP'],sub_data_0['RH'],label="Relative humidity",color="cornflowerblue")
axs2.set_ylabel('%')
axs2.set_ylim([0,100])

# ax2.plot(sub_data_0['TIMESTAMP'],sub_data_0['SlrW'],label="SW radiation D",linestyle="dashed")
# ax2.set_ylabel('W/m^2')


axs[1].xaxis.set_major_formatter(mdates.DateFormatter('%H:%M')) 

#axs[0].legend(bbox_to_anchor=(1,1), bbox_transform=ax.transAxes)

axs[0].legend(loc='upper center', bbox_to_anchor=(0.5, 1.3),ncol=3)

axs[1].legend(loc='upper center', bbox_to_anchor=(0.25, -0.2),ncol=1)

axs2.legend(loc='upper center', bbox_to_anchor=(0.65, -0.2),ncol=1)

arrow_size = 7

fig.text(0.155, 0.5, "Wed " , ha="center", va="center", rotation=0, size=arrow_size,
    bbox=dict(boxstyle="darrow,pad=0.3", fc="w", ec="black"))


fig.text(0.27, 0.5, "        Thur        ", ha="center", va="center", rotation=0, size=arrow_size,
    bbox=dict(boxstyle="darrow,pad=0.3", fc="w", ec="black"))

fig.text(0.43, 0.5, "          Fri          ", ha="center", va="center", rotation=0, size=arrow_size,
    bbox=dict(boxstyle="darrow,pad=0.3", fc="w", ec="black"))


fig.text(0.59, 0.5, "          Sat        ", ha="center", va="center", rotation=0, size=arrow_size,
    bbox=dict(boxstyle="darrow,pad=0.3", fc="w", ec="black"))


fig.text(0.745, 0.5, "         Sun        ", ha="center", va="center", rotation=0, size=arrow_size,
    bbox=dict(boxstyle="darrow,pad=0.3", fc="w", ec="black"))

fig.text(0.865, 0.5, " Mon ", ha="center", va="center", rotation=0, size=arrow_size,
    bbox=dict(boxstyle="darrow,pad=0.3", fc="w", ec="black"))

fig.text(0.15, 0.94, "Starting 17/02", ha="center", va="center", rotation=0, size=10,
    bbox=dict(boxstyle="round4,pad=0.3", fc="w", ec="black"))


#%%
import plotly.graph_objects as go
from plotly.subplots import make_subplots

time_idx = sub_data_0['TIMESTAMP']

# Create figure with secondary y-axis
fig = make_subplots(specs=[[{"secondary_y": True}]])

# Add traces
fig.add_trace(
    go.Scatter(x=time_idx, y=sub_data_0['globe_temp_C'], name="yaxis data"),
    secondary_y=False,
)

fig.add_trace(
    go.Scatter(x=time_idx, y=sub_data_0['WS_ms'], name="yaxis2 data"),
    secondary_y=True,
)

# Add figure title
fig.update_layout(
    title_text="Double Y Axis Example"
)

# Set x-axis title
fig.update_xaxes(title_text="xaxis title")

# Set y-axes titles
fig.update_yaxes(title_text="<b>primary</b> yaxis title", secondary_y=False)
fig.update_yaxes(title_text="<b>secondary</b> yaxis title", secondary_y=True)

fig.show()

#%% plot data in plotnine/ggplot

# (ggplot(sub_data_0)         # defining what data to use
#  + aes(x='class')    # defining what variable to use
#  + geom_bar(size=20) # defining the type of plot to use
# )

data_ext=sub_data_0[["TIMESTAMP","globe_temp_C","AirTC","mean_radiant_temp_C"]].copy()

data_ext = data_ext.set_index("TIMESTAMP").stack()

data_ext = pd.DataFrame(data_ext)

data_ext = data_ext.reset_index()

data_ext.rename(columns = {0:"values","level_1":"measurements"},inplace=True)

(ggplot(data_ext, aes(x = "TIMESTAMP", y = "values")) + 
  geom_line(aes(color = "measurements", linetype = "measurements")) +
  scale_x_datetime(breaks=date_breaks('15 minutes'), labels=date_format('%HH:%MM'))# + 
  #scale_color_manual(values = c("darkred", "steelblue"))
)  
  
  
  








