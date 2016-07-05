import os
import numpy as np
import numpy.ma as ma
import Ngl
import netCDF4
from pandas import Series, DataFrame
import pandas as pd
 
src_nc0 = netCDF4.Dataset('data/c.e13.C1DECO.T62_g37.INX.005.pop.TEMP.nday.0031.nc'       ,'r')
dst_nc0 = netCDF4.Dataset('data/c.e13.C1DECO.T62_g37.INX.005.pop.TEMPERATURE.nday.0031.nc','a')

dd = src_nc0.variables['time'][:]


tt = np.zeros(365)
for n in range(365):
  tt[n] = 12.0 + n * 24.0

dst_nc0.variables['time'][:]        = tt[:]
dst_nc0.variables['TEMPERATURE'][:] = src_nc0.variables['TEMP'][:]


src_nc0.close()
dst_nc0.close()

##### get data #####
#dep   = ma.ravel(src_nc0.variables["z_t"]) * 1.e-2
#lat   = ma.ravel(src_nc0.variables["TLAT"][:,:])
#lon   = ma.ravel(src_nc0.variables["TLONG"][:,:])
#var3d = ma.copy (src_nc0.variables["Fe"][0,:,:,:]) * 1.e3

##### check abnormal data #####
#x = var3d
#x[x ==  np.inf] = var3d.fill_value  # eliminate inf values
#x[x == -np.inf] = var3d.fill_value
#x = ma.masked_outside(x,0.0,2.0)    # eliminate data outside the bound
#x = ma.compressed(x)                # eliminate masked data and compressed in an array

#print DataFrame(x).describe()
#plt.hist(x,50,histtype='bar')
#print DataFrame(dep)


##### draw by pyngl #####
#wks = Ngl.open_wks("ps",psf)
#
#res0 = Ngl.Resources()
#
#res0.nglDraw               = False
#res0.nglFrame              = False
#
#plot = []
#
#res0.sfYArray = lat
#res0.sfXArray = lon
#
#res0.cnFillOn              = True
#res0.cnFillMode            = "RasterFill"
#res0.cnLinesOn             = False
#res0.cnLineLabelsOn        = False
#
#res0.cnLevelSelectionMode  = "ManualLevels"
#res0.cnMinLevelValF        = 0.0
#res0.cnMaxLevelValF        = 2.0
#res0.cnLevelSpacingF       = 0.1
#
#res0.mpGridAndLimbOn       = False
#
#res0.pmLabelBarDisplayMode = "Never"
#
#res0.lbLabelAutoStride     = True
#
#resT = Ngl.Resources()
#resT.txFontHeightF         = 0.02
#Ngl.text_ndc(wks,ttl,0.5,0.9,resT)
#
#for k in [0, 10, 26, 39]:
#  res0.tiMainString = str(dep[k]) + "m depth"
#  var = ma.ravel(var3d[k,:,:])
#  plot.append(Ngl.contour_map(wks,var,res0))
#
#
#resP = Ngl.Resources()
#resP.nglPanelLabelBar                 = True
#resP.nglPanelLabelBarLabelFontHeightF = 0.01
#resP.nglPanelLabelBarHeightF          = 0.10
#resP.nglPanelLabelBarWidthF           = 1.000
##resP.nglPanelFigureStrings            = ["a", "b", "c", "d"]
##resP.nglPanelFigureStringsJust        = "BottomRight"
#
#Ngl.panel(wks,plot[0:4],[2,2],resP)

##### output data into a netcdf file #####
#x = np.random.rand(1*60*116*110)
#x = x.reshape([1,60,116,100])
#dst_nc0.variables['TEMP'][:] = x[:]
# 

##### example of a cdl file. ##### 
#
# % ncgen -o hoge.nc hoge.cdl
#
#####
#netcdf sample data {
#dimensions:
#        time = UNLIMITED ; // (1 currently)
#        z_t = 60 ;
#        nlon = 100 ;
#        nlat = 116 ;
#variables:
#        float TEMP(time, z_t, nlat, nlon) ;
#                TEMP:long_name = "Potential Temperature" ;
#                TEMP:units = "degC" ;
#                TEMP:coordinates = "TLONG TLAT z_t time" ;
#                TEMP:grid_loc = "3111" ;
#                TEMP:cell_methods = "time: mean" ;
#                TEMP:_FillValue = 9.96921e+36f ;
#                TEMP:missing_value = 9.96921e+36f ;
#
#// global attributes:
#                :title = "c.e13.CECO.T62_g37.INX.001" ;
#}

