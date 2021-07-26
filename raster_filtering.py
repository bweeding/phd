# -*- coding: utf-8 -*-
"""
Created on Mon Jun 21 16:35:52 2021

@author: weedingb
"""

from PIL import Image
import numpy as np
from scipy import ndimage
import matplotlib.pyplot as plt
def conv_mapping(x):
    """
    When the fifth value (x[4]) of the filter array (the center of the window) 
    is null, replace it with the mean of the surrounding values.
    """
    if np.isnan(x[4]) and not np.isnan(np.delete(x, 4)).all():
        return np.nanmean(np.delete(x, 4))
    else:
        return x[4]

photo = Image.open("C:\\Users\\weedingb\\desktop\\Tmrt_daytime_mean.tif")
#photo.show()

data = np.array(photo)
#print(data)
data[data==-9999] = np.nan

plt.hist(data)

photo2 = Image.open("C:\\Users\\weedingb\\desktop\\CDSM_no25.tif")
#photo.show()

data2 = np.array(photo2)
#print(data)
data2[data2==-9999] = np.nan

plt.hist(data2)

datacol = np.reshape(data,data.shape[0]*data.shape[1])
data2col = np.reshape(data2,data2.shape[0]*data2.shape[1])

x=np.column_stack([datacol,data2col])

colors = ['red', 'tan']
plt.hist(x, 50, density=True, histtype='bar', color=colors, label=colors)
plt.legend(prop={'size': 10})
plt.set_title('bars with legend')




# mask = np.ones((3, 3))
# result = ndimage.generic_filter(data, function=conv_mapping, footprint=mask, mode='constant', cval=np.NaN)