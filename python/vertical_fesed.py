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

src_nc0 = netCDF4.Dataset('/Users/misumi/tower/Roms_work/data/fesedflux_gx1v6_etopo2v2_Dec2012.nc','r')
dst_nc0 = netCDF4.Dataset('/Users/misumi/roms_data/v1d_coag/v1d_fesed_160701.nc','a')

ny, nx, = grd_s.hgrid.mask.shape
ns,     = grd_s.vgrid.z_r.s_rho.shape
nz      = grd_z.vgrid.N

sed_pop_1 = ma.zeros((nz,1,1))
sed_pop_1[:,0,0] = src_nc0.variables['FESEDFLUXIN'][::-1,311,162] # definition of z is opposite between POP and gridid.txt.

dep = grd_z.vgrid.z[:,0,0]

sed_pop = ma.zeros((nz,nx,ny))
sed_pop = sed_pop + sed_pop_1

miss = -999.9
sed_roms = pyroms.remapping.z2roms(sed_pop,grd_z,grd_s,spval=miss)

sed_pop  = ma.masked_where(sed_pop  < 1.e-30,sed_pop)
sed_roms = ma.masked_where(sed_roms < 1.e-30,sed_roms)

s = grd_s.vgrid.s_rho
#s = grd_s.vgrid.z_r[0,:][:,0,0] 

fig = plt.figure()

ax0 = fig.add_subplot(121)
ax0.set_title('POP',fontsize=16)
ax0.set_xscale('log')
ax0.set_xlim(1.e-3,1.e1)
ax0.set_ylim(-1500.0,0.0)
ax0.xaxis.grid(True,'major')
ax0.yaxis.grid(True,'major')
ax0.set_xlabel(r"FeSed [$\mu$mol m$^{-2}$ day$^{-1}$]",fontsize=16)
ax0.set_ylabel("Depth [m]",fontsize=16)
ax0.plot(sed_pop[:,0,0],dep[:],'ro')

ax1 = fig.add_subplot(122)
ax1.set_title('ROMS',fontsize=16)
ax1.set_xscale('log')
#ax1.set_ylim(-1500.0,0.0)
ax1.set_ylim(-1.0,0.0)
ax1.set_xlim(1.e-3,1.e1)
ax1.xaxis.grid(True,'major')
ax1.yaxis.grid(True,'major')
ax1.set_xlabel(r"FeSed [$\mu$mol m$^{-2}$ day$^{-1}$]",fontsize=16)
ax1.set_ylabel("s",fontsize=16)
ax1.plot(sed_roms[:,0,0],s[:],'ro')

dst_nc0.variables["fesed_time"][:] = 180.0
dst_nc0.variables["fesed"][:] = sed_roms[:]

src_nc0.close()
dst_nc0.close()
