# -*- coding: utf-8 -*-
"""
Created on Mon Dec  7 16:26:44 2020

@author: weedingb
"""

import sys

from qgis.core import *

from qgis.gui import (
    QgsLayerTreeMapCanvasBridge,
)

from qgis import processing

from qgis.analysis import QgsNativeAlgorithms
	
import warnings

import pyplugin_installer


sys.path.append('C:\\Program Files\\QGIS 3.16\\apps\\qgis\\python\\plugins')

warnings.filterwarnings("ignore",category=DeprecationWarning)

QgsApplication.setPrefixPath('C:\\Program Files\\QGIS 3.16\\apps\\qgis\\python',True)

qgs = QgsApplication([], False)
qgs.initQgis()

pyplugin_installer.instance().fetchAvailablePlugins(False)

pyplugin_installer.instance().installFromZipFile('C:\\Users\\weedingb\\Desktop\\QGIS_processingtools_conda\\processing_umep-0.5.zip')

from processing.core.Processing import Processing
Processing.initialize()
QgsApplication.processingRegistry().addProvider(QgsNativeAlgorithms())
import processing

# loads buildings shape file - working in QGIS console
layer = QgsVectorLayer('C:\\Users\\weedingb\\Desktop\\LAS_fusion_processing\\list_2d_building_polys_hobart.shp', 'buildings', 'ogr')
 
# Add the layer to the map (comment the following line if the loading in the Layers Panel is not needed) - working in QGIS console
QgsProject.instance().addMapLayer(layer)

las_loc = 'C:\\Users\\weedingb\\Desktop\\LAS_fusion_processing\\ClimateFuturesDerwent2008-C2-AHD_5265250_55.las'

# DEM.dtm (grid surface create class 2)
alg_params = {
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
    'OUTPUT_DTM': QgsProcessing.TEMPORARY_OUTPUT
}
    
processing.run('fusion:gridsurfacecreate', alg_params)