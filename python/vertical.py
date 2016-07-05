import os
import numpy as np
import numpy.ma as ma
import Ngl
import netCDF4
from pandas import Series, DataFrame
import pandas as pd
import pyroms

grd_s = pyroms.grid.get_ROMS_grid('v1d_grd')
grd_z = pyroms.grid.get_ROMS_grid('v1d_grd_z')

src_nc0 = netCDF4.Dataset('/Users/misumi/roms_out/ROMS_run/out/roms_run.a.001.nc','r')
src_nc1 = netCDF4.Dataset('/Users/misumi/roms_data/v1d_coag/v1d_clm_160616.nc','r')

var0_time = src_nc0.variables['ocean_time'][:]
var0_time = var0_time / 86400.0

tind = 0
cnt  = 0.0
b0   = ma.zeros(src_nc0.variables['temp'][0,:,:,:].shape)
b1   = ma.zeros(src_nc0.variables['temp'][0,:,:,:].shape)

for i in var0_time:
  if i > 10592.25:
#  if i < 365.25:
    print tind,i
    var0_s = src_nc0.variables['temp'][tind,:,:,:]
    var1_s = src_nc0.variables['salt'][tind,:,:,:]
    b0  = b0 + var0_s
    b1  = b1 + var1_s
    cnt = cnt + 1.0
  tind = tind + 1

var0_s = b0 / cnt
var1_s = b1 / cnt


clm0_s = src_nc1.variables['temp'][0,:,:,:]
clm1_s = src_nc1.variables['salt'][0,:,:,:]

miss = -999.9

var0_z = pyroms.remapping.roms2z(var0_s[:],grd_s,grd_z,spval=miss)
var1_z = pyroms.remapping.roms2z(var1_s[:],grd_s,grd_z,spval=miss)
clm0_z = pyroms.remapping.roms2z(clm0_s[:],grd_s,grd_z,spval=miss)
clm1_z = pyroms.remapping.roms2z(clm1_s[:],grd_s,grd_z,spval=miss)

dep    = grd_z.vgrid.z[:,0,0]

var0_z = ma.masked_where(var0_z[:,0,0]==miss,var0_z[:,0,0])
var1_z = ma.masked_where(var1_z[:,0,0]==miss,var1_z[:,0,0])
clm0_z = ma.masked_where(clm0_z[:,0,0]==miss,clm0_z[:,0,0])
clm1_z = ma.masked_where(clm1_z[:,0,0]==miss,clm1_z[:,0,0])

fig = plt.figure()
fig.suptitle("1 year")
ax0 = fig.add_subplot(121)
ax0.plot(var0_z,dep,'ro',label="Model")
ax0.plot(clm0_z,dep,'gx',label="Obs")
ax0.legend(loc='lower right')
ax1 = fig.add_subplot(122)
ax1.plot(var1_z,dep,'ro')
ax1.plot(clm1_z,dep,'gx')

src_nc0.close()


###



#dst_nc0 = netCDF4.Dataset('data/c.e13.C1DECO.T62_g37.INX.005.pop.TEMPERATURE.nday.0031.nc','a')
#
#dd = src_nc0.variables['time'][:]
#
#
#tt = np.zeros(365)
#for n in range(365):
#  tt[n] = 12.0 + n * 24.0
#
#dst_nc0.variables['time'][:]        = tt[:]
#dst_nc0.variables['TEMPERATURE'][:] = src_nc0.variables['TEMP'][:]
#
#
#src_nc0.close()
#dst_nc0.close()
#
###### get data #####
##dep   = ma.ravel(src_nc0.variables["z_t"]) * 1.e-2
##lat   = ma.ravel(src_nc0.variables["TLAT"][:,:])
##lon   = ma.ravel(src_nc0.variables["TLONG"][:,:])
##var3d = ma.copy (src_nc0.variables["Fe"][0,:,:,:]) * 1.e3
#
###### check abnormal data #####
##x = var3d
##x[x ==  np.inf] = var3d.fill_value  # eliminate inf values
##x[x == -np.inf] = var3d.fill_value
##x = ma.masked_outside(x,0.0,2.0)    # eliminate data outside the bound
##x = ma.compressed(x)                # eliminate masked data and compressed in an array
#
##print DataFrame(x).describe()
##plt.hist(x,50,histtype='bar')
##print DataFrame(dep)
#
#
###### draw by pyngl #####
##wks = Ngl.open_wks("ps",psf)
##
##res0 = Ngl.Resources()
##
##res0.nglDraw               = False
##res0.nglFrame              = False
##
##plot = []
##
##res0.sfYArray = lat
##res0.sfXArray = lon
##
##res0.cnFillOn              = True
##res0.cnFillMode            = "RasterFill"
##res0.cnLinesOn             = False
##res0.cnLineLabelsOn        = False
##
##res0.cnLevelSelectionMode  = "ManualLevels"
##res0.cnMinLevelValF        = 0.0
##res0.cnMaxLevelValF        = 2.0
##res0.cnLevelSpacingF       = 0.1
##
##res0.mpGridAndLimbOn       = False
##
##res0.pmLabelBarDisplayMode = "Never"
##
##res0.lbLabelAutoStride     = True
##
##resT = Ngl.Resources()
##resT.txFontHeightF         = 0.02
##Ngl.text_ndc(wks,ttl,0.5,0.9,resT)
##
##for k in [0, 10, 26, 39]:
##  res0.tiMainString = str(dep[k]) + "m depth"
##  var = ma.ravel(var3d[k,:,:])
##  plot.append(Ngl.contour_map(wks,var,res0))
##
##
##resP = Ngl.Resources()
##resP.nglPanelLabelBar                 = True
##resP.nglPanelLabelBarLabelFontHeightF = 0.01
##resP.nglPanelLabelBarHeightF          = 0.10
##resP.nglPanelLabelBarWidthF           = 1.000
###resP.nglPanelFigureStrings            = ["a", "b", "c", "d"]
###resP.nglPanelFigureStringsJust        = "BottomRight"
##
##Ngl.panel(wks,plot[0:4],[2,2],resP)
#
###### output data into a netcdf file #####
##x = np.random.rand(1*60*116*110)
##x = x.reshape([1,60,116,100])
##dst_nc0.variables['TEMP'][:] = x[:]
## 
#
###### example of a cdl file. ##### 
##
## % ncgen -o hoge.nc hoge.cdl
##
######
##netcdf sample data {
##dimensions:
##        time = UNLIMITED ; // (1 currently)
##        z_t = 60 ;
##        nlon = 100 ;
##        nlat = 116 ;
##variables:
##        float TEMP(time, z_t, nlat, nlon) ;
##                TEMP:long_name = "Potential Temperature" ;
##                TEMP:units = "degC" ;
##                TEMP:coordinates = "TLONG TLAT z_t time" ;
##                TEMP:grid_loc = "3111" ;
##                TEMP:cell_methods = "time: mean" ;
##                TEMP:_FillValue = 9.96921e+36f ;
##                TEMP:missing_value = 9.96921e+36f ;
##
##// global attributes:
##                :title = "c.e13.CECO.T62_g37.INX.001" ;
##}
#
