# -*- coding: utf-8 -*-
"""
Created on Fri Nov 27 15:42:57 2020

@author: weedingb
"""

from qgis import processing

# to get help
# processing.algorithmHelp("LAStools:lasclip")

processing.run("",{'':,
                "":
                "":
                "":
                "":
                ""})

# Initial separation into ground, buildings, vegetation
##############################################################################
# create .las from 2 - ground class
processing.run("LAStools:las2las_filter",{'CPU64':True,
                'INPUT_LASLAZ':'C:/Users/weedingb/Desktop/Learning_LAStools/ClimateFuturesDerwent2008-C2-AHD_5265250_55.las',
                'OUTPUT_LASLAZ':'C:/Users/weedingb/Desktop/Learning_LAStools/ground.las',
                'FILTER_RETURN_CLASS_FLAGS1':7,
                'FILTER_COORDS_INTENSITY1_ARG':'None',
                'FILTER_COORDS_INTENSITY2_ARG':'None'})

# create .las from 6 - buildings class
processing.run("LAStools:las2las_filter",{'CPU64':True,
                'INPUT_LASLAZ':'C:/Users/weedingb/Desktop/Learning_LAStools/ClimateFuturesDerwent2008-C2-AHD_5265250_55.las',
                'OUTPUT_LASLAZ':'C:/Users/weedingb/Desktop/Learning_LAStools/buildings.las',
                'FILTER_RETURN_CLASS_FLAGS1':10,
                'FILTER_COORDS_INTENSITY1_ARG':'None',
                'FILTER_COORDS_INTENSITY2_ARG':'None'})

# create .las from 3 4 5 - vegetation classes
processing.run("LAStools:las2las_filter",{'CPU64':True,
                'INPUT_LASLAZ':'C:/Users/weedingb/Desktop/Learning_LAStools/ClimateFuturesDerwent2008-C2-AHD_5265250_55.las',
                'OUTPUT_LASLAZ':'C:/Users/weedingb/Desktop/Learning_LAStools/veg.las',
                'FILTER_RETURN_CLASS_FLAGS1':12,
                'FILTER_COORDS_INTENSITY1_ARG':'None',
                'FILTER_COORDS_INTENSITY2_ARG':'None'})

##############################################################################
                
# filter out vegetation inside buildings
processing.run("LAStools:lasclip",{'CPU64':True,
                'INPUT_LASLAZ':'C:/Users/weedingb/Desktop/Learning_LAStools/veg.las',
                'OUTPUT_LASLAZ':'C:/Users/weedingb/Desktop/Learning_LAStools/veg_outside_buildings.las',
                'INPUT_GENERIC':'C:/Users/weedingb/Desktop/LIST_2D_BUILDING_POLYS_HOBART/list_2d_building_polys_hobart.shp',
                'INTERIOR':True,
                'OPERATION':0,
                'CLASSIFY_AS:':2})
                
# filter out buildings outside buildings
processing.run("LAStools:lasclip",{'CPU64':True,
                'INPUT_LASLAZ':'C:/Users/weedingb/Desktop/Learning_LAStools/buildings.las',
                'OUTPUT_LASLAZ':'C:/Users/weedingb/Desktop/Learning_LAStools/buildings_inside_buildings.las',
                'INPUT_GENERIC':'C:/Users/weedingb/Desktop/LIST_2D_BUILDING_POLYS_HOBART/list_2d_building_polys_hobart.shp',
                'INTERIOR':False,
                'OPERATION':0,
                'CLASSIFY_AS:':6})

# merge ground and vegetation data - not working, can do with command line
processing.run("LAStools:lasmerge",{'CPU64':True,
                'INPUT_LASLAZ':'C:/Users/weedingb/Desktop/Learning_LAStools/ground.las',
                'FILE2':'C:/Users/weedingb/Desktop/Learning_LAStools/veg_outside_buildings.las',
                'OUTPUT_LASLAZ':'C:/Users/weedingb/Desktop/Learning_LAStools/ground_and_veg_outside_buildings.las'})

processing.run("LAStools:las2dem",{'CPU64':True,
                'INPUT_LASLAZ':'C:/Users/weedingb/Desktop/Learning_LAStools/ground_and_veg_outside_buildings.las',
                'OUTPUT_LASLAZ':'C:/Users/weedingb/Desktop/Learning_LAStools/CDSM.tif'})


# gives us all points 2.5m+ above the ground (will be only veg)             
processing.run("LAStools:lasheight",{'CPU64':True,
                'INPUT_LASLAZ':'C:/Users/weedingb/Desktop/Learning_LAStools/ground_and_veg_outside_buildings.las',
                'OUTPUT_LASLAZ':'C:/Users/weedingb/Desktop/Learning_LAStools/ground_and_veg_outside_buildings.las_ZMIN_2-5.las',
                'DROP_BELOW':True,
                'DROP_BELOW_HEIGHT':2.5})

# Used las merge to create CDSM_veg_2-5.las  
# Now convert to .tif
processing.run("LAStools:las2dem",{'CPU64':True,
                'INPUT_LASLAZ':'C:/Users/weedingb/Desktop/Learning_LAStools/CDSM_veg_2-5.las',
                'OUTPUT_RASTER':'C:/Users/weedingb/Desktop/Learning_LAStools/CDSM_veg_2-5.tif'})









                