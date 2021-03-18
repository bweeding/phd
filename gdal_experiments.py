# -*- coding: utf-8 -*-
"""
Created on Thu Mar 18 14:30:40 2021

@author: weedingb
"""

import os
import subprocess
from osgeo import gdal

cmd = 'C:\Users\weedingb\Anaconda3\envs\qgis_env\Scripts\gdal_calc.py --calc "A*B" --format GTiff --type Float32 -A C:/Users/weedingb/Desktop/utas_solweig_run/DSM.tif --A_band 1 -B C:/Users/weedingb/Desktop/utas_solweig_run/DEM.tif --outfile C:/Users/weedingb/Desktop/utas_solweig_run/multiplied.tif'

os.system(cmd)

#C:\Users\weedingb\Anaconda3\envs\qgis_env\Scripts\gdal_calc.py


C:\\Users\\weedingb\\Anaconda3\\envs\\qgis_env\\python -m gdal -c

C:\\Users\\weedingb\\Anaconda3\\envs\\qgis_env\\python -m gdal -c gdal_calc --calc "A*B" --format GTiff --type Float32 -A C:/Users/weedingb/Desktop/utas_solweig_run/DSM.tif --A_band 1 -B C:/Users/weedingb/Desktop/utas_solweig_run/DEM.tif --outfile C:/Users/weedingb/Desktop/utas_solweig_run/multiplied.tif


#WORKS!
cmd = 'python %CONDA_PREFIX%\Scripts\gdal_calc.py --calc "A*B" --format GTiff --type Float32 -A C:/Users/weedingb/Desktop/utas_solweig_run/DSM.tif --A_band 1 -B C:/Users/weedingb/Desktop/utas_solweig_run/CDSM.tif --outfile C:/Users/weedingb/Desktop/utas_solweig_run/multiplied.tif'

os.system(cmd)
