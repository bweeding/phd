# -*- coding: utf-8 -*-
"""
Created on Tue Jul 27 09:49:47 2021

@author: weedingb
"""

import numpy as np
import pandas as pd
import xarray as xr

# basic construction
data = xr.DataArray(np.random.randn(2, 3), dims=("x", "y"), coords={"x": [10, 20]})

# In this case, we have generated a 2D array, assigned the names x and y to the two dimensions respectively 
# and associated two coordinate labels ‘10’ and ‘20’ with the two locations along the x dimension

# in xarray the x and y (and whatever else) are just measurements of dimension, 
# in this case the data could be in the z dimension! It's a field essentially!!!

# accessing basic info
data.values

data.dims

data.coords

data.attrs

# indexing

# positional and by integer label, like numpy
data[0,:]

#loc or "location": positional and coordinate label, like pandas
data.loc[10]

# isel or "integer select":  by dimension name and integer label
data.isel(x=0)

# sel or "select": by dimension name and coordinate label
data.sel(x=10)

# attributes

data.attrs["long_name"]="random velocity"

data.attrs["units"] = "metres/sec"

data.attrs["description"] = "a random variables created as an example"

data.attrs["random attribute"] = "123"

data.x.attrs["units"] = "x units"

# computation

data + 10

np.sin(data)

data.sum()

data.mean(dim="x") # gives mean at each y value, works along x

data.mean(dim="y") # at each x value, works along y



test = xr.DataArray(landcover_image, dims=("x", "y"), coords={"x": np.arange(1,151),"y": np.arange(1,151)})

