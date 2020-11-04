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

#os.chdir('/rdsi/barra/private/BARRA_TA/v1/utas/v1.2/hourly')

# optional timer start
#t0=time.time()



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
    nc_data_ext = list(zip(pd.to_datetime(nc_time,unit='h').year,pd.to_datetime(nc_time,unit='h').dayofyear,pd.to_datetime(nc_time,unit='h').hour,pd.to_datetime(nc_time,unit='h').minute,nc_main))
    
    # creates a dataframe from the above list
    nc_df = pd.DataFrame(nc_data_ext,columns=['Year','DOY','Hour','Min',nc_main_varname])
    
    nc_df = nc_df.set_index(['Year','DOY','Hour','Min'])

    # closes current netcdf
    nc.close()    

    # returns the created dataframe
    return nc_df

# =============================================================================
# 
# =============================================================================

def barra_to_UMEP_met(start_date,end_date):

    # list of Barra variables to import
    target_vars = ['temp_scrn','rh2m','uwnd10m','vwnd10m','av_sfc_sw_dif','av_sfc_sw_dir','av_swsfcdown','av_lwsfcdown']

    # list of instantaneous variables
    inst_vars = ['temp_scrn','rh2m','uwnd10m','vwnd10m']

    # list of forecast variables that must be obtained from a separate file path
    forecast_vars = ['av_sfc_sw_dif','av_sfc_sw_dir','av_swsfcdown','av_lwsfcdown']

    var_types = [inst_vars, forecast_vars]

    directories = ['/rdsi/barra/private/BARRA_TA/v1/utas/v1.2/hourly','/rdsi/barra/private/BARRA_TA/v1/forecast/slv']

    date_slices = [slice(-17,-9),slice(-21,-13)]

    # create dataframe to fill with target variable data
    total_df = pd.DataFrame(columns=['Year','DOY','Hour','Min'])

    # set index of dataframe to enable merging
    total_df = total_df.set_index(['Year','DOY','Hour','Min'])

    for current_var_type, current_direc, current_slice in zip(var_types,directories,date_slices):

        for var_folder in current_var_type:

            for root, dirs, files in os.walk(current_direc+'/'+var_folder):

                # for each file
                for fname in files:

                    if any(var in fname for var in current_var_type):

                        if pd.to_datetime(start_date) <= pd.to_datetime(fname[current_slice]) <= pd.to_datetime(end_date):

                            # optional print filename
                            print(os.path.join(root,fname))

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

    # remove unwanted wind data
    total_df.drop(['uwnd10m','vwnd10m'], inplace=True, axis=1)

    # convert temperature from Kelvin to Celsius
    total_df['temp_scrn'] -= 273.15

    # remove the multindex from total_df to allow for easy extraction of timings to export file
    total_df = total_df.reset_index(level=['Year','DOY','Hour','Min'])

    # list of variables to be interpolated as they are measured instantaneously on the hour
    vars_to_interp = inst_vars = ['temp_scrn','rh2m','wspd10m']

    # linearly interpolate instantaneous variables
    total_df[vars_to_interp] = total_df[vars_to_interp].interpolate()

    # take only measurements on the half hour (averaged measurements and interpolated values)
    total_df = total_df[total_df['Min']==30]

    # remove remaining rows containing Nan (should only be the first row where interpolation can't take place)
    total_df = total_df.dropna()

    # round data to two decimal places in line with files supplied by UMEP
    total_df[total_df.columns.difference(['Year','DOY','Hour','Min'])] = total_df[total_df.columns.difference(['Year','DOY','Hour','Min'])].round(2)

    # create a dataframe with the headings specified @ https://umep-docs.readthedocs.io/en/latest/pre-processor/Meteorological%20Data%20MetPreprocessor.html
    met_df = pd.DataFrame(columns=['iy','id','it','imin','qn','qh','qe','qs','qf','U','RH','Tair','pres','rain','kdown','snow','ldown','fcld','wuh','xsmd','lai','kdiff','kdir','wdir'])

    # fill met_df with the appropriate data from total_df
    met_df[['iy','id','it','imin','Tair','RH','U','kdiff','kdir','kdown','ldown']] = total_df[['Year','DOY','Hour','Min','temp_scrn','rh2m','wspd10m','av_sfc_sw_dif','av_sfc_sw_dir','av_swsfcdown','av_lwsfcdown']]


    # fill all Nans with -999.00 in accordance with https://umep-docs.readthedocs.io/en/latest/pre-processor/Meteorological%20Data%20MetPreprocessor.html
    met_df = met_df.fillna(-999.00)

    # sets output path for use on Jupyter
    csv_path = '/mnt/bweeding_workspace/output'

    csv_output = os.path.join(csv_path,'metfile_'+start_date+'_'+end_date+'.txt')

    # export met_df to spaced separated text file for use in UMEP, named with start and end dates
    met_df.to_csv(csv_output,index=False,sep=' ')


