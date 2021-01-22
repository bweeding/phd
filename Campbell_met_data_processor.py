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


os.chdir('C:/Campbellsci/PC200W')

data_0 = pd.read_csv('C:/Campbellsci/PC200W/CR1000_33158_METdata_trial_190121.dat',header=[1],skiprows=[2,3])

data_0.set_index('RECORD')

data_0['globe_temp_C'] = -20 + 2*data_0['Pulse']

data_0.loc[data_0.index[31:48], ['WS_ms']] = 2.8

data_0['mean_radiant_temp_C'] = -273.15 + ((data_0['globe_temp_C']+273.15)**4 + (1.1E8 * data_0['WS_ms']**0.6)/(0.95*150**0.4) * (data_0['globe_temp_C']-data_0['AirTC']))**0.25

sub_data_0 = data_0.iloc[0:101]

(ggplot(mpg)         # defining what data to use
 + aes(x='class')    # defining what variable to use
 + geom_bar(size=20) # defining the type of plot to use
)



(ggplot(sub_data_0, aes('TIMESTAMP')) +       # Create ggplot2 plot
  geom_line(aes(y = 'globe_temp_C'), color = "red") +
  geom_line(aes(y ='AirTC'), color = "blue"))