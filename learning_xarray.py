# -*- coding: utf-8 -*-
"""
Created on Mon Mar  1 15:17:38 2021

@author: weedingb
"""

import xarray as xr
import pandas as pd
import numpy as np

arr = xr.DataArray(
    np.random.rand(4,6),
    dims=('x','y'),
    coords={
        'x':[-3.2,2.1,5.3,6.5],
        'y':pd.date_range('2009-01-05',periods=6,freq='M')
        }
    )

arr.y[1]

arr.sel(x=5.3,y='2009-04-30')

arr.sel(x=5.3,y=arr.y[1])

#all dimensions are coded as a pandas series

arr.sel(x=5.3,y='2009-04-30',method='nearest')