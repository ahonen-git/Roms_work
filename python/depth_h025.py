import os
import numpy as np
import numpy.ma as ma
import Ngl
import netCDF4
from pandas import Series, DataFrame
import pandas as pd
import pyroms

grd_s = pyroms.grid.get_ROMS_grid('h025_l045_v001')

dst_nc0 = netCDF4.Dataset('/Users/misumi/roms_data/h025_l045_v001/h025_l045_v001.depth.160705.nc','a')

msk   = grd_s.hgrid.mask_rho[:]
msk3d = ma.zeros(grd_s.vgrid.z_r[0,:,:,:].shape)
msk3d = msk3d + msk

dep = ma.masked_where(msk3d<0.1,grd_s.vgrid.z_r[0,:,:,:])

dst_nc0.variables["depth"][:] = dep[:]
