# -*- coding: utf-8 -*-
"""
Created on Wed Jul 28 12:23:41 2021

@author: weedingb
"""


import PIL
from PIL import Image
import numpy as np
from scipy import ndimage
import matplotlib.pyplot as plt
import os
import glob
import xarray as xr
import pandas as pd
import time, datetime

#TODO: convert time strings to numpy datetime64
# https://stackoverflow.com/questions/47178086/convert-string-to-numpy-datetime64-dtype

# can use landcover map buildings=2 to eliminate building value

# raster multiply by landcover != 2

def mrt_extractor_3(current_dir):
    
    # initial time
    tick_mrt_extractor_xr = time.perf_counter()
    
    landcover_image = Image.open(r"C:\Users\weedingb\Desktop\COC_solweig_run\landcover_clipped.tif")

    landcover_image = np.array(landcover_image)

    landcover_image[landcover_image!=2]=1

    landcover_image[landcover_image==2]=np.nan
 
    landcover_image = landcover_image[50:100,50:100]
    
    count = 0
    
    valid_files = glob.glob1(current_dir,"Tmrt_2*")
    
    file_count = len(valid_files)
    
    first_image = Image.open(current_dir+'/'+valid_files[0])

    # for info use PIL.TiffTags.lookup(33922)
    # geotiffs are referenced to the top left of the image
    xdim_start = first_image.tag[33922][3]
    
    ydim_start = first_image.tag[33922][4]
    
    xpixel_size = first_image.tag[33550][0]
    
    ypixel_size = first_image.tag[33550][1]
    
    xcoords = np.linspace(xdim_start+50*xpixel_size,xdim_start+99*xpixel_size,50)
    
    ycoords = np.linspace(ydim_start-50*ypixel_size,ydim_start-99*ypixel_size,50)
            
    
    all_data =  xr.DataArray(np.zeros((file_count,50,50)), dims=("timestamp","y", "x"),coords={"timestamp":[i.split("Tmrt_",1)[1].split(".tif",1)[0] for i in valid_files],"x": xcoords,"y": ycoords})
    
    for current_file,current_ts in zip(valid_files,all_data.coords["timestamp"]):
            
        print("{}%".format(round(count/file_count*100,2)))
        
        current_image = Image.open(current_dir+'/'+current_file)
                
        current_data = np.array(current_image)
        
        current_data = current_data[50:100,50:100]
        
        current_data = current_data*landcover_image
        
        current_data[current_data==-9999] = np.nan
        
        all_data.loc[dict(timestamp=current_ts)]=current_data
        
        count += 1

    tock_mrt_extractor_xr = time.perf_counter()
    
    # calculates run time
    print(str(datetime.timedelta(seconds=tock_mrt_extractor_xr-tick_mrt_extractor_xr)))
        
    return all_data


#file.split("Tmrt_",1)[1].split(".tif",1)[0]

#big = mrt_extractor_3(r"C:\\Users\\weedingb\\SOLWEIG_run_07-07-2021_0444\\SOLWEIG_output_07-07-2021_0444")
jan17 = mrt_extractor_3(r"C:\Users\weedingb\Desktop\COC_sol_jan")
# apr17 = mrt_extractor_3(r"C:\Users\weedingb\Desktop\COC_sol_april") 