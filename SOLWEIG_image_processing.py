# -*- coding: utf-8 -*-
"""
Created on Thu Dec 17 13:44:21 2020

@author: weedingb
"""

import gdal

options_list = [
    '-ot Byte',
    '-of JPEG',
    '-b 1',
    '-colorinterp red',
    '-scale'
]           

options_string = " ".join(options_list)
    
gdal.Translate(
    'C:\\Users\\weedingb\\Desktop\\LAS_fusion_processing\\SOLWEIG_output\\Tmrt_average3.jpeg',
    'C:\\Users\\weedingb\\Desktop\\LAS_fusion_processing\\SOLWEIG_output\\Tmrt_average.tif',
    options=options_string
)