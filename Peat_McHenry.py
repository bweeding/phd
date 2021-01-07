# -*- coding: utf-8 -*-
"""
Created on Thu Jan  7 11:05:02 2021

@author: weedingb
"""

from sympy.solvers import solve
from sympy import Symbol
import numpy as np
import pandas as pd
import os

os.chdir('C:/Users/weedingb/Desktop/GPR peat project - Cam and Melinda')

peat_data = pd.read_csv('C:/Users/weedingb/Desktop/GPR peat project - Cam and Melinda/Depth.csv')

x = Symbol('x')

#solve(x**2+x-10,x)

# coefficients from Nagare et al. 2011 "Laboratory calibration of time domain reflectometry to determine moisture content in undisturbed peat samples"
bc= np.array([-1.89E-2,3.2E-2,-4.59E-4,2.7E-6])
bM1 = np.array([-4.89E-2,3.66E-2,-5.29E-4,2.84E-6])
bM2 = np.array([-9.25E-2,4.12E-2,-7.1E-4,4.76E-6])
bM3 = np.array([-9.5E-2,3.64E-2,-6.2E-4,4.78E-6])
bM4 = np.array([-4.3E-2,4.07E-2,-8.6E-4,6.93E-6])
bL1 = np.array([4.01E-2,1.52E-2,-1.29E-5,0])
bL2 = np.array([6.41E-2,3.17E-2,-6.46E-4,5.29E-6])

poly_fits = [bc,bM1,bM2,bM3,bM4,bL1,bL2]

solve(b[0]+b[1]*x+b[2]*x**2+b[3]*x**3-0.5)[0]


solve(poly_fits[0][0]+poly_fits[0][1]*x+poly_fits[0][2]*x**2+poly_fits[0][3]*x**3-peat_data['VMC'])[0]
   









