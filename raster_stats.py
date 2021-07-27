# -*- coding: utf-8 -*-
"""
Created on Mon Jul 26 12:15:12 2021

@author: weedingb
"""

from PIL import Image
import numpy as np
from scipy import ndimage
import matplotlib.pyplot as plt
import os
import glob
import xarray as xr
import pandas as pd
import time, datetime

# can use landcover map buildings=2 to eliminate building value

# raster multiply by landcover != 2

def mrt_extractor(cur_dir):
    
    tick_mrt_extractor = time.perf_counter()
    
    landcover_image = Image.open(r"C:\Users\weedingb\Desktop\COC_solweig_run\landcover_clipped.tif")

    landcover_image = np.array(landcover_image)
    
    landcover_image[landcover_image!=2]=1
    
    landcover_image[landcover_image==2]=np.nan
    
    landcover_image = landcover_image[50:100,50:100]
    
    all_data = []

    count = 1
    
    file_count = len(glob.glob1(cur_dir,"Tmrt_2*"))
    
    for file in os.listdir(cur_dir):
        
        if file.startswith("Tmrt_2"):
            
            print("{}%".format(round(count/file_count*100,2)))
            
            cur_image = Image.open(cur_dir+'/'+file)
    
            current_data = np.array(cur_image)
            
            current_data = current_data[50:100,50:100]
    
            current_data[current_data==-9999] = np.nan
            
            current_data = current_data*landcover_image
            
            current_data = current_data.ravel()
            
            current_data = current_data.tolist()
            
            all_data.extend(current_data[:])
            
            count += 1
        
    all_data = np.array(all_data)
    
    tock_mrt_extractor = time.perf_counter()
    
    # calculates run time
    print(str(datetime.timedelta(seconds=tock_mrt_extractor-tick_mrt_extractor)))
        
    return all_data
        

jan17 = mrt_extractor(r"C:\Users\weedingb\Desktop\COC_sol_jan")
apr17 = mrt_extractor(r"C:\Users\weedingb\Desktop\COC_sol_april")        


# bins = np.linspace(-5,65,141)

# plt.hist(jan17, bins, alpha=0.5, label='Jan 17', density=True)

# plt.hist(apr17, bins, alpha=0.5, label='Apr 17', density=True)

# plt.legend(loc='upper right')

# axs[0].yaxis.set_major_formatter(PercentFormatter(xmax=1))

# plt.show()


bins = np.linspace(-5,65,141)


fig, ax = plt.subplots()

# the histogram of the data
ax.hist(jan17, bins, alpha=0.5, label='Jan 17', density=True)

ax.hist(apr17, bins, alpha=0.5, label='Apr 17', density=True)
    
ax.set_xlabel('Mean radiant temperature  °C')
ax.set_ylabel('Probability density')

ax.legend(loc="upper right")
#ax.set_title(r'Histogram of IQ: $\mu=100$, $\sigma=15$')

# Tweak spacing to prevent clipping of ylabel
fig.tight_layout()
plt.show()


# all_data = []

# count = 1

# file_count = len(glob.glob1("C:\\Users\\weedingb\\SOLWEIG_run_07-07-2021_0444\\SOLWEIG_output_07-07-2021_0444","Tmrt_2*"))

# for file in os.listdir("C:\\Users\\weedingb\\SOLWEIG_run_07-07-2021_0444\\SOLWEIG_output_07-07-2021_0444"):
#     if file.startswith("Tmrt_2"):
#         #print(file)
#         print("{}%".format(round(count/file_count*100,2)))
        
#         cur_image = Image.open("C:\\Users\\weedingb\\SOLWEIG_run_07-07-2021_0444\\SOLWEIG_output_07-07-2021_0444\\"+file)

#         current_data = np.array(cur_image)

#         current_data[current_data==-9999] = np.nan
        
#         current_data = current_data.ravel()
        
#         current_data = current_data.tolist()
        
#         all_data.extend(current_data[:])
        
#         count += 1
        
# all_data = np.array(all_data)

# plt.hist(all_data,100)        
        