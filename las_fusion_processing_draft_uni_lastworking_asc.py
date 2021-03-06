
#%% Import and setup of PyQGIS environment

# import packages
import sys
import os
import time
import datetime
from qgis import processing
from qgis.core import QgsApplication, QgsProject, QgsCoordinateReferenceSystem
from qgis.analysis import QgsNativeAlgorithms


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
from UMEP_processing_main.processing_umep_provider import ProcessingUMEPProvider
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
run_folder = base_folder+'SOLWEIG_run_'+datetime.datetime.now().strftime('%d-%m-%Y_%H%M')

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
processing.run("fusion:dtm2tif", {'INPUT':run_folder+'DEM.dtm','MASK':False,'OUTPUT':run_folder+'DEM.tif'})

# assigns a CRS to the .tif file via the command line
os.system('python %CONDA_PREFIX%\Scripts\gdal_edit.py -a_srs EPSG:28355 C:/Users/weedingb/Desktop/utas_solweig_run/DEM.tif')

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

# creates a DSM using fusion:canopymodel in .asc format
alg_params_dsm = {
    'ADVANCED_MODIFIERS': '',
    'ASCII': True,
    'CELLSIZE': 1,
    'CLASS': '',
    'GROUND': run_folder+'\\DEM.dtm',
    'INPUT': run_folder+'\\ground_outside_b.las'+';'+run_folder+'\\buildings_inside_b.las',
    'MEDIAN': '',
    'SLOPE': False,
    'SMOOTH': '',
    'VERSION64': True,
    'XYUNITS': 0,
    'ZUNITS': 0,
    'OUTPUT': run_folder+'\\DSM.asc'
}
DSM = processing.run('fusion:canopymodel', alg_params_dsm)   

# sets the CRS of the .asc file to EPSG:28355
processing.run("gdal:translate", {'INPUT':'C:/Users/weedingb/Desktop/utas_solweig_run/DSM.asc','TARGET_CRS':QgsCoordinateReferenceSystem('EPSG:28355'),'NODATA':None,'COPY_SUBDATASETS':False,'OPTIONS':'','EXTRA':'','DATA_TYPE':0,'OUTPUT':'C:/Users/weedingb/Desktop/utas_solweig_run/DSM.tif'})

#%% Canopy digiital surface model production

# converts extent of the DSM to a shapefile using native:polygonfromlayerextent
alg_params_extent = {
    'INPUT':run_folder+'\\DSM.asc',
    'OUTPUT':run_folder+'\\DSM_extent.shp'
}

extent = processing.run('native:polygonfromlayerextent',alg_params_extent)

# classifies and clips vegetation points outside buildings 2.5m above the DEM using fusion:clipdata
alg_params_veg_outside_b_zmin2_5 = {
    'ADVANCED_MODIFIERS': '/zmin:2.5',
    'CLASS': '',
    'DTM': run_folder+'\\DEM.dtm',
    'EXTENT': run_folder+'\\DSM_extent.shp',
    'HEIGHT': False,
    'IGNOREOVERLAP': False,
    'INPUT': run_folder+'\\veg_outside_b.las',
    'SHAPE': 0,
    'VERSION64': True,
    'OUTPUT': run_folder+'\\veg_outside_b_zmin2_5.las'
}
veg_outside_b_zmin2_5 = processing.run('fusion:clipdata', alg_params_veg_outside_b_zmin2_5)

# creates a CDSM.asc using fusion:canopy model
alg_params_cdsm = {
    'ADVANCED_MODIFIERS': '',
    'ASCII': True,
    'CELLSIZE': 1,
    'CLASS': '',
    'GROUND': run_folder+'\\DEM.dtm',
    'INPUT': run_folder+'\\ground_outside_b.las'+';'+run_folder+'\\veg_outside_b_zmin2_5.las',
    'MEDIAN': '',
    'SLOPE': False,
    'SMOOTH': '',
    'VERSION64': True,
    'XYUNITS': 0,
    'ZUNITS': 0,
    'OUTPUT': run_folder+'\\CDSM.asc'
}

CDSM = processing.run('fusion:canopymodel', alg_params_cdsm)  

# creates a CDSM.tif with CRS EPSG:28355
processing.run("gdal:translate", {'INPUT':'C:/Users/weedingb/Desktop/utas_solweig_run/CDSM.asc','TARGET_CRS':QgsCoordinateReferenceSystem('EPSG:28355'),'NODATA':None,'COPY_SUBDATASETS':False,'OPTIONS':'','EXTRA':'','DATA_TYPE':0,'OUTPUT':'C:/Users/weedingb/Desktop/utas_solweig_run/CDSM.tif'})

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
    'OUTPUT': run_folder+'\\buildings_buffered.shp'
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
    'INPUT': run_folder+'\\buildings_buffered.shp',
    'OUTPUT': run_folder+'\\buildings_buffered_zeros.shp'
}
buildings_buffered_zeros = processing.run('qgis:advancedpythonfieldcalculator', alg_params_buildings_buffered_zeros)

# creates a .tif from the buffered buildings shape file (with zero field) using gdal:rasterize
alg_params_buildings_buffered_raster = {
    'BURN': '',
    'DATA_TYPE': 5,
    'EXTENT': run_folder+'\\DSM_extent.shp',
    'EXTRA': '',
    'FIELD': 'zeros',
    'HEIGHT': 1,
    'INIT': 1,
    'INPUT': run_folder+'\\buildings_buffered_zeros.shp',
    'INVERT': False,
    'NODATA': None,
    'OPTIONS': '',
    'UNITS': 1,
    'WIDTH': 1,
    'OUTPUT': run_folder+'\\buildings_buffered_raster.tif'
}
buildings_buffered_raster = processing.run('gdal:rasterize', alg_params_buildings_buffered_raster)


#%% Filtered CDSM production

# multiply the buffered building raster with the CDSM using the command line, removing any vegetation present inside the buffered buildings
os.system('python %CONDA_PREFIX%\Scripts\gdal_calc.py --calc "A*B" --format GTiff --type Float32 -A C:/Users/weedingb/Desktop/utas_solweig_run/buildings_buffered_raster.tif --A_band 1 -B C:/Users/weedingb/Desktop/utas_solweig_run/CDSM.tif --outfile C:/Users/weedingb/Desktop/utas_solweig_run/CDSM_filt1.tif'
)
# eliminates small fluctuating elevations produced by the canopy model algorithm when normalised against the DEM.dtm
os.system('python %CONDA_PREFIX%\Scripts\gdal_calc.py --calc "(A>0.5)*A" --format GTiff --type Float32 -A C:/Users/weedingb/Desktop/utas_solweig_run/CDSM_filt1.tif --A_band 1 --outfile C:/Users/weedingb/Desktop/utas_solweig_run/CDSM_filt2.tif'
)
# assigns a projection to the filtered CDSM of EPSG:28355 using gdal:assignprojection
processing.run("gdal:assignprojection", {'INPUT':run_folder+'/CDSM_filt2.tif','CRS':'QgsCoordinateReferenceSystem("EPSG:28355")'})


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
        'PROJWIN':'526570.7875,526739.3125,5249794.0250,5249935.7750 [EPSG:28355]',
        'NODATA':None,
        'OPTIONS':'',
        'DATA_TYPE':0,
        'EXTRA':'',
        'OUTPUT':file_out})

# adds the clipped DEM to the clipped DSM    
os.system('python %CONDA_PREFIX%\Scripts\gdal_calc.py --calc "A+B" --format GTiff --type Float32 -A C:/Users/weedingb/Desktop/utas_solweig_run/DEM_clipped.tif --A_band 1 -B C:/Users/weedingb/Desktop/utas_solweig_run/DSM_clipped.tif --outfile C:/Users/weedingb/Desktop/utas_solweig_run/DSM_clipped_addDEM.tif'
)

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
                'INPUTMET':run_folder+'metfile_20190105_20190106_tester.txt',
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
                'OUTPUT_DIR':run_folder+'solweig_output'})

# finish time
tock_solweig = time.perf_counter()

# calculates run time
runtime_solweig = str(datetime.timedelta(seconds=tock_solweig-tick_solweig))



