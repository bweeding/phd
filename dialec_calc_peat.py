# -*- coding: utf-8 -*-
"""
Created on Wed Jun  2 11:11:45 2021

@author: weedingb
"""

import pandas as pd
import numpy as np

df = pd.read_csv (r'C:\Users\weedingb\Desktop\GPR_peat_Melinda\allsoildataforR.csv')

df['SoilH20_m3m3'] = df['SoilH20']/100


coeffs_comb = np.flip(np.array([-1.89E-2,3.20E-2,-4.59E-4,2.70E-6]))
coeffs_M1 = np.flip(np.array([-4.89E-2,3.66E-2,-5.29E-4,2.84E-6]))
coeffs_M2 = np.flip(np.array([-9.25E-2,4.12E-2,-7.10E-4,4.76E-6]))
coeffs_M3 = np.flip(np.array([-9.50E-2,3.64E-2,-6.20E-4,4.78E-6]))
coeffs_M4 = np.flip(np.array([-4.30E-2,4.07E-2,-8.60E-4,6.93E-6]))
coeffs_L1 = np.flip(np.array([4.01E-2,1.52E-2,-1.29E-5,0]))
coeffs_L2 = np.flip(np.array([6.41E-2,3.17E-2,-6.46E-4,5.29E-6]))


def dia_perm_solver(soilh20,coeffs):
    
    if ~np.isnan(soilh20):
        q = np.poly1d([coeffs[0],coeffs[1],coeffs[2],coeffs[3]-soilh20])

        return q.r[np.isreal(q.r)].real[0]
    
    else:
        return np.nan
 

df['dia_perm_comb'] = df.apply(
    lambda row: dia_perm_solver(row['SoilH20_m3m3'],coeffs_comb),
    axis=1)

df['dia_perm_M1'] = df.apply(
    lambda row: dia_perm_solver(row['SoilH20_m3m3'],coeffs_M1),
    axis=1)

df['dia_perm_M2'] = df.apply(
    lambda row: dia_perm_solver(row['SoilH20_m3m3'],coeffs_M2),
    axis=1)

df['dia_perm_M3'] = df.apply(
    lambda row: dia_perm_solver(row['SoilH20_m3m3'],coeffs_M3),
    axis=1)

df['dia_perm_M4'] = df.apply(
    lambda row: dia_perm_solver(row['SoilH20_m3m3'],coeffs_M4),
    axis=1)

df['dia_perm_L1'] = df.apply(
    lambda row: dia_perm_solver(row['SoilH20_m3m3'],coeffs_L1),
    axis=1)

df['dia_perm_L2'] = df.apply(
    lambda row: dia_perm_solver(row['SoilH20_m3m3'],coeffs_L2),
    axis=1)

df.to_csv(r'C:\Users\weedingb\Desktop\GPR_peat_Melinda\dia_perm_data.csv')

##############################################################################
################################## Junkyard ##################################
##############################################################################

# df['comb'][0]=dia_perm_solver(df['SoilH20_m3m3'][0])

# df.loc[:,('comb')][~np.isnan(df['SoilH20'])]=dia_perm_solver(df.loc[(:,'SoilH20_m3m3')][~np.isnan(df['SoilH20'])])

# df['comb']
# for row_tuple in df[~np.isnan(df['SoilH20'])].itertuples():
#     q = np.poly1d([coeffs_comb[0],coeffs_comb[1],coeffs_comb[2],coeffs_comb[3]-row_tuple.SoilH20_m3m3])
#     #row_tuple.comb = q.r[np.isreal(q.r)].real[0]
#     print(q.r[np.isreal(q.r)].real[0])

# df.loc[:,('comb')][~np.isnan(df['SoilH20'])] = dia_perm_solver(df.loc[:,('SoilH20_m3m3')][~np.isnan(df['SoilH20'])])
