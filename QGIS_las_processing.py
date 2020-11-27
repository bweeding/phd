# -*- coding: utf-8 -*-
"""
Created on Fri Nov 27 15:42:57 2020

@author: weedingb
"""

from qgis import processing

# to get help
# processing.algorithmHelp("LAStools:lasclip")



# keeps classes 3 4 5
processing.run("LAStools:las2las_filter",{'CPU64':True,
                'INPUT_LASLAZ':'C:/Users/weedingb/Desktop/Learning_LAStools/ClimateFuturesDerwent2008-C2-AHD_5265250_55.las',
                'OUTPUT_LASLAZ':'C:/Users/weedingb/Desktop/Learning_LAStools/veg.las',
                'FILTER_RETURN_CLASS_FLAGS1':12,
                'FILTER_COORDS_INTENSITY1_ARG':'None',
                'FILTER_COORDS_INTENSITY2_ARG':'None'})
                

processing.run("LAStools:lasclip",{'CPU64':True,
                'INPUT_LASLAZ':'C:/Users/weedingb/Desktop/Learning_LAStools/veg.las',
                'OUTPUT_LASLAZ':'C:/Users/weedingb/Desktop/Learning_LAStools/veg_outside_buildings.las',
                'INPUT_GENERIC':'C:/Users/weedingb/Desktop/LIST_2D_BUILDING_POLYS_HOBART/list_2d_building_polys_hobart.shp',
                'INTERIOR':True,
                'OPERATION':0,
                'CLASSIFY_AS:':12})
                
# doesn't work as there's no ground!?                
processing.run("LAStools:lasheight",{'CPU64':True,
                'INPUT_LASLAZ':'C:/Users/weedingb/Desktop/Learning_LAStools/veg_outside_buildings.las',
                'OUTPUT_LASLAZ':'C:/Users/weedingb/Desktop/Learning_LAStools/veg_outside_buildings_ZMIN_2-5.las',
                'DROP_BELOW':True,
                'DROP_BELOW_HEIGHT':2.5})
                