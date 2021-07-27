# -*- coding: utf-8 -*-
"""
Created on Tue Jul 27 11:03:29 2021

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

def mrt_extractor_xr(cur_dir):
    
    # initial time
    tick_mrt_extractor_xr = time.perf_counter()
    
    landcover_image = Image.open(r"C:\Users\weedingb\Desktop\COC_solweig_run\landcover_clipped.tif")

    #landcover_image = np.array(landcover_image)
    landcover_image = xr.DataArray(landcover_image, dims=("y", "x"), coords={"x": np.arange(-49,101),"y": np.arange(-49,101)})
    
    #landcover_image[landcover_image!=2]=1
    landcover_image = xr.where(landcover_image!=2, 1,landcover_image)
    
   #landcover_image[landcover_image==2]=np.nan
    landcover_image = xr.where(landcover_image==2, np.nan,landcover_image)
    
    landcover_image = landcover_image[50:100,50:100]
    
    #landcover_image.plot()
    
    #all_data = []

    count = 0
    
    file_count = len(glob.glob1(cur_dir,"Tmrt_2*"))
    
    for file in os.listdir(cur_dir):
        
        if file.startswith("Tmrt_2"):
            
            print("{}%".format(round(count/file_count*100,2)))
            
            cur_image = Image.open(cur_dir+'/'+file)
            
            current_data = cur_image*np.ones((150,150))
            
            current_data = current_data[50:100,50:100]
            
            #current_data = current_data*landcover_image
            
            
            current_data = np.expand_dims(current_data, axis=0)
            
    
            current_data = xr.DataArray(current_data, dims=("timestamp","y", "x"),coords={"timestamp":[file.split("Tmrt_",1)[1].split(".tif",1)[0]],"x": np.arange(1,51),"y": np.arange(1,51)})
            
            
            current_data = xr.where(current_data==-9999, np.nan,current_data)
            
            current_data = current_data*landcover_image
            

            if count == 0:
                
                all_data = current_data
                
            else:
            
                all_data = xr.concat([all_data,current_data],dim="timestamp")
            
            count += 1

    
    tock_mrt_extractor_xr = time.perf_counter()
    
    # calculates run time
    print(str(datetime.timedelta(seconds=tock_mrt_extractor_xr-tick_mrt_extractor_xr)))
        
    return all_data


#file.split("Tmrt_",1)[1].split(".tif",1)[0]

jan17 = mrt_extractor_xr(r"C:\Users\weedingb\Desktop\COC_sol_jan")
apr17 = mrt_extractor_xr(r"C:\Users\weedingb\Desktop\COC_sol_april") 