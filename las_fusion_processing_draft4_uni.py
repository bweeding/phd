#%% Import and setup of PyQGIS environment

# import packages
import sys
import os
import time
import datetime
from qgis import processing
from qgis.core import QgsApplication, QgsProject, QgsCoordinateReferenceSystem
from qgis.analysis import QgsNativeAlgorithms
from osgeo import gdal


# initiate a PyQGIS application
qgishome = 'C:/Program Files/QGIS 3.16/apps/qgis/'
QgsApplication.setPrefixPath(qgishome, True)
app = QgsApplication([], False)
app.initQgis()

# set the coordinate reference system of the project
QgsProject.instance().setCrs(QgsCoordinateReferenceSystem('EPSG:28355'))

# import and activate the QGIS native processing algorithms
from processing.core.Processing import Processing
Processing.initialize()
QgsApplication.processingRegistry().addProvider(QgsNativeAlgorithms())

# add the folder containing 3rd party processing algorithm to the path
sys.path.append(r'C:\Users\weedingb\AppData\Roaming\QGIS\QGIS3\profiles\default\python\plugins')

# import UMEP processing tools
from processing_umep.processing_umep_provider import ProcessingUMEPProvider
umep_provider = ProcessingUMEPProvider()
QgsApplication.processingRegistry().addProvider(umep_provider)

# import Fusion processing tools
from processing_fusion.fusionProvider import FusionProvider
fusion_provider = FusionProvider()
QgsApplication.processingRegistry().addProvider(fusion_provider)

# sets base folder location
base_folder = 'C:\\Users\\weedingb\\Desktop\\utas_solweig_run\\'

# creates run folder
os.mkdir(base_folder+'SOLWEIG_run_'+datetime.datetime.now().strftime('%d-%m-%Y_%H%M'))

# sets run folder location
run_folder = base_folder+'SOLWEIG_run_'+datetime.datetime.now().strftime('%d-%m-%Y_%H%M')+'\\'

# creates output folder
os.mkdir(run_folder+'SOLWEIG_output'+datetime.datetime.now().strftime('%d-%m-%Y_%H%M'))

# sets output folder location
output_folder = run_folder+'SOLWEIG_output'+datetime.datetime.now().strftime('%d-%m-%Y_%H%M')

# sets the LAS (lidar) path and filename
las_loc = base_folder+'MtWellington2011-C2-AHD_5265249_55_classified.las'

# sets the building shape file path and filename
build_loc = base_folder+'list_2d_building_polys_hobart.shp'

# lists all available processing algorithms, commented out by default
# for alg in QgsApplication.processingRegistry().algorithms():
#     print("{}:{} --> {}".format(alg.provider().name(), alg.name(), alg.displayName()))

#%% Digital elevation model production

# creates a DEM using fusion:gridsurfacecreate in .dtm format
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
    'OUTPUT_DTM': run_folder+'DEM.dtm'
}
    
dem = processing.run('fusion:gridsurfacecreate', alg_params_DEM)

# converts the .dtm to .tif using fusion:dtm2tif
processing.run("fusion:dtm2tif", {'INPUT':run_folder+'DEM.dtm','MASK':False,'OUTPUT':run_folder+'DEM_nopro.tif'})
# modify resampling to alter banding artifacts? 1?
processing.run("gdal:warpreproject", {'INPUT':run_folder+'DEM_nopro.tif','SOURCE_CRS':None,'TARGET_CRS':QgsCoordinateReferenceSystem('EPSG:28355'),'RESAMPLING':0,'NODATA':None,'TARGET_RESOLUTION':None,'OPTIONS':'','DATA_TYPE':0,'TARGET_EXTENT':None,'TARGET_EXTENT_CRS':None,'MULTITHREADING':False,'EXTRA':'','OUTPUT':run_folder+'DEM.tif'})

#%% Classifcation of LAS file/LIDAR data

# classifies and clips ground points outside buildings using fusion:pollyclipdata
alg_params_ground_outside_b = {
    'ADVANCED_MODIFIERS': '/outside /class:2',
    'FIELD': '',
    'INPUT': las_loc,
    'MASK': build_loc,
    'SHAPE': False,
    'VALUE': '',
    'VERSION64': True,
    'OUTPUT': run_folder+'ground_outside_b.las'
}
ground_outside_b = processing.run('fusion:pollyclipdata',alg_params_ground_outside_b)
    
    
# classifies and clips vegetation points outside buildings using fusion:pollyclipdata
alg_params_veg_outside_b = {
    'ADVANCED_MODIFIERS': '/outside /class:3,4,5',
    'FIELD': '',
    'INPUT': las_loc,
    'MASK': build_loc,
    'SHAPE': False,
    'VALUE': '',
    'VERSION64': True,
    'OUTPUT': run_folder+'veg_outside_b.las'
}
veg_outside_b = processing.run('fusion:pollyclipdata', alg_params_veg_outside_b)    
    
# classifies and clips building points inside buildings using fusion:pollyclipdata
alg_params_buildings_inside_b = {
    'ADVANCED_MODIFIERS': '/class:6',
    'FIELD': '',
    'INPUT': las_loc,
    'MASK': build_loc,
    'SHAPE': False,
    'VALUE': '',
    'VERSION64': True,
    'OUTPUT': run_folder+'buildings_inside_b.las'
}
buildings_inside_b = processing.run('fusion:pollyclipdata', alg_params_buildings_inside_b)   

#%% Digital surface model production

# creates a DSM using fusion:canopymodel in .dtm format
alg_params_dsm = {
    'ADVANCED_MODIFIERS': '',
    'ASCII': True,
    'CELLSIZE': 1,
    'CLASS': '',
    'GROUND': '',#run_folder+'DEM.dtm', don't use ground.dtm according to FL
    'INPUT': run_folder+'ground_outside_b.las'+';'+run_folder+'buildings_inside_b.las',
    'MEDIAN': '',
    'SLOPE': False,
    'SMOOTH': '',
    'VERSION64': True,
    'XYUNITS': 0,
    'ZUNITS': 0,
    'OUTPUT': run_folder+'DSM.dtm'
}
DSM = processing.run('fusion:canopymodel', alg_params_dsm)

# converts the .dtm to .tif using fusion:dtm2tif
processing.run("fusion:dtm2tif", {'INPUT':run_folder+'DSM.dtm','MASK':False,'OUTPUT':run_folder+'DSM_nopro.tif'})
#processing.run("fusion:dtm2tif", {'INPUT':run_folder+'DSM.dtm','MASK':False,'OUTPUT':run_folder+'DSM_dummy.tif'})

processing.run("gdal:warpreproject", {'INPUT':run_folder+'DSM_nopro.tif','SOURCE_CRS':None,'TARGET_CRS':QgsCoordinateReferenceSystem('EPSG:28355'),'RESAMPLING':0,'NODATA':None,'TARGET_RESOLUTION':None,'OPTIONS':'','DATA_TYPE':0,'TARGET_EXTENT':None,'TARGET_EXTENT_CRS':None,'MULTITHREADING':False,'EXTRA':'','OUTPUT':run_folder+'DSM.tif'})

# converts extent of the DSM to a shapefile using native:polygonfromlayerextent
alg_params_extent = {
    'INPUT':run_folder+'DSM.tif',
    'OUTPUT':run_folder+'DSM_extent.shp'
}

extent = processing.run('native:polygonfromlayerextent',alg_params_extent)

#%% Canopy digiital surface model production


# classifies and clips vegetation points outside buildings 2.5m above the DEM using fusion:clipdata
# 'flat base', gives vegetation heights above a flat surface using DTM
alg_params_veg_outside_b_zmin2_5 = {
    'ADVANCED_MODIFIERS':'/zmin:2.5',
    'CLASS': '',
    'DTM':'',
    'EXTENT': run_folder+'DSM_extent.shp',
    'HEIGHT': False,
    'IGNOREOVERLAP': False,
    'INPUT': run_folder+'veg_outside_b.las',
    'SHAPE': 0,
    'VERSION64': True,
    'OUTPUT': run_folder+'veg_outside_b_zmin2_5.las'
}
veg_outside_b_zmin2_5 = processing.run('fusion:clipdata', alg_params_veg_outside_b_zmin2_5)


# creates a CDSM.dtm using fusion:canopy model
alg_params_cdsm = {
    'ADVANCED_MODIFIERS':'/nofill',
    'ASCII': True,
    'CELLSIZE': 1,
    'CLASS': '',
    'GROUND':run_folder+'DEM.dtm',
    'INPUT':run_folder+'\\veg_outside_b_zmin2_5.las', #run_folder+'ground_outside_b.las'+';'+run_folder+'\\veg_outside_b_zmin2_5.las',
    'MEDIAN': '',
    'SLOPE': False,
    'SMOOTH': '',
    'VERSION64': True,
    'XYUNITS': 0,
    'ZUNITS': 0,
    'OUTPUT': run_folder+'CDSM.dtm'
}

CDSM = processing.run('fusion:canopymodel', alg_params_cdsm)  


# why the difference between dtm to tif and dtm to asc? check umep guide for sequence
# 
ds=gdal.Open(run_folder+'CDSM.asc')
ds2=gdal.Translate(run_folder+'CDSM_nopro.tif',ds)

processing.run("gdal:warpreproject", {'INPUT':run_folder+'CDSM_nopro.tif','SOURCE_CRS':None,'TARGET_CRS':QgsCoordinateReferenceSystem('EPSG:28355'),'RESAMPLING':0,'NODATA':None,'TARGET_RESOLUTION':None,'OPTIONS':'','DATA_TYPE':0,'TARGET_EXTENT':None,'TARGET_EXTENT_CRS':None,'MULTITHREADING':False,'EXTRA':'','OUTPUT':run_folder+'CDSM.tif'})

#%% Buffered building raster production

# creates a 1m buffered shape file of buildings using native:buffer
alg_params_buildings_buffered = {
    'DISSOLVE': False,
    'DISTANCE': 1,
    'END_CAP_STYLE': 1,
    'INPUT': build_loc,
    'JOIN_STYLE': 1,
    'MITER_LIMIT': 2,
    'SEGMENTS': 5,
    'OUTPUT': run_folder+'buildings_buffered.shp'
}
buildings_buffered = processing.run('native:buffer', alg_params_buildings_buffered)

# adds a field of zeros to the buffered buildings file using qgis:advancedpythonfieldcalculator
alg_params_buildings_buffered_zeros = {
    'FIELD_LENGTH': 10,
    'FIELD_NAME': 'zeros',
    'FIELD_PRECISION': 3,
    'FIELD_TYPE': 1,
    'FORMULA': 'value = 0',
    'GLOBAL': '',
    'INPUT': run_folder+'buildings_buffered.shp',
    'OUTPUT': run_folder+'buildings_buffered_zeros.shp'
}
buildings_buffered_zeros = processing.run('qgis:advancedpythonfieldcalculator', alg_params_buildings_buffered_zeros)

alg_params_cdsm_extent = {
    'INPUT':run_folder+'CDSM.tif',
    'OUTPUT':run_folder+'CDSM_extent.shp'
}

extentcdsm = processing.run('native:polygonfromlayerextent',alg_params_cdsm_extent)

# creates a .tif from the buffered buildings shape file (with zero field) using gdal:rasterize
alg_params_buildings_buffered_raster = {
    'BURN': '',
    'DATA_TYPE': 5,
    'EXTENT': run_folder+'CDSM_extent.shp',
    'EXTRA': '',
    'FIELD': 'zeros',
    'HEIGHT': 1,
    'INIT': 1,
    'INPUT': run_folder+'buildings_buffered_zeros.shp',
    'INVERT': False,
    'NODATA': None,
    'OPTIONS': '',
    'UNITS': 1,
    'WIDTH': 1,
    'OUTPUT': run_folder+'buildings_buffered_raster.tif'
}
buildings_buffered_raster = processing.run('gdal:rasterize', alg_params_buildings_buffered_raster)


#%% Filtered CDSM production - file size error?! 
# CDSM is 1001x1001, building file is 1001x1003 - clip earlier??

# prepare system string
str_in_AtimesB = 'python %CONDA_PREFIX%\Scripts\gdal_calc.py --calc "A*B" --format GTiff --type Float32 -A '+run_folder+'buildings_buffered_raster.tif --A_band 1 -B '+run_folder+'CDSM.asc --outfile '+run_folder+'CDSM_filt1.tif'

# multiply the buffered building raster with the CDSM using the command line, removing any vegetation present inside the buffered buildings
os.system(str_in_AtimesB)

# prepare system string
str_in_AtimesA = 'python %CONDA_PREFIX%\Scripts\gdal_calc.py --calc "(A>0.5)*A" --format GTiff --type Float32 -A '+run_folder+'CDSM_filt1.tif --A_band 1 --outfile '+run_folder+'CDSM_filt2.tif'

# eliminates small fluctuating elevations produced by the canopy model algorithm when normalised against the DEM.dtm
os.system(str_in_AtimesA)

# assigns a projection to the filtered CDSM of EPSG:28355 using gdal:assignprojection
processing.run("gdal:assignprojection", {'INPUT':run_folder+'CDSM_filt2.tif','CRS':QgsCoordinateReferenceSystem('EPSG:28355')})


#%% Clip raster extents for speed on laptop

files_in = [run_folder+'CDSM_filt2.tif',
            run_folder+'DEM.tif',
            run_folder+'DSM.tif']

files_out = [run_folder+'CDSM_clipped.tif',
            run_folder+'DEM_clipped.tif',
            run_folder+'DSM_clipped.tif']

# for each file in, clip according to the specified coordinates
for file_in,file_out in zip(files_in,files_out):

    processing.run("gdal:cliprasterbyextent", 
        {'INPUT':file_in,
        'PROJWIN':'526707.4469,526794.8455,5249811.8763,5249894.1338 [EPSG:28355]',
        'NODATA':None,
        'OPTIONS':'',
        'DATA_TYPE':0,
        'EXTRA':'',
        'OUTPUT':file_out})


str_in_DSM_addDEM = 'python %CONDA_PREFIX%\Scripts\gdal_calc.py --calc "A+B" --format GTiff --type Float32 -A '+run_folder+'DEM_clipped.tif --A_band 1 -B '+run_folder+'DSM_clipped.tif --outfile '+run_folder+'DSM_clipped_addDEM.tif'

# adds the clipped DEM to the clipped DSM    
os.system(str_in_DSM_addDEM)

processing.run("gdal:assignprojection", {'INPUT':run_folder+'DSM_clipped_addDEM.tif','CRS':QgsCoordinateReferenceSystem('EPSG:28355')})


str_in_CDSM_addDEM = 'python %CONDA_PREFIX%\Scripts\gdal_calc.py --calc "A+B" --format GTiff --type Float32 -A '+run_folder+'DEM_clipped.tif --A_band 1 -B '+run_folder+'CDSM_clipped.tif --outfile '+run_folder+'CDSM_clipped_addDEM.tif'

os.system(str_in_CDSM_addDEM)

processing.run("gdal:assignprojection", {'INPUT':run_folder+'CDSM_clipped_addDEM.tif','CRS':QgsCoordinateReferenceSystem('EPSG:28355')})



#%% Sky view factor and wall data production

# initial time
tick_svf_walls = time.perf_counter()

# calculates sky view factors using UMEP
processing.run("umep:Urban Geometry: Sky View Factor", 
    {'INPUT_DSM':run_folder+'DSM_clipped_addDEM.tif',
    'USE_VEG':True,
    'TRANS_VEG':3,
    'INPUT_CDSM':run_folder+'CDSM_clipped.tif',
    'TSDM_EXIST':False,
    'INPUT_TDSM':None,
    'INPUT_THEIGHT':25,
    'ANISO':False,
    'OUTPUT_DIR':run_folder,
    'OUTPUT_FILE':run_folder+'sky_view.tif'})
    
# calculates wall heights and aspects using UMEP
processing.run("umep:Urban Geometry: Wall Height and Aspect", 
    {'INPUT':run_folder+'DSM_clipped_addDEM.tif',
    'ASPECT_BOOL':True,
    'INPUT_LIMIT':3,
    'OUTPUT_HEIGHT':run_folder+'height.tif',
    'OUTPUT_ASPECT':run_folder+'aspect.tif'})

# finish time
tock_svf_walls = time.perf_counter()
# calculates run time
runtime_svf_walls = str(datetime.timedelta(seconds=tock_svf_walls-tick_svf_walls))


    
#%% SOLWEIG



# initial time
tick_solweig = time.perf_counter()

# runs the SOLWEIG model
processing.run("umep:Outdoor Thermal Comfort: SOLWEIG", 
               {'INPUT_DSM':run_folder+'DSM_clipped_addDEM.tif',
                'INPUT_SVF':run_folder+'svfs.zip',
                'INPUT_HEIGHT':run_folder+'height.tif',
                'INPUT_ASPECT':run_folder+'aspect.tif',
                'INPUT_CDSM':run_folder+'CDSM_clipped.tif',  
                'TRANS_VEG':3,
                'INPUT_TDSM':None,
                'INPUT_THEIGHT':25,
                'INPUT_LC':None,
                'USE_LC_BUILD':False,
                'INPUT_DEM':run_folder+'DEM_clipped.tif',
                'SAVE_BUILD':False,
                'INPUT_ANISO':'',
                'ALBEDO_WALLS':0.2,
                'ALBEDO_GROUND':0.15,
                'EMIS_WALLS':0.9,
                'EMIS_GROUND':0.95,
                'ABS_S':0.7,
                'ABS_L':0.95,
                'POSTURE':0,
                'CYL':True,
                'INPUTMET':base_folder+'metfile_20190105_20190106_tester.txt',
                'ONLYGLOBAL':False,
                'UTC':0,
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
                'OUTPUT_SH':True,
                'OUTPUT_TREEPLANTER':False,
                'OUTPUT_DIR':output_folder})

# finish time
tock_solweig = time.perf_counter()

# calculates run time
runtime_solweig = str(datetime.timedelta(seconds=tock_solweig-tick_solweig))


print(runtime_svf_walls)
print(runtime_solweig)