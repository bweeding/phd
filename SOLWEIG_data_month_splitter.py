# -*- coding: utf-8 -*-
"""
Created on Wed Jun  9 09:20:14 2021

@author: weedingb
"""

import os
import shutil
import datetime


def monthly_splitter(base_folder):
    
    source_folder = base_folder+'\\SOLWEIG_output_'+base_folder[-15::]
    
    months = ['Jan','Feb','Mar','Apr','May','Jun','Jul','Aug','Sep','Oct','Nov','Dec']
    
    os.mkdir(base_folder+'\\monthly_data')
    
    for cur_month in months:

        os.mkdir(base_folder+'\\monthly_data\\'+cur_month)
    
    for folders, subfolders, filenames in os.walk(source_folder):
        
        for filename in filenames:

            try:
            
                filemonth = datetime.datetime.strptime(filename.split('_')[1]+' '+filename.split('_')[2],'%Y %j').strftime('%b')
                    
                shutil.copy(os.path.join(folders, filename), base_folder+'\\monthly_data\\'+filemonth)
                
            except IndexError:
                
                pass