# -*- coding: utf-8 -*-
"""
Created on Wed Oct 28 12:43:07 2020

@author: weedingb
"""

import os
from netCDF4 import Dataset
import numpy as np
import pandas as pd
import time

# set wdir to netcdf directory
os.chdir('C:/Users/weedingb/Desktop/barra dir test')

# list of Barra variables to import
target_vars = ['temp_scrn','rh2m','uwnd10m','vwnd10m']
    
# create dataframe to fill with target variable data
total_df = pd.DataFrame(columns=['Year','DOY','Hour'])

# set index of dataframe to enable merging
total_df = total_df.set_index(['Year','DOY','Hour'])

# optional timer start
#t0=time.time()

# loop through all files in directory
for root, dirs, files in os.walk(r'C:/Users/weedingb/Desktop/Barra dir test'):
    
    # for each file
    for fname in files:
    
        # optional print filename
        #print(os.path.join(root,fname))
        
        # extract file location
        file_loc = os.path.join(root,fname)
        
        # create dataframe from file using function defined below
        ncx = barra_nc_to_df(file_loc.replace(os.sep, '/'))
         
        # merge new dataframe with total_df - will contain additional overlapping columns and NaNs
        total_df = total_df.merge(ncx,left_index=True, right_index=True,how='outer')
        

# for each of the Barra variables
for current_var in target_vars:
    
    # fill the target variable named columns with the maximum values from each overlapping column to obtain the correct data at each timestamp
    total_df[current_var] = total_df[total_df.filter(like=current_var).columns].max(axis=1)

# remove the overlapping columns        
total_df = total_df[target_vars]

# calculate total windspeed
total_df['wspd10m'] = np.sqrt(np.square(total_df['uwnd10m']) + np.square(total_df['vwnd10m']))

# remove the multindex from total_df to allow for easy extraction of timings to export file
total_df = total_df.reset_index(level=['Year','DOY','Hour'])

# create a dataframe with the headings specified @ https://umep-docs.readthedocs.io/en/latest/pre-processor/Meteorological%20Data%20MetPreprocessor.html
met_df = pd.DataFrame(columns=['iy','id','it','imin','qn','qh','qe','qs','qf','U','RH','Tair','pres','rain','kdown','snow','ldown','fcld','wuh','xsmd,','lai','kdiff','kdir','wdir'])

# fill met_df with the appropriate data from total_df
met_df[['iy','id','it','Tair','RH','U']] = total_df[['Year','DOY','Hour','temp_scrn','rh2m','wspd10m']]

# set minutes to zero as we are using on the hour data
met_df['imin'] = np.zeros(met_df['imin'].shape)

# fill all Nans with -999.00 in accordance with https://umep-docs.readthedocs.io/en/latest/pre-processor/Meteorological%20Data%20MetPreprocessor.html
met_df = met_df.fillna(-999.00)

# optional timer end
#t1=time.time()

# optional print timing
#print(t1-t0)

# export met_df to spaced separated text file for use in UMEP
met_df.to_csv('metfile.txt',index=False,sep=' ')


# =============================================================================
# Extracts the date/time information and main variable from a Barra netcdf. 
# Default lat/lon are for Franklin Square in Hobart.
# =============================================================================

def barra_nc_to_df(nc_file_loc, target_lat = -42.882808, target_lon = 147.330266):
    
    # opens the netcdf specified by the file location
    nc = Dataset(nc_file_loc,mode='r')

    # sets the string that signifies the end of the main variable in the filename format
    splitter = '-fc'
    
    # extracts the main variable name for the file from the filename
    nc_main_varname = nc_file_loc.rpartition(splitter)[0]
    nc_main_varname = nc_main_varname.rpartition('/')[-1]
   
 
    # find indices of closest lat and lon in netcdf
    lat_idx = (np.abs(np.array(nc.variables['latitude'][:])-target_lat)).argmin()
    lon_idx = (np.abs(np.array(nc.variables['longitude'][:])-target_lon)).argmin()
    
    # extracts main variable from netcdf at closest lat/lon for all timestamps
    nc_main = np.array(nc.variables[nc_main_varname][:,lat_idx,lon_idx])
    
    # extracts time data (in hours since 01/01/1970 00:00:00)
    nc_time = np.array(nc.variables['time'][:])
    
    # creates a list of the zip of year, day of year (DOY), hour, and main variable from the netcdf
    nc_data_ext = list(zip(pd.to_datetime(nc_time,unit='h').year,pd.to_datetime(nc_time,unit='h').dayofyear,pd.to_datetime(nc_time,unit='h').hour,nc_main))
    
    # creates a dataframe from the above list
    nc_df = pd.DataFrame(nc_data_ext,columns=['Year','DOY','Hour',nc_main_varname])
    
    nc_df = nc_df.set_index(['Year','DOY','Hour'])

    # closes current netcdf
    nc.close()    

    # returns the created dataframe
    return nc_df

# =============================================================================
# 
# =============================================================================








# nc = Dataset('temp_scrn-fc-spec-PT1H-utas-v1.2-20150101T0000Z.nc',mode='r')

# # Use ~ Franklin square lat lon: -42.882808      147.330266 
# target_lat = -42.882808
# target_lon = 147.330266 

# # find index 
# nc_lat = np.array(nc.variables['latitude'][:])
# nc_lon = np.array(nc.variables['longitude'][:])

# target_lat_idx = (np.abs(nc_lat-target_lat)).argmin()
# target_lon_idx = (np.abs(nc_lon-target_lon)).argmin()

# target_nc_temp_scrn = np.array(nc.variables['temp_scrn'][:,target_lat_idx,target_lon_idx])

# target_nc_time = np.array(nc.variables['time'][:])

# pd.to_datetime(target_nc_time,unit='h')

# target_nc_data = list(zip(pd.to_datetime(target_nc_time,unit='h').year,pd.to_datetime(target_nc_time,unit='h').dayofyear,pd.to_datetime(target_nc_time,unit='h').hour,target_nc_temp_scrn))

# target_nc_df = pd.DataFrame(target_nc_data,columns=['Year','DOY','Hour','Scrn T'])


# ['longitude',
#  'time',
#  'latitude',
#  'height',
#  'latitude_longitude',
#  'forecast_period',
#  'forecast_reference_time',
#  'temp_scrn']

# #units: hours since 1970-01-01 00:00:00

#met_df = pd.DataFrame(columns=['%iy','id','it','imin','Q*','QH','QE','Qs','Qf','Wind','RH','Td','press','rain','Kdn','snow','ldown','fcld','wuh','xsmd','lai_hr','Kdiff','Kdir','Wd'])














