# -*- coding: utf-8 -*-
"""
Created on Mon Mar 15 11:37:17 2021

@author: weedingb
"""

def laz2las(laz_in):
    
    import os
    import pylas
    import lazrs
    
    las_out = laz_in.replace('.laz','.las')
    
    las = pylas.read(laz_in)  
    
    las = pylas.convert(las)  
    
    las.write(las_out)
    
    