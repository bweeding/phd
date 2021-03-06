# -*- coding: utf-8 -*-
"""
Created on Fri Mar 12 12:37:31 2021

@author: weedingb
"""
#%% inputs to add
#home_folder


#%% debug from here

import sys
import os
from qgis import processing
from qgis.core import QgsApplication
from qgis.core import QgsCoordinateReferenceSystem
from qgis.core import QgsProject
from qgis.core import QgsRasterLayer
from qgis.core import QgsProcessingFeedback
from qgis.analysis import QgsNativeAlgorithms


# Initiating a QGIS application
qgishome = 'C:/Program Files/QGIS 3.16/apps/qgis/'
QgsApplication.setPrefixPath(qgishome, True)
app = QgsApplication([], False)
app.initQgis()

QgsProject.instance().setCrs(QgsCoordinateReferenceSystem('EPSG:28355'))

#import processing
from processing.core.Processing import Processing
Processing.initialize()
QgsApplication.processingRegistry().addProvider(QgsNativeAlgorithms())

# import third party processing plugins
sys.path.append(r'C:\Users\weedingb\AppData\Roaming\QGIS\QGIS3\profiles\default\python\plugins')

from processing_umep.processing_umep_provider import ProcessingUMEPProvider
umep_provider = ProcessingUMEPProvider()
QgsApplication.processingRegistry().addProvider(umep_provider)
# returns True


# works!
from processing_fusion.fusionProvider import FusionProvider
fusion_provider = FusionProvider()
QgsApplication.processingRegistry().addProvider(fusion_provider)

# sets home folder location
home_folder = 'C:\\Users\\weedingb\\Desktop\\utas_solweig_run'

las_loc = home_folder+'\\MtWellington2011-C2-AHD_5265249_55_classified.las'

build_loc = home_folder+'\\list_2d_building_polys_hobart.shp'

for alg in QgsApplication.processingRegistry().algorithms():
    print("{}:{} --> {}".format(alg.provider().name(), alg.name(), alg.displayName()))

################################################################################
# Do this later, polyclipdata won't run if the shape file is loaded!?!?

# loads the building shape file
#building_layer = QgsVectorLayer(home_folder+'\\list_2d_building_polys_hobart.shp', 'buildings', 'ogr')

# adds the building shapefile as a layer
#QgsProject.instance().addMapLayer(building_layer)

################################################################################

# specifies the location of the current las file and buildings file
# should it just auto select a .las file? How will we structure? 
# depends on run time!


#%%
# creates a DEM (grid surface create class 2)
alg_params_DEM = {
    'ADVANCED_MODIFIERS': '',
    'CELLSIZE': 1,
    'CLASS': '2',
    'INPUT': las_loc,
    'MEDIAN': '',
    'MINIMUM': '',
    'SLOPE': '',
    'SMOOTH': '',
    'SPIKE': '',
    'VERSION64': True,
    'XYUNITS': 0,
    'ZUNITS': 0,
    'OUTPUT_DTM': home_folder+'\\DEM.dtm'
}
    
dem = processing.run('fusion:gridsurfacecreate', alg_params_DEM)

processing.run("fusion:dtm2tif", {'INPUT':home_folder+'/DEM.dtm','MASK':False,'OUTPUT':home_folder+'/DEM.tif'})

os.system('python %CONDA_PREFIX%\Scripts\gdal_edit.py -a_srs EPSG:28355 C:/Users/weedingb/Desktop/utas_solweig_run/DEM.tif')
#%%
# Process the las files

# ground_outside_b.las
alg_params_ground_outside_b = {
    'ADVANCED_MODIFIERS': '/outside /class:2',
    'FIELD': '',
    'INPUT': las_loc,
    'MASK': build_loc,
    'SHAPE': False,
    'VALUE': '',
    'VERSION64': True,
    'OUTPUT': home_folder+'\\ground_outside_b.las'
}
ground_outside_b = processing.run('fusion:pollyclipdata',alg_params_ground_outside_b)
    
    
# veg_outside_b.las
alg_params_veg_outside_b = {
    'ADVANCED_MODIFIERS': '/outside /class:3,4,5',
    'FIELD': '',
    'INPUT': las_loc,
    'MASK': build_loc,
    'SHAPE': False,
    'VALUE': '',
    'VERSION64': True,
    'OUTPUT': home_folder+'\\veg_outside_b.las'
}
veg_outside_b = processing.run('fusion:pollyclipdata', alg_params_veg_outside_b)    
    
# buildings_inside_b.las
alg_params_buildings_inside_b = {
    'ADVANCED_MODIFIERS': '/class:6',
    'FIELD': '',
    'INPUT': las_loc,
    'MASK': build_loc,
    'SHAPE': False,
    'VALUE': '',
    'VERSION64': True,
    'OUTPUT': home_folder+'\\buildings_inside_b.las'
}
buildings_inside_b = processing.run('fusion:pollyclipdata', alg_params_buildings_inside_b)   

#%%

# DSM - ground isn't working!
alg_params_dsm = {
    'ADVANCED_MODIFIERS': '',
    'ASCII': True,
    'CELLSIZE': 1,
    'CLASS': '',
    'GROUND': home_folder+'\\DEM.dtm',
    'INPUT': home_folder+'\\ground_outside_b.las'+';'+home_folder+'\\buildings_inside_b.las',
    'MEDIAN': '',
    'SLOPE': False,
    'SMOOTH': '',
    'VERSION64': True,
    'XYUNITS': 0,
    'ZUNITS': 0,
    'OUTPUT': home_folder+'\\DSM.asc'
}
DSM = processing.run('fusion:canopymodel', alg_params_dsm)   

#processing.run("gdal:translate", {'INPUT':'C:/Users/weedingb/Desktop/utas_solweig_run/DSM.asc','TARGET_CRS':None,'NODATA':None,'COPY_SUBDATASETS':False,'OPTIONS':'','EXTRA':'','DATA_TYPE':0,'OUTPUT':'C:/Users/weedingb/Desktop/utas_solweig_run/DSM.tif'}) 

# Works! assigns crs on generation of tif
processing.run("gdal:translate", {'INPUT':'C:/Users/weedingb/Desktop/utas_solweig_run/DSM.asc','TARGET_CRS':QgsCoordinateReferenceSystem('EPSG:28355'),'NODATA':None,'COPY_SUBDATASETS':False,'OPTIONS':'','EXTRA':'','DATA_TYPE':0,'OUTPUT':'C:/Users/weedingb/Desktop/utas_solweig_run/DSM.tif'})

#os.system('python %CONDA_PREFIX%\Scripts\gdal_edit.py -a_srs EPSG:28355 C:/Users/weedingb/Desktop/utas_solweig_run/DSM.tif')

#%%

# Convert extent of DSM to a shapefile
alg_params_extent = {
    'INPUT':home_folder+'\\DSM.asc',
    'OUTPUT':home_folder+'\\DSM_extent.shp'
}

#QgsProcessingException: Error: Algorithm native:polygonfromlayerextent not found
# "extract layer extent"
extent = processing.run('native:polygonfromlayerextent',alg_params_extent)

# extract vegetation above 2.5m
alg_params_veg_outside_b_zmin2_5 = {
    'ADVANCED_MODIFIERS': '',
    'CLASS': '',
    'DTM': '',#home_folder+'\\DEM.dtm',
    'EXTENT': home_folder+'\\DSM_extent.shp',
    'HEIGHT': False,
    'IGNOREOVERLAP': False,
    'INPUT': home_folder+'\\veg_outside_b.las',
    'SHAPE': 0,
    'VERSION64': True,
    'OUTPUT': home_folder+'\\veg_outside_b_zmin2_5.las'
}
veg_outside_b_zmin2_5 = processing.run('fusion:clipdata', alg_params_veg_outside_b_zmin2_5)


alg_params_cdsm = {
    'ADVANCED_MODIFIERS': '',
    'ASCII': True,
    'CELLSIZE': 1,
    'CLASS': '',
    'GROUND': home_folder+'\\DEM.dtm',
    'INPUT': home_folder+'\\ground_outside_b.las'+';'+home_folder+'\\veg_outside_b_zmin2_5.las',
    'MEDIAN': '',
    'SLOPE': False,
    'SMOOTH': '',
    'VERSION64': True,
    'XYUNITS': 0,
    'ZUNITS': 0,
    'OUTPUT': home_folder+'\\CDSM.asc'
}
#also produces CDSM.asc
CDSM = processing.run('fusion:canopymodel', alg_params_cdsm)  

processing.run("gdal:translate", {'INPUT':'C:/Users/weedingb/Desktop/utas_solweig_run/CDSM.asc','TARGET_CRS':QgsCoordinateReferenceSystem('EPSG:28355'),'NODATA':None,'COPY_SUBDATASETS':False,'OPTIONS':'','EXTRA':'','DATA_TYPE':0,'OUTPUT':'C:/Users/weedingb/Desktop/utas_solweig_run/CDSM.tif'})


#os.system('python %CONDA_PREFIX%\Scripts\gdal_edit.py -a_srs EPSG:28355 C:/Users/weedingb/Desktop/utas_solweig_run/CDSM.tif')


#%%

# building_footprint_buffered
alg_params_buildings_buffered = {
    'DISSOLVE': False,
    'DISTANCE': 2,
    'END_CAP_STYLE': 1,
    'INPUT': build_loc,
    'JOIN_STYLE': 1,
    'MITER_LIMIT': 2,
    'SEGMENTS': 5,
    'OUTPUT': home_folder+'\\buildings_buffered.shp'
}
buildings_buffered = processing.run('native:buffer', alg_params_buildings_buffered)

# building_footprint_buffered_field_zero
alg_params_buildings_buffered_zeros = {
    'FIELD_LENGTH': 10,
    'FIELD_NAME': 'zeros',
    'FIELD_PRECISION': 3,
    'FIELD_TYPE': 1,
    'FORMULA': 'value = 0',
    'GLOBAL': '',
    'INPUT': home_folder+'\\buildings_buffered.shp',
    'OUTPUT': home_folder+'\\buildings_buffered_zeros.shp'
}
buildings_buffered_zeros = processing.run('qgis:advancedpythonfieldcalculator', alg_params_buildings_buffered_zeros)

# building_footprint_raster
alg_params_buildings_buffered_raster = {
    'BURN': '',
    'DATA_TYPE': 5,
    'EXTENT': home_folder+'\\DSM_extent.shp',
    'EXTRA': '',
    'FIELD': 'zeros',
    'HEIGHT': 1,
    'INIT': 1,
    'INPUT': home_folder+'\\buildings_buffered_zeros.shp',
    'INVERT': False,
    'NODATA': None,
    'OPTIONS': '',
    'UNITS': 1,
    'WIDTH': 1,
    'OUTPUT': home_folder+'\\buildings_buffered_raster.tif'
}
buildings_buffered_raster = processing.run('gdal:rasterize', alg_params_buildings_buffered_raster)


#%% 


# alg_params_cdsm_filt1 = {
#     'INPUT_A':home_folder+'\\CDSM.tif',
#     'BAND_A':1,
#     'INPUT_B':home_folder+'\\buildings_buffered_raster.tif',
#     'BAND_B':None,
#     'INPUT_C':None,'BAND_C':None,'INPUT_D':None,'BAND_D':None,'INPUT_E':None,'BAND_E':None,'INPUT_F':None,'BAND_F':None,
#     'FORMULA':'A*B',
#     'NO_DATA':None,
#     'RTYPE':5,
#     'OPTIONS':'',
#     'EXTRA':'',
#     'OUTPUT':home_folder+'\\CDSM_filt1.tif'}

# cdsm_filt1 = processing.run("gdal:rastercalculator", alg_params_cdsm_filt1)

# cdsm_layer = QgsRasterLayer(home_folder+'\\CDSM.tif')
# cdsm_extent = cdsm_layer.extent()
# cdsm_layer_loc = home_folder+'\\CDSM.tif'

# buildings_layer = QgsRasterLayer(home_folder+'\\buildings_buffered_raster.tif')
# buildings_layer_loc = home_folder+'\\buildings_buffered_raster.tif'

os.system('python %CONDA_PREFIX%\Scripts\gdal_calc.py --calc "A*B" --format GTiff --type Float32 -A C:/Users/weedingb/Desktop/utas_solweig_run/buildings_buffered_raster.tif --A_band 1 -B C:/Users/weedingb/Desktop/utas_solweig_run/CDSM.tif --outfile C:/Users/weedingb/Desktop/utas_solweig_run/CDSM_filt1.tif'
)

# alg_params = {
#      'CELLSIZE': 0,
#      'CRS':QgsCoordinateReferenceSystem("EPSG:28355"),
#      'EXPRESSION': f'{cdsm_layer_loc}@1*{buildings_layer_loc}@1',
#      'EXTENT': cdsm_extent,
#      'LAYERS': [cdsm_layer],
#      'OUTPUT': home_folder+'\\raster_multiplied.tif'
#  }

# result = processing.run('qgis:rastercalculator', alg_params)
 
# processing.run("qgis:rastercalculator", 
#                 {'EXPRESSION':'\"CDSM@1\" * \"buildings_buffered_raster@1\"',
#                  'LAYERS':['C:/Users/weedingb/Desktop/utas_solweig_run/CDSM.tif'],
#                  'CELLSIZE':0,
#                  'EXTENT':None,
#                  'CRS':QgsCoordinateReferenceSystem('EPSG:28355'),
#                  'OUTPUT':'C:/Users/weedingb/Desktop/utas_solweig_run/rast_calc_output.tif'})

#%%

#layer3 = QgsRasterLayer(home_folder+'\\CDSM_filt1.tif','CDSM_filt1')

# alg_params_cdsm_filt2 = {
#     'INPUT_A':home_folder+'\\CDSM_filt1.tif',
#     'BAND_A':1,
#     'INPUT_B':None,'BAND_B':None,'INPUT_C':None,'BAND_C':None,'INPUT_D':None,'BAND_D':None,'INPUT_E':None,'BAND_E':None,'INPUT_F':None,'BAND_F':None,
#     'FORMULA':'(A>0.5)*A',
#     'NO_DATA':None,
#     'RTYPE':5,
#     'OPTIONS':'',
#     'EXTRA':'',
#     'OUTPUT':home_folder+'\\CDSM_filt2.tif'}

# processing.run("gdal:rastercalculator", alg_params_cdsm_filt2)

os.system('python %CONDA_PREFIX%\Scripts\gdal_calc.py --calc "(A>0.5)*A" --format GTiff --type Float32 -A C:/Users/weedingb/Desktop/utas_solweig_run/CDSM_filt1.tif --A_band 1 --outfile C:/Users/weedingb/Desktop/utas_solweig_run/CDSM_filt2.tif'
)

processing.run("gdal:assignprojection", {'INPUT':home_folder+'/CDSM_filt2.tif','CRS':'QgsCoordinateReferenceSystem("EPSG:28355")'})

# clip files for processing speed on my machine
#%%

files_in = [home_folder+'/CDSM_filt2.tif',
            home_folder+'/DEM.tif',
            home_folder+'/DSM.tif']

files_out = [home_folder+'/CDSM_clipped.tif',
            home_folder+'/DEM_clipped.tif',
            home_folder+'/DSM_clipped.tif']

for file_in,file_out in zip(files_in,files_out):

    processing.run("gdal:cliprasterbyextent", 
        {'INPUT':file_in,
        'PROJWIN':'526402.3861,526823.6200,5249680.3568,5249990.0000 [EPSG:28355]',
        'NODATA':None,
        'OPTIONS':'',
        'DATA_TYPE':0,
        'EXTRA':'',
        'OUTPUT':file_out})
#%% Current limit
# Addition of DEM to DSM and CDSM following advice of F.Lindberg
#processing.run("gdal:rastercalculator", {'INPUT_A':home_folder+'/DSM_clipped.tif','BAND_A':1,'INPUT_B':home_folder+'/DEM_clipped.tif','BAND_B':None,'INPUT_C':None,'BAND_C':None,'INPUT_D':None,'BAND_D':None,'INPUT_E':None,'BAND_E':None,'INPUT_F':None,'BAND_F':None,'FORMULA':'A+B','NO_DATA':None,'RTYPE':5,'OPTIONS':'','EXTRA':'','OUTPUT':home_folder+'/DSM_clipped_addDEM.tif'})

os.system('python %CONDA_PREFIX%\Scripts\gdal_calc.py --calc "A+B" --format GTiff --type Float32 -A C:/Users/weedingb/Desktop/utas_solweig_run/DEM_clipped.tif --A_band 1 -B C:/Users/weedingb/Desktop/utas_solweig_run/DSM_clipped.tif --outfile C:/Users/weedingb/Desktop/utas_solweig_run/DSM_clipped_addDEM.tif'
)

#processing.run("gdal:rastercalculator", {'INPUT_A':home_folder+'/CDSM_clipped.tif','BAND_A':1,'INPUT_B':home_folder+'/DEM_clipped.tif','BAND_B':None,'INPUT_C':None,'BAND_C':None,'INPUT_D':None,'BAND_D':None,'INPUT_E':None,'BAND_E':None,'INPUT_F':None,'BAND_F':None,'FORMULA':'A+B','NO_DATA':None,'RTYPE':5,'OPTIONS':'','EXTRA':'','OUTPUT':home_folder+'/CDSM_clipped_addDEM.tif'})

os.system('python %CONDA_PREFIX%\Scripts\gdal_calc.py --calc "A+B" --format GTiff --type Float32 -A C:/Users/weedingb/Desktop/utas_solweig_run/CDSM_clipped.tif --A_band 1 -B C:/Users/weedingb/Desktop/utas_solweig_run/DEM_clipped.tif --outfile C:/Users/weedingb/Desktop/utas_solweig_run/CDSM_clipped_addDEM.tif'
)


#%%
# generation of sky view factors - slow!

processing.run("umep:Urban Geometry: Sky View Factor", 
    {'INPUT_DSM':home_folder+'/DSM_clipped_addDEM.tif',
    'USE_VEG':True,
    'TRANS_VEG':3,
    'INPUT_CDSM':home_folder+'/CDSM_clipped_addDEM.tif',
    'TSDM_EXIST':False,
    'INPUT_TDSM':None,
    'INPUT_THEIGHT':25,
    'ANISO':False,
    'OUTPUT_DIR':home_folder,
    'OUTPUT_FILE':home_folder+'/sky_view.tif'})
    

processing.run("umep:Urban Geometry: Wall Height and Aspect", 
    {'INPUT':home_folder+'/DSM_clipped_addDEM.tif',
    'ASPECT_BOOL':True,
    'INPUT_LIMIT':3,
    'OUTPUT_HEIGHT':home_folder+'/height.tif',
    'OUTPUT_ASPECT':home_folder+'/aspect.tif'})
    
#%%
# run SOLWEIG

processing.run("umep:Outdoor Thermal Comfort: SOLWEIG", 
    {'INPUT_DSM':home_folder+'/DSM_clipped_addDEM.tif',
    'INPUT_SVF':home_folder+'\\svfs.zip',
    'INPUT_HEIGHT':home_folder+'/height.tif',
    'INPUT_ASPECT':home_folder+'/aspect.tif',
    'USE_VEG':True,
    'TRANS_VEG':3,
    'INPUT_CDSM':home_folder+'/CDSM_clipped_addDEM.tif',
    'TSDM_EXIST':False,
    'INPUT_TDSM':None,
    'INPUT_THEIGHT':25,
    'USE_LC':False,
    'INPUT_LC':None,
    'USE_LC_BUILD':False,
    'INPUT_DEM':home_folder+'/DEM_clipped_addDEM.tif',
    'SAVE_BUILD':False,
    'USE_ANISO':False,
    'INPUT_ANISO':'',
    'ALBEDO_WALLS':0.2,
    'ALBEDO_GROUND':0.15,
    'EMIS_WALLS':0.9,
    'EMIS_GROUND':0.95,
    'ABS_S':0.7,
    'ABS_L':0.95,
    'POSTURE':0,
    'CYL':True,
    'INPUTMET':home_folder+'\\metfile_20190105_20190106_tester.txt',
    'ONLYGLOBAL':False,
    'UTC':0,
    'POI':False,
    'POI_FILE':None,
    'POI_FIELD':'',
    'AGE':35,
    'ACTIVITY':80,
    'CLO':0.9,
    'WEIGHT':75,
    'HEIGHT':180,
    'SEX':0,
    'SENSOR_HEIGHT':10,
    'OUTPUT_TMRT':True,
    'OUTPUT_KDOWN':True,
    'OUTPUT_KUP':False,
    'OUTPUT_LDOWN':False,
    'OUTPUT_LUP':False,
    'OUTPUT_SH':False,
    'OUTPUT_DIR':home_folder+'\\SOLWEIG_output'})

    
    
    
    
    
    
    
    