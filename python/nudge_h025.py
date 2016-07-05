import os
import numpy as np
import numpy.ma as ma
import Ngl
import netCDF4
from pandas import Series, DataFrame
import pandas as pd
import pyroms

grd_s = pyroms.grid.get_ROMS_grid('h025_l045_v001')

# -- for normal configuration --
#src_nc0 = netCDF4.Dataset('/Users/misumi/roms_data/h025_l045_v001/h025_l045_v001.depth.160705.nc','r')
#src_nc1 = netCDF4.Dataset('/Users/misumi/roms_data/h025_l045_v001/h025_l045_v001.bry-ts.160705.nc','r')
#dst_nc0 = netCDF4.Dataset('/Users/misumi/roms_data/h025_l045_v001/h025_l045_v001.clm-ts.160705.nc','a')

# -- for full configuration --
src_nc0 = netCDF4.Dataset('/Users/misumi/roms_data/h025_l045_v001/h025_l045_v001.depth.160705.nc','r')
src_nc1 = netCDF4.Dataset('/Users/misumi/roms_data/h025_l045_v001/h025_l045_v001.bry-ts.160705.nc','r')
dst_nc0 = netCDF4.Dataset('/Users/misumi/roms_data/h025_l045_v001/h025_l045_v001.clm-ts-full.160705.nc','a')

t_time = src_nc1.variables["temp_time"][:]

#depth = src_nc0.variables["depth"][:]
#nz, ny, nx, = depth.shape
#nudge = ma.zeros([12,nz,ny,nx])

msk = ma.zeros([12,ny,nx])
msk = msk + grd_s.hgrid.mask_rho[:]

#a = ma.where(depth<=-2200.0,365.25,0.0)
#nudge = nudge + a

dst_nc0.variables["temp_time"][:] = t_time
dst_nc0.variables["salt_time"][:] = t_time

#dst_nc0.variables["temp_nudge"][:] = nudge[:]
#nudge[:,-1,:,:] = 30.0
#nudge[:,-1,:,:] = ma.masked_where(msk<1,nudge[:,-1,:,:])
#dst_nc0.variables["salt_nudge"][:] = nudge[:]

dst_nc0.variables["temp_nudge"][:] = 30.0
dst_nc0.variables["salt_nudge"][:] = 30.0

src_nc0.close()
src_nc1.close()
dst_nc0.close()
