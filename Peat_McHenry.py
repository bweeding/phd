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
import matplotlib.pyplot as plt

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

coeff_data = {'comb':[-1.89E-2,3.2E-2,-4.59E-4,2.7E-6],
              'M1':[-4.89E-2,3.66E-2,-5.29E-4,2.84E-6],
              'M2':[-9.25E-2,4.12E-2,-7.1E-4,4.76E-6],
              'M3':[-9.5E-2,3.64E-2,-6.2E-4,4.78E-6],
              'M4':[-4.3E-2,4.07E-2,-8.6E-4,6.93E-6],
              'L1':[4.01E-2,1.52E-2,-1.29E-5,0],
              'L2':[6.41E-2,3.17E-2,-6.46E-4,5.29E-6],
    }

coeffs = pd.DataFrame(coeff_data)

perms = pd.DataFrame(columns = coeffs.columns)

for i in coeffs.columns:
    
    perms[i] = [solve(coeffs[i][0]+coeffs[i][1]*x+coeffs[i][2]*x**2+coeffs[i][3]*x**3-VMC)[0] for VMC in peat_data['VMC']]


poly_fits = [bc,bM1,bM2,bM3,bM4,bL1,bL2]

pf_idx = 0
#solve(b[0]+b[1]*x+b[2]*x**2+b[3]*x**3-0.5)[0]

permittivity = [solve(poly_fits[pf_idx][0]+poly_fits[pf_idx][1]*x+poly_fits[pf_idx][2]*x**2+poly_fits[pf_idx][3]*x**3-VMC)[0] for VMC in peat_data['VMC']]
 



# exporting
  
#peat_data['permittivity'] = permittivity


# export met_df to spaced separated text file for use in UMEP, named with start and end dates
#peat_data.to_csv('C:/Users/weedingb/Desktop/GPR peat project - Cam and Melinda/Depth_with_permittivity.csv',index=False)


# plotting

fig, ax = plt.subplots()
for color in ['comb', 'M1','M2','M3','M4','L1','L2']:
    ax.scatter(np.array(perms[color]), np.array(peat_data['VMC']), label=color,
               alpha=0.5, edgecolors='none')

ax.legend(loc='lower right')

ax.set_xlabel('Dielectric permittivity')
ax.set_ylabel('Volumetric water content')
ax.set_title('Peat soil permittivity')

ax.grid(True)

plt.show()






