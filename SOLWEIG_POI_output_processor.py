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
import matplotlib

os.chdir('C:/Users/weedingb/Desktop/solweig sample output')

data_1 = pd.read_csv('C:/Users/weedingb/Desktop/solweig sample output/POI_0.txt',sep='\s+')

pd.to_datetime(data_1['yyyy'],format='%Y') + pd.to_timedelta(data_1['dectime']-1,unit='D')

fig, ax = plot.subplots()

ax.plot(data_1)