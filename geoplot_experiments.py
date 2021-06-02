# -*- coding: utf-8 -*-
"""
Created on Wed May 19 12:14:59 2021

@author: weedingb
"""
import numpy as np
import plotly.express as px
import plotly.io as pio
import geopandas as gpd
import itertools

pio.renderers.default='browser'

import plotly.graph_objects as go

import pandas as pd



lats=np.array([-46.      , -45.9865  , -45.973   , -45.9595  ,
                   -45.946   , -45.9325  , -45.919   , -45.9055  ,
                   -45.892   , -45.8785  , -45.865   , -45.8515  ,
                   -45.838   , -45.8245  , -45.811   , -45.7975  ,
                   -45.784   , -45.7705  , -45.757   , -45.7435  ,
                   -45.73    , -45.7165  , -45.703   , -45.6895  ,
                   -45.676   , -45.6625  , -45.649   , -45.6355  ,
                   -45.622   , -45.6085  , -45.595   , -45.5815  ,
                   -45.568   , -45.5545  , -45.541   , -45.5275  ,
                   -45.514   , -45.5005  , -45.487   , -45.4735  ,
                   -45.46    , -45.4465  , -45.433   , -45.4195  ,
                   -45.406   , -45.3925  , -45.379   , -45.3655  ,
                   -45.352   , -45.3385  , -45.325   , -45.3115  ,
                   -45.298   , -45.2845  , -45.271   , -45.2575  ,
                   -45.244   , -45.2305  , -45.217   , -45.2035  ,
                   -45.19    , -45.1765  , -45.163   , -45.1495  ,
                   -45.136   , -45.1225  , -45.109   , -45.0955  ,
                   -45.082   , -45.0685  , -45.055   , -45.0415  ,
                   -45.028   , -45.0145  , -45.001   , -44.9875  ,
                   -44.974   , -44.9605  , -44.947   , -44.9335  ,
                   -44.92    , -44.9065  , -44.893   , -44.8795  ,
                   -44.866   , -44.8525  , -44.839   , -44.8255  ,
                   -44.812   , -44.7985  , -44.785   , -44.7715  ,
                   -44.758   , -44.7445  , -44.731   , -44.7175  ,
                   -44.704   , -44.6905  , -44.677   , -44.6635  ,
                   -44.65    , -44.6365  , -44.623   , -44.6095  ,
                   -44.596   , -44.5825  , -44.569   , -44.5555  ,
                   -44.542   , -44.5285  , -44.515   , -44.5015  ,
                   -44.488   , -44.4745  , -44.461   , -44.4475  ,
                   -44.434   , -44.4205  , -44.407   , -44.3935  ,
                   -44.38    , -44.3665  , -44.353   , -44.3395  ,
                   -44.326   , -44.3125  , -44.299   , -44.2855  ,
                   -44.272   , -44.2585  , -44.245   , -44.2315  ,
                   -44.218   , -44.2045  , -44.191   , -44.1775  ,
                   -44.164   , -44.1505  , -44.137   , -44.1235  ,
                   -44.11    , -44.0965  , -44.083   , -44.0695  ,
                   -44.056   , -44.0425  , -44.029   , -44.0155  ,
                   -44.002   , -43.9885  , -43.975   , -43.9615  ,
                   -43.947998, -43.9345  , -43.921   , -43.9075  ,
                   -43.894   , -43.8805  , -43.867   , -43.8535  ,
                   -43.84    , -43.8265  , -43.813   , -43.7995  ,
                   -43.786   , -43.7725  , -43.759   , -43.7455  ,
                   -43.732   , -43.7185  , -43.705   , -43.6915  ,
                   -43.678   , -43.6645  , -43.651   , -43.6375  ,
                   -43.624   , -43.6105  , -43.597   , -43.5835  ,
                   -43.57    , -43.5565  , -43.543   , -43.5295  ,
                   -43.516   , -43.5025  , -43.489   , -43.4755  ,
                   -43.461998, -43.4485  , -43.435   , -43.4215  ,
                   -43.408   , -43.3945  , -43.381   , -43.3675  ,
                   -43.354   , -43.3405  , -43.327   , -43.3135  ,
                   -43.3     , -43.2865  , -43.273   , -43.2595  ,
                   -43.246   , -43.2325  , -43.219   , -43.2055  ,
                   -43.192   , -43.1785  , -43.165   , -43.1515  ,
                   -43.138   , -43.1245  , -43.111   , -43.0975  ,
                   -43.084   , -43.0705  , -43.057   , -43.0435  ,
                   -43.03    , -43.0165  , -43.003   , -42.9895  ,
                   -42.975998, -42.9625  , -42.949   , -42.9355  ,
                   -42.922   , -42.9085  , -42.895   , -42.8815  ,
                   -42.868   , -42.8545  , -42.841   , -42.8275  ,
                   -42.814   , -42.8005  , -42.787   , -42.7735  ,
                   -42.76    , -42.7465  , -42.733   , -42.7195  ,
                   -42.706   , -42.6925  , -42.679   , -42.6655  ,
                   -42.652   , -42.6385  , -42.625   , -42.6115  ,
                   -42.598   , -42.5845  , -42.571   , -42.5575  ,
                   -42.544   , -42.5305  , -42.517   , -42.5035  ,
                   -42.49    , -42.4765  , -42.463   , -42.4495  ,
                   -42.436   , -42.4225  , -42.409   , -42.3955  ,
                   -42.382   , -42.3685  , -42.355   , -42.3415  ,
                   -42.328   , -42.3145  , -42.301   , -42.2875  ,
                   -42.274   , -42.260498, -42.247   , -42.2335  ,
                   -42.22    , -42.2065  , -42.193   , -42.1795  ,
                   -42.166   , -42.1525  , -42.139   , -42.1255  ,
                   -42.112   , -42.0985  , -42.085   , -42.0715  ,
                   -42.058   , -42.0445  , -42.031   , -42.0175  ,
                   -42.004   , -41.9905  , -41.977   , -41.9635  ,
                   -41.95    , -41.9365  , -41.923   , -41.9095  ,
                   -41.896   , -41.8825  , -41.869   , -41.8555  ,
                   -41.842   , -41.8285  , -41.815   , -41.8015  ,
                   -41.788002, -41.774498, -41.761   , -41.7475  ,
                   -41.734   , -41.7205  , -41.707   , -41.6935  ,
                   -41.68    , -41.6665  , -41.653   , -41.6395  ,
                   -41.626   , -41.6125  , -41.599   , -41.5855  ,
                   -41.572   , -41.5585  , -41.545   , -41.5315  ,
                   -41.517998, -41.5045  , -41.491   , -41.4775  ,
                   -41.464   , -41.4505  , -41.437   , -41.4235  ,
                   -41.41    , -41.3965  , -41.383   , -41.3695  ,
                   -41.356   , -41.3425  , -41.329   , -41.3155  ,
                   -41.302002, -41.288498, -41.275   , -41.2615  ,
                   -41.248   , -41.2345  , -41.221   , -41.2075  ,
                   -41.194   , -41.1805  , -41.167   , -41.1535  ,
                   -41.14    , -41.1265  , -41.113   , -41.0995  ,
                   -41.086   , -41.0725  , -41.059   , -41.0455  ,
                   -41.032   , -41.0185  , -41.005   , -40.9915  ,
                   -40.978   , -40.9645  , -40.951   , -40.9375  ,
                   -40.924   , -40.9105  , -40.897   , -40.8835  ,
                   -40.87    , -40.8565  , -40.843   , -40.8295  ,
                   -40.816   , -40.802498, -40.789   , -40.7755  ,
                   -40.762   , -40.7485  , -40.735   , -40.7215  ,
                   -40.708   , -40.6945  , -40.681   , -40.6675  ,
                   -40.654   , -40.6405  , -40.627   , -40.6135  ,
                   -40.6     , -40.5865  , -40.572998, -40.5595  ,
                   -40.546   , -40.5325  , -40.519   , -40.5055  ,
                   -40.492   , -40.4785  , -40.465   , -40.4515  ,
                   -40.438   , -40.4245  , -40.411   , -40.3975  ,
                   -40.384   , -40.3705  , -40.357   , -40.3435  ,
                   -40.33    , -40.316498, -40.303   , -40.2895  ,
                   -40.276   , -40.2625  , -40.249   , -40.2355  ,
                   -40.222   , -40.2085  , -40.195   , -40.1815  ,
                   -40.168   , -40.1545  , -40.141   , -40.1275  ,
                   -40.114   , -40.1005  , -40.086998, -40.0735  ,
                   -40.06    , -40.0465  , -40.033   , -40.0195  ,
                   -40.006   , -39.9925  , -39.979   , -39.9655  ,
                   -39.952   , -39.9385  , -39.925   , -39.9115  ,
                   -39.898   , -39.8845  , -39.871   , -39.8575  ,
                   -39.844   , -39.830498, -39.817   , -39.8035  ,
                   -39.79    , -39.7765  , -39.763   , -39.7495  ,
                   -39.736   , -39.7225  , -39.709   , -39.6955  ,
                   -39.682   , -39.6685  , -39.655   , -39.6415  ,
                   -39.628   , -39.614502, -39.600998, -39.5875  ,
                   -39.574   , -39.5605  , -39.547   , -39.5335  ,
                   -39.52    , -39.5065  , -39.493   , -39.4795  ,
                   -39.466   , -39.4525  , -39.439   , -39.4255  ,
                   -39.412   , -39.3985  , -39.385   , -39.3715  ,
                   -39.358   , -39.3445  , -39.331   , -39.3175  ,
                   -39.304   , -39.2905  , -39.277   , -39.2635  ,
                   -39.25    , -39.2365  , -39.223   , -39.2095  ,
                   -39.196   , -39.1825  , -39.169   , -39.1555  ])

lons = np.array([142.5005 , 142.514  , 142.5275 , 142.541  , 142.5545 ,

                 

                
                   142.56801, 142.5815 , 142.595  , 142.6085 , 142.62201,
                   142.6355 , 142.649  , 142.6625 , 142.67601, 142.6895 ,
                   142.703  , 142.7165 , 142.73001, 142.7435 , 142.757  ,
                   142.77051, 142.784  , 142.7975 , 142.811  , 142.82451,
                   142.838  , 142.8515 , 142.865  , 142.87851, 142.892  ,
                   142.9055 , 142.919  , 142.93251, 142.946  , 142.9595 ,
                   142.973  , 142.9865 , 143.     , 143.0135 , 143.02701,
                   143.0405 , 143.054  , 143.0675 , 143.08101, 143.0945 ,
                   143.108  , 143.1215 , 143.13501, 143.1485 , 143.162  ,
                   143.1755 , 143.18901, 143.2025 , 143.216  , 143.2295 ,
                   143.243  , 143.2565 , 143.27   , 143.28351, 143.297  ,
                   143.3105 , 143.324  , 143.33751, 143.351  , 143.3645 ,
                   143.378  , 143.39151, 143.405  , 143.4185 , 143.432  ,
                   143.44551, 143.459  , 143.4725 , 143.48601, 143.4995 ,
                   143.513  , 143.5265 , 143.54001, 143.5535 , 143.567  ,
                   143.5805 , 143.59401, 143.6075 , 143.621  , 143.6345 ,
                   143.64801, 143.6615 , 143.675  , 143.6885 , 143.70201,
                   143.7155 , 143.729  , 143.74251, 143.756  , 143.7695 ,
                   143.783  , 143.79651, 143.81   , 143.8235 , 143.837  ,
                   143.85051, 143.864  , 143.8775 , 143.891  , 143.90451,
                   143.918  , 143.9315 , 143.945  , 143.9585 , 143.972  ,
                   143.9855 , 143.99901, 144.0125 , 144.026  , 144.0395 ,
                   144.05301, 144.0665 , 144.08   , 144.0935 , 144.10701,
                   144.1205 , 144.134  , 144.1475 , 144.16101, 144.1745 ,
                   144.188  , 144.2015 , 144.215  , 144.2285 , 144.242  ,
                   144.25551, 144.269  , 144.2825 , 144.296  , 144.30951,
                   144.323  , 144.3365 , 144.35   , 144.36351, 144.377  ,
                   144.3905 , 144.404  , 144.41751, 144.431  , 144.4445 ,
                   144.45801, 144.4715 , 144.485  , 144.4985 , 144.51201,
                   144.5255 , 144.539  , 144.5525 , 144.56601, 144.5795 ,
                   144.593  , 144.6065 , 144.62001, 144.6335 , 144.647  ,
                   144.6605 , 144.67401, 144.6875 , 144.701  , 144.71451,
                   144.728  , 144.7415 , 144.755  , 144.76851, 144.782  ,
                   144.7955 , 144.809  , 144.82251, 144.836  , 144.8495 ,
                   144.863  , 144.87651, 144.89   , 144.9035 , 144.917  ,
                   144.9305 , 144.944  , 144.9575 , 144.97101, 144.9845 ,
                   144.998  , 145.0115 , 145.02501, 145.0385 , 145.052  ,
                   145.0655 , 145.07901, 145.0925 , 145.106  , 145.1195 ,
                   145.13301, 145.1465 , 145.16   , 145.17351, 145.187  ,
                   145.2005 , 145.214  , 145.22751, 145.241  , 145.2545 ,
                   145.268  , 145.28151, 145.295  , 145.3085 , 145.322  ,
                   145.33551, 145.349  , 145.3625 , 145.376  , 145.38951,
                   145.403  , 145.4165 , 145.43001, 145.4435 , 145.457  ,
                   145.4705 , 145.48401, 145.4975 , 145.511  , 145.5245 ,
                   145.53801, 145.5515 , 145.565  , 145.5785 , 145.59201,
                   145.6055 , 145.619  , 145.6325 , 145.646  , 145.6595 ,
                   145.673  , 145.68651, 145.7    , 145.7135 , 145.727  ,
                   145.74051, 145.754  , 145.7675 , 145.781  , 145.79451,
                   145.808  , 145.8215 , 145.835  , 145.84851, 145.862  ,
                   145.8755 , 145.889  , 145.9025 , 145.916  , 145.9295 ,
                   145.94301, 145.9565 , 145.97   , 145.9835 , 145.99701,
                   146.0105 , 146.024  , 146.0375 , 146.05101, 146.0645 ,
                   146.078  , 146.0915 , 146.10501, 146.1185 , 146.132  ,
                   146.14551, 146.159  , 146.1725 , 146.186  , 146.19951,
                   146.213  , 146.2265 , 146.24   , 146.25351, 146.267  ,
                   146.2805 , 146.294  , 146.30751, 146.321  , 146.3345 ,
                   146.348  , 146.36151, 146.375  , 146.3885 , 146.40201,
                   146.4155 , 146.429  , 146.4425 , 146.45601, 146.4695 ,
                   146.483  , 146.4965 , 146.51001, 146.5235 , 146.537  ,
                   146.5505 , 146.56401, 146.5775 , 146.591  , 146.6045 ,
                   146.61801, 146.6315 , 146.645  , 146.65851, 146.672  ,
                   146.6855 , 146.699  , 146.71251, 146.726  , 146.7395 ,
                   146.753  , 146.76651, 146.78   , 146.7935 , 146.807  ,
                   146.82051, 146.834  , 146.8475 , 146.86101, 146.8745 ,
                   146.888  , 146.9015 , 146.91501, 146.9285 , 146.942  ,
                   146.9555 , 146.96901, 146.9825 , 146.996  , 147.0095 ,
                   147.02301, 147.0365 , 147.05   , 147.0635 , 147.077  ,
                   147.0905 , 147.104  , 147.11751, 147.131  , 147.1445 ,
                   147.158  , 147.17151, 147.185  , 147.1985 , 147.212  ,
                   147.22551, 147.239  , 147.2525 , 147.266  , 147.27951,
                   147.293  , 147.3065 , 147.32   , 147.3335 , 147.347  ,
                   147.3605 , 147.37401, 147.3875 , 147.401  , 147.4145 ,
                   147.42801, 147.4415 , 147.455  , 147.4685 , 147.48201,
                   147.4955 , 147.509  , 147.5225 , 147.53601, 147.5495 ,
                   147.563  , 147.5765 , 147.59   , 147.6035 , 147.617  ,
                   147.63051, 147.644  , 147.6575 , 147.671  , 147.68451,
                   147.698  , 147.7115 , 147.725  , 147.73851, 147.752  ,
                   147.7655 , 147.779  , 147.79251, 147.806  , 147.8195 ,
                   147.83301, 147.8465 , 147.86   , 147.8735 , 147.88701,
                   147.9005 , 147.914  , 147.9275 , 147.94101, 147.9545 ,
                   147.968  , 147.9815 , 147.99501, 148.0085 , 148.022  ,
                   148.0355 , 148.04901, 148.0625 , 148.076  , 148.08951,
                   148.103  , 148.1165 , 148.13   , 148.14351, 148.157  ,
                   148.1705 , 148.184  , 148.19751, 148.211  , 148.2245 ,
                   148.238  , 148.25151, 148.265  , 148.2785 , 148.292  ,
                   148.30551, 148.319  , 148.3325 , 148.34601, 148.3595 ,
                   148.373  , 148.3865 , 148.40001, 148.4135 , 148.427  ,
                   148.4405 , 148.45401, 148.4675 , 148.481  , 148.4945 ,
                   148.50801, 148.5215 , 148.535  , 148.54851, 148.562  ,
                   148.5755 , 148.589  , 148.60251, 148.616  , 148.6295 ,
                   148.643  , 148.65651, 148.67   , 148.6835 , 148.697  ,
                   148.71051, 148.724  , 148.7375 , 148.751  , 148.7645 ,
                   148.778  , 148.7915 , 148.80501, 148.8185 , 148.832  ,
                   148.8455 , 148.85901, 148.8725 , 148.886  , 148.8995 ,
                   148.91301, 148.9265 , 148.94   , 148.9535 , 148.96701,
                   148.9805 , 148.994  , 149.0075 , 149.021  , 149.0345 ,
                   149.048  , 149.06151, 149.075  , 149.0885 , 149.102  ,
                   149.11551, 149.129  , 149.1425 , 149.156  , 149.16951,
                   149.183  , 149.1965 , 149.21   , 149.22351, 149.237  ,
                   149.2505 , 149.264  , 149.2775 , 149.291  , 149.3045 ,
                   149.31801, 149.3315 , 149.345  , 149.3585 , 149.37201,
                   149.3855 , 149.399  , 149.4125 , 149.42601, 149.4395 ,
                   149.453  , 149.4665 , 149.48001, 149.4935 , 149.507  ,
                   149.52051, 149.534  , 149.5475 , 149.561  , 149.57451,
                   149.588  , 149.6015 , 149.615  , 149.62851, 149.642  ,
                   149.6555 , 149.669  , 149.68251, 149.696  , 149.7095 ,
                   149.723  , 149.73651, 149.75   , 149.7635 , 149.77701,
                   149.7905 , 149.804  , 149.8175 , 149.83101, 149.8445 ,
                   149.858  , 149.8715 , 149.88501, 149.8985 , 149.912  ,
                   149.9255 , 149.93901, 149.9525 , 149.966  , 149.9795 ,
                   149.99301, 150.0065 , 150.02   , 150.03351, 150.047  ,
                   150.0605 , 150.074  , 150.08751, 150.101  , 150.1145 ,
                   150.128  , 150.14151, 150.155  , 150.1685 , 150.182  ,
                   150.19551, 150.209  , 150.2225 , 150.23601, 150.2495 ,
                   150.263  , 150.2765 , 150.29001, 150.3035 , 150.317  ,
                   150.3305 , 150.34401, 150.3575 , 150.371  , 150.3845 ,
                   150.39801, 150.4115 , 150.425  , 150.4385 , 150.45201,
                   150.4655 , 150.479  , 150.49251, 150.506  ])

lats_into_df = []
lons_into_df = []

for i in lats:
    for j in lons:
        lats_into_df.append(i)
        lons_into_df.append(j)

lldf = pd.DataFrame(zip(lats_into_df,lons_into_df),columns=['lats','lons'])

fig = go.Figure(data=go.Scattergeo(
        lon = lldf['lons'][0:1000],
        lat = lldf['lats'][0:1000],
        #mode = 'markers',
        ))

# fig.update_layout(
#         title = 'Most trafficked US airports<br>(Hover for airport names)',
#         geo_scope='usa',
#     )
fig.show()



lldf2=lldf[(lldf['lats']>=-42.925)&(lldf['lats']<=-42.77)&(lldf['lons']>=147.225)&(lldf['lons']<=147.44)]


import plotly.graph_objects as go


import pandas as pd

import plotly.express as px

fig = px.scatter_mapbox(lldf2, lat="lats", lon="lons",
                        color_discrete_sequence=["red"], zoom=3, height=500)
fig.update_layout(mapbox_style="open-street-map")
fig.update_layout(margin={"r":0,"t":0,"l":0,"b":0})
fig.show()
