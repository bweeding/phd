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

    # closes current netcdf
    nc.close()    

    # returns the created dataframe
    return nc_df

# =============================================================================
# 
# =============================================================================
def barra_to_UMEP_met(start_date,end_date):

    # manual date setting for experimentation when not running as a function
#     start_date = '20190201'
#     end_date = '20190203'

    # converting dates to UTC datetime objects
    start_datetime = pd.to_datetime(start_date).tz_localize('UTC')
    end_datetime = pd.to_datetime(end_date).tz_localize('UTC')

    # extracting year as a string from starting dates - could be changed to take from datetime objects?
    start_year = start_date[0:4]
    end_year = end_date[0:4]

    # generates a list of the years from which data will be taken
    years = [str(i) for i in range(int(start_year),int(end_year)+1)]
    
    #years.append(end_year)

    # generates list of all years of data available from Barra
    all_years = [str(i) for i in range(1990,2020)]

    # generates a numerical list of months in the form 01,02,03...10,11,12
    all_months = [str(i).zfill(2) for i in range(1,13)]

    # creates strings naming the corresponding folders for the start and end dates
    start_folder = '/'+start_date[0:4]+'/'+start_date[4:6]
    end_folder = '/'+end_date[0:4]+'/'+end_date[4:6]


    # creates a list of all the folders available
    master_list = []

    for y in all_years:

        for m in all_months:

            master_list.append('/'+y+'/'+m)

    # finds the indices of the start and end folders
    start_idx = master_list.index(start_folder)
    end_idx = master_list.index(end_folder)

    # starts a timer
    t0 = time.time()

    # list of Barra variables to import
    target_vars = ['temp_scrn','rh2m','uwnd10m','vwnd10m','av_sfc_sw_dif','av_sfc_sw_dir','av_swsfcdown','av_lwsfcdown']

    # list of instantaneous variables
    inst_vars = ['temp_scrn','rh2m','uwnd10m','vwnd10m']

    # list of forecast variables that must be obtained from a separate file path
    forecast_vars = ['av_sfc_sw_dif','av_sfc_sw_dir','av_swsfcdown','av_lwsfcdown']

    # list of variable types
    var_types = [inst_vars, forecast_vars]

    # list of directories corresponding to variable types
    directories = ['/rdsi/barra/private/BARRA_TA/v1/utas/v1.2/hourly','/rdsi/barra/private/BARRA_TA/v1/forecast/slv']

    # data slices from filenames containing full date and times ie. 20190101T0000Z
    date_slices = [slice(-17,-3),slice(-21,-7)]

    # create dataframe to fill with target variable data, indexed on a date range, adjusted for time offsets in the Barra files
    total_df = pd.DataFrame(index = pd.date_range(start = start_datetime - pd.Timedelta(hours = 3), end = end_datetime + pd.Timedelta(hours = 28), freq = '30min'),columns=['Year','DOY','Hour','Min','temp_scrn','rh2m','uwnd10m','vwnd10m','av_sfc_sw_dif','av_sfc_sw_dir','av_swsfcdown','av_lwsfcdown'])

    # fills the time variables in the dataframe
    total_df['Year'] = np.array(total_df.index.year)
    total_df['DOY'] = np.array(total_df.index.dayofyear)
    total_df['Hour'] = np.array(total_df.index.hour)
    total_df['Min'] = np.array(total_df.index.minute)
    
    # if the start date is the first day of a year, allow the code to look at data from the previous year to compensate 
    #for the time offsets in the Barra files
    if start_date[4:8] == '0101':

        start_year = str(int(start_year)-1)

    # generates a list of years to be excluded
    exclude_years = [x for x in all_years if x not in years]    
    

    # main loop
    
    # for each combination of variable type, matching directory, and matching slice of date location in filenames

    for current_var_type, current_direc, current_slice in zip(var_types,directories,date_slices):

        # for each variable named folder in the current variable type
        for var_folder in current_var_type:

            # for each combination of root, directory and file in the var_folder
            for root, dirs, files in os.walk(current_direc+'/'+var_folder):

                # remove any directories from excluded years
                [dirs.remove(d) for d in list(dirs) if d in exclude_years]

                # if any of the roots match those in the master list
                if any(r in root for r in  master_list[start_idx-1:end_idx+1]):

                    # for each file
                    for fname in files:
                        
                        # if the file contains the current variable name
                        if any(var in fname for var in current_var_type):

                            # if the file's date is in an acceptable period, adjusted for the time offsets in the barra files
                            if start_datetime - pd.Timedelta(hours = 8) <= pd.to_datetime(fname[current_slice]) <= end_datetime + pd.Timedelta(hours = 22):

                                # optional print filename
                                #print(os.path.join(root,fname))

                                # extract file location
                                file_loc = os.path.join(root,fname)

                                # create dataframe from file using function defined below
                                ncx = barra_nc_to_df(file_loc.replace(os.sep, '/'))

                                # find the index of the location where the time in the total_df matches the 1st time in the ncx
                                fill_idx = np.where((total_df['Year'] == ncx['Year'][0]) & (total_df['DOY'] == ncx['DOY'][0])& (total_df['Hour'] == ncx['Hour'][0])& (total_df['Min'] == ncx['Min'][0]))[0]

                                # fill the relevant variable in the total_df in every 2nd position (as measurements are on
                                # either hours or half hours depending on variable type) from the ncx
                                total_df.loc[total_df.index[fill_idx[0]:fill_idx[0]+12:2],ncx.columns[-1]] = np.array(ncx[ncx.columns[-1]])


    # convert temperature from Kelvin to Celsius
    total_df['temp_scrn'] -= 273.15

    # convert all the columns to numeric type to allow interpolation
    for col in total_df:
        total_df[col] = pd.to_numeric(total_df[col], errors='coerce')

    # list of variables to be interpolated as they are measured instantaneously on the hour
    vars_to_interp = ['temp_scrn','rh2m','uwnd10m','vwnd10m'] 

    # linearly interpolate instantaneous variables
    total_df[vars_to_interp] = total_df[vars_to_interp].interpolate()

    # take only measurements on the half hour (averaged measurements and interpolated values)
    total_df = total_df[total_df['Min']==30]

    # trim the start and end of total_df to the appropriate times
    total_df = total_df.loc[start_datetime:end_datetime+pd.Timedelta(minutes=30)]

    #calculate total windspeed
    total_df['wspd10m'] = np.sqrt(np.square(total_df['uwnd10m'].dropna()) + np.square(total_df['vwnd10m'].dropna()))

    # remove unwanted wind data
    total_df.drop(['uwnd10m','vwnd10m'], inplace=True, axis=1)

    # round data to two decimal places in line with files supplied by UMEP
    total_df[total_df.columns.difference(['Year','DOY','Hour','Min'])] = total_df[total_df.columns.difference(['Year','DOY','Hour','Min'])].round(2)

    # create a dataframe with the headings specified @ https://umep-docs.readthedocs.io/en/latest/pre-processor/Meteorological%20Data%20MetPreprocessor.html
    met_df = pd.DataFrame(columns=['iy','id','it','imin','qn','qh','qe','qs','qf','U','RH','Tair','pres','rain','kdown','snow','ldown','fcld','wuh','xsmd','lai','kdiff','kdir','wdir'])

    # fill met_df with the appropriate data from total_df
    met_df[['iy','id','it','imin','Tair','RH','U','kdiff','kdir','kdown','ldown']] = total_df[['Year','DOY','Hour','Min','temp_scrn','rh2m','wspd10m','av_sfc_sw_dif','av_sfc_sw_dir','av_swsfcdown','av_lwsfcdown']]


    # fill all Nans with -999.00 in accordance with https://umep-docs.readthedocs.io/en/latest/pre-processor/Meteorological%20Data%20MetPreprocessor.html
    met_df = met_df.fillna(-999.00)

        # optional timer end
    t1=time.time()

    # optional print timing
    print(t1-t0)

    # sets output path for use on Jupyter
    csv_path = '/mnt/bweeding_workspace/output'

    csv_output = os.path.join(csv_path,'metfile_'+start_date+'_'+end_date+'.txt')

    # export met_df to spaced separated text file for use in UMEP, named with start and end dates
    met_df.to_csv(csv_output,index=False,sep=' ')