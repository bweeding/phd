import sys

# sets home folder location
home_folder = 'C:\\Users\\weedingb\\Desktop\\LAS_fusion_processing'

################################################################################
# Do this later, polyclipdata won't run if the shape file is loaded!?!?

# loads the building shape file
#building_layer = QgsVectorLayer(home_folder+'\\list_2d_building_polys_hobart.shp', 'buildings', 'ogr')

# adds the building shapefile as a layer
#QgsProject.instance().addMapLayer(building_layer)

################################################################################

# specifies the location of the current las file and buildings file
las_loc = home_folder+'\\ClimateFuturesDerwent2008-C2-AHD_5265250_55.las'

build_loc = home_folder+'\\list_2d_building_polys_hobart.shp'

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

################################################################################
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

################################################################################

# DSM
alg_params_dsm = {
    'ADVANCED_MODIFIERS': '',
    'ASCII': True,
    'CELLSIZE': 1,
    'CLASS': '',
    'GROUND': '',
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
    
################################################################################

# Convert extent of DSM to a shapefile
alg_params_extent = {
    'INPUT':home_folder+'\\DSM.asc',
    'OUTPUT':home_folder+'\\DSM_extent.shp'
}

extent = processing.run('native:polygonfromlayerextent',alg_params_extent)

# extract vegetation above 2.5m
alg_params_veg_outside_b_zmin2_5 = {
    'ADVANCED_MODIFIERS': '',
    'CLASS': '',
    'DTM': home_folder+'\\DEM.dtm',
    'EXTENT': home_folder+'\\DSM_extent.shp',
    'HEIGHT': False,
    'IGNOREOVERLAP': False,
    'INPUT': home_folder+'\\veg_outside_b.las',
    'SHAPE': 0,
    'VERSION64': True,
    'OUTPUT': home_folder+'\\veg_outside_b_zmin2_5.las'
}
veg_outside_b_zmin2_5 = processing.run('fusion:clipdata', alg_params_veg_outside_b_zmin2_5)

# CDSM
alg_params_cdsm = {
    'ADVANCED_MODIFIERS': '',
    'ASCII': True,
    'CELLSIZE': 1,
    'CLASS': '',
    'GROUND': '',
    'INPUT': home_folder+'\\ground_outside_b.las'+';'+home_folder+'\\veg_outside_b_zmin2_5.las',
    'MEDIAN': '',
    'SLOPE': False,
    'SMOOTH': '',
    'VERSION64': True,
    'XYUNITS': 0,
    'ZUNITS': 0,
    'OUTPUT': home_folder+'\\CDSM.asc'
}
CDSM = processing.run('fusion:canopymodel', alg_params_cdsm)  

################################################################################

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



















    
    
    
    
    
    
    
    
    
    
    