# -*- coding: utf-8 -*-
"""
Created on Wed Oct 28 12:43:07 2020

@author: weedingb
"""

import os
from netCDF4 import Dataset
import numpy as np
from datetime import datetime, date
import pandas as pd

# set working directory to phd repository
os.chdir('C:\\Users\\weedingb\\Documents\\GitHub\\phd')

# set wdir to netcdf location
os.chdir('C:\\Users\\weedingb\\Desktop\\barra_temp_sample')

# =============================================================================
# Extracts the date/time information and main variable from a Barra netcdf. 
# Default lat/lon are for Franklin Square in Hobart.
# =============================================================================

def barra_nc_to_df(nc_filename, target_lat = -42.882808, target_lon = 147.330266):
    
    # opens the netcdf specified by the filename
    nc = Dataset(nc_filename,mode='r')

    # sets the string that signifies the end of the main variable in the filename format
    splitter = '-fc'
    
    # extracts the main variable name for the file from the filename
    nc_main_varname = nc_filename.rpartition(splitter)[0]
    
    # find indices of closest lat and lon in netcdf
    lat_idx = (np.abs(np.array(nc.variables['latitude'][:])-target_lat)).argmin()
    lon_idx = (np.abs(np.array(nc.variables['longitude'][:])-target_lon)).argmin()
    
    # extracts main variable from netcdf at closest lat/lon for all timestamps
    nc_main = np.array(nc.variables[nc_main_varname][:,target_lat_idx,target_lon_idx])
    
    # extracts time data (in hours since 01/01/1970 00:00:00)
    nc_time = np.array(nc.variables['time'][:])
    
    # creates a list of the zip of year, day of year (DOY), hour, and main variable from the netcdf
    nc_data_ext = list(zip(pd.to_datetime(nc_time,unit='h').year,pd.to_datetime(nc_time,unit='h').dayofyear,pd.to_datetime(nc_time,unit='h').hour,nc_main))
    
    # creates a dataframe from the above list
    nc_df = pd.DataFrame(nc_data_ext,columns=['Year','DOY','Hour',nc_main_varname])

    # returns the created dataframe
    return nc_df

# =============================================================================
# 
# =============================================================================








nc = Dataset('temp_scrn-fc-spec-PT1H-utas-v1.2-20150101T0000Z.nc',mode='r')

# Use ~ Franklin square lat lon: -42.882808      147.330266 
target_lat = -42.882808
target_lon = 147.330266 

# find index 
nc_lat = np.array(nc.variables['latitude'][:])
nc_lon = np.array(nc.variables['longitude'][:])

target_lat_idx = (np.abs(nc_lat-target_lat)).argmin()
target_lon_idx = (np.abs(nc_lon-target_lon)).argmin()

target_nc_temp_scrn = np.array(nc.variables['temp_scrn'][:,target_lat_idx,target_lon_idx])

target_nc_time = np.array(nc.variables['time'][:])

pd.to_datetime(target_nc_time,unit='h')

target_nc_data = list(zip(pd.to_datetime(target_nc_time,unit='h').year,pd.to_datetime(target_nc_time,unit='h').dayofyear,pd.to_datetime(target_nc_time,unit='h').hour,target_nc_temp_scrn))

target_nc_df = pd.DataFrame(target_nc_data,columns=['Year','DOY','Hour','Scrn T'])


['longitude',
 'time',
 'latitude',
 'height',
 'latitude_longitude',
 'forecast_period',
 'forecast_reference_time',
 'temp_scrn']

#units: hours since 1970-01-01 00:00:00

met_df = pd.DataFrame(columns=['%iy','id','it','imin','Q*','QH','QE','Qs','Qf','Wind','RH','Td','press','rain','Kdn','snow','ldown','fcld','wuh','xsmd','lai_hr','Kdiff','Kdir','Wd'])














