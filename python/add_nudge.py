import os
import numpy as np
import numpy.ma as ma
import Ngl
import netCDF4
from pandas import Series, DataFrame
import pandas as pd
 
dst_nc0 = netCDF4.Dataset('/Users/misumi/roms_data/v1d_coag/v1d_clm_160629_append.nc','a')

dst_nc0.variables['temp_nudge'][0,:,:,:]   = 0.0
dst_nc0.variables['temp_nudge'][0,0:7,:,:] = 1.0
dst_nc0.variables['salt_nudge'][0,:,:,:]   = 0.0
dst_nc0.variables['salt_nudge'][0,0:7,:,:] = 1.0

dst_nc0.close()

##### print format #####
#print "%4.0f %4.0f -> %4.0f %4.0f" % (pstr, pend, rstr, rend)

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

##### draw by matplotlib #####
#fig0 = plt.figure()
#
#subplots_adjust(wspace=0.05)
#ax0 = fig0.add_subplot(131)
#ax1 = fig0.add_subplot(132,sharey=ax0)
#ax2 = fig0.add_subplot(133,sharey=ax0)
#
#ax0.grid(True)
#ax1.grid(True)
#ax2.grid(True)
#
#ax0.set_xlim(0.0, 3.5)
#ax1.set_xlim(0.0,50.0)
#ax2.set_xlim(0.0, 1.0)
#
#ax0.set_xticks(arange(0.0, 3.5, 0.5))
#ax1.set_xticks(arange(0.0,60.0,10.0))
#ax2.set_xticks(arange(0.0, 1.0, 0.2))
#
#plt.setp( ax1.get_yticklabels(), visible=False )
#plt.setp( ax2.get_yticklabels(), visible=False )
#
#ax0.set_xlabel("PO4 [uM]")
#ax0.set_ylabel("Depth [m]")
#ax1.set_xlabel("NO3 [uM]")
#ax2.set_xlabel("Fe  [nM]")
#
#ax0.plot(po4_0_z_a,z,color="black",label="POP" ,linewidth=2)
#ax0.plot(po4_1_z_a,z,color="red"  ,label="ROMS",linewidth=2)
#ax1.plot(no3_0_z_a,z,color="black",linewidth=2)
#ax1.plot(no3_1_z_a,z,color="red"  ,linewidth=2)
#ax2.plot(fe_0_z_a ,z,color="black",linewidth=2)
#ax2.plot(fe_1_z_a ,z,color="red"  ,linewidth=2)
#
#ax0.legend(loc="lower left")

#fig0.savefig('../psfiles/hogehoge.png',dpi=200)



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
#res0.mpCenterLonF          = -150
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


##### read fortran binary #####
#temp=np.fromfile('temp.bin',dtype='>f8',count=60*116*100)  # '>' represents big endian
#temp = a.reshape((60,116,100))

##### write fortran binary #####
#temp_d[:] = temp[:]
#temp_d.byteswap(True) # convert little to big endian
#for nday in range(1,366):
#  ddd = "%03i" % nday
#  temp_d[nday-1,:,:,:].tofile('data/c.e13.C1DECO.T62_g37.INX.005.pop.TEMP.nday.0031.ieeer8.0001.'+ddd+'.12')

