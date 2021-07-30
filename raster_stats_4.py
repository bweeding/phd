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
from pythermalcomfort.models import utci

#TODO: convert time strings to numpy datetime64
# https://stackoverflow.com/questions/47178086/convert-string-to-numpy-datetime64-dtype

# can use landcover map buildings=2 to eliminate building value

# raster multiply by landcover != 2

def mrt_extractor_3(current_dir):
    
    # initial time
    tick_mrt_extractor_xr = time.perf_counter()
    
    
    # met data
    run_info_name = glob.glob1(current_dir,'RuninfoSOLWEIG*.txt')
    
    with open(current_dir+'/'+run_info_name[0]) as run_info:
    
        run_info_lines = run_info.readlines()
    
    metfile_location = [x for x in run_info_lines if x.startswith("Meteorological file")][0].split("Meteorological file: ")[1].split("\n")[0]
        
    met_data = pd.read_csv(metfile_location,sep=' ')
        
    met_data['datetime'] = pd.to_datetime(met_data['iy'].map(str)+'_'+met_data['id'].map(str)+'_'+met_data['it'].map(str)+met_data['imin'].map(str),format='%Y_%j_%H%M')    
    
    RH_data =  xr.DataArray(met_data["RH"], dims=("timestamp"),coords={"timestamp":met_data["datetime"]})
    
    Tair_data =  xr.DataArray(met_data["Tair"], dims=("timestamp"),coords={"timestamp":met_data["datetime"]})
    
    Uwind_data =  xr.DataArray(met_data["U"], dims=("timestamp"),coords={"timestamp":met_data["datetime"]})
    
    
    # landcover data 
    landcover_image = Image.open(r"C:\Users\weedingb\Desktop\COC_solweig_run\landcover_clipped.tif")

    landcover_image = np.array(landcover_image)

    landcover_image[landcover_image!=2]=1

    landcover_image[landcover_image==2]=np.nan
 
    landcover_image = landcover_image[50:100,50:100]
    
    
    # mrt rasters
    count = 0
    
    valid_files = glob.glob1(current_dir,"Tmrt_[12]**.tif")
    
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
    
    #tmrt_data =  xr.DataArray(np.zeros((file_count,50,50)), dims=("timestamp","y", "x"),coords={"timestamp":[pd.to_datetime(i.split("Tmrt_",1)[1].split(".tif",1)[0][0:-1],format='%Y_%j_%H%M') for i in valid_files] ,"x": xcoords,"y": ycoords})
   
    tmrt_data =  xr.DataArray(np.zeros((file_count,50,50)), dims=("timestamp","y", "x"),coords={"timestamp":met_data["datetime"] ,"x": xcoords,"y": ycoords}) 
    
    for current_file,current_ts in zip(valid_files,tmrt_data.coords["timestamp"]):
            
        print("{}%".format(round(count/file_count*100,2)))
        
        current_image = Image.open(current_dir+'/'+current_file)
                
        current_data = np.array(current_image)
        
        current_data = current_data[50:100,50:100]
        
        current_data = current_data*landcover_image
        
        current_data[current_data==-9999] = np.nan
        
        tmrt_data.loc[dict(timestamp=current_ts)]=current_data
        
        count += 1

    tock_mrt_extractor_xr = time.perf_counter()
    
    # calculates run time
    print(str(datetime.timedelta(seconds=tock_mrt_extractor_xr-tick_mrt_extractor_xr)))
    
    all_data = xr.Dataset(dict(Tmrt=tmrt_data,RH=RH_data,Tair=Tair_data,Uwind=Uwind_data))

    
    pet_vec = np.vectorize(_PET)
    
    def pet_array(a,b,c,d,e,f,g,h,i,j):
            
        return xr.apply_ufunc(pet_vec,a,b,c,d,e,f,g,h,i,j)
    
    pet_data =  xr.DataArray(np.zeros((file_count,50,50)), dims=("timestamp","y", "x"),coords={"timestamp":met_data["datetime"] ,"x": xcoords,"y": ycoords}) 
    
    for i in range(0,50):
        
        for j in range(0,50):
            
            pet_data[:,i,j] = pet_array(all_data["Tair"].values[:],all_data["RH"].values[:],all_data["Tmrt"].values[:,i,j],all_data["Uwind"].values[:],90,30,1.78,100,3,1)
            
            
    
    
    print(utci(tdb = all_data["Tair"].values[1], tr=all_data["Tmrt"].values[1,1,1],v=all_data["Uwind"].values[1],rh=all_data["RH"].values[1]))
        
    return all_data


#file.split("Tmrt_",1)[1].split(".tif",1)[0]

#big = mrt_extractor_3(r"C:\\Users\\weedingb\\SOLWEIG_run_07-07-2021_0444\\SOLWEIG_output_07-07-2021_0444")
jan17 = mrt_extractor_3(r"C:\Users\weedingb\Desktop\COC_sol_jan")
# apr17 = mrt_extractor_3(r"C:\Users\weedingb\Desktop\COC_sol_april") 