import numpy as np
import os
import glob
import gdal
from netCDF4 import Dataset as dt
import time
from ILAMB.Variable import Variable

mask_fpath = './mask12.npy'
NO_DATA = [-999.0, -999.0]
lsmk = np.load(mask_fpath)

fdir = './outputs_flt'
files = glob.glob1(fdir, '*.flt')
fpath = fdir + os.sep + files[0]
varname = files[0].split('.')[0]
caete_name = fdir + os.sep + varname + '_' + 'annual_cycle_mean_CAETE.nc'
nc_filename = caete_name


def flt_attrs():
    return {'wsoil' : ['soil_water_fraction','1'],
            'et'    : ['evapotranpiration','kg/m^2/s'],
            'runoff': ['runoff','m^3/s']}



def read_raster(fpath):
    """Returns the raster file in fpath as a masked numpy array
    with shape as raster file
    formal arguments:
    
    fpath :: string: complete file path

    """
    
    ds = gdal.Open(fpath)
    raw_data = ds.ReadAsArray()
    ds = None    
    return np.ma.masked_array(raw_data, mask= lsmk)    
    
    
def write_CAETE_output(nc_filename, arr, var):

    t, la, lo,  = arr.shape 
    
    # create netcdf file
    rootgrp = dt(nc_filename, mode='w', format='NETCDF4')
    
    #dimensions
    rootgrp.createDimension("time", None)
    rootgrp.createDimension("latitude", la)
    rootgrp.createDimension("longitude", lo)
    
    
    #variables
    time      = rootgrp.createVariable("time",np.float32,("time",))
    latitude  = rootgrp.createVariable("latitude",np.float32,("latitude",))
    longitude = rootgrp.createVariable("longitude",np.float32,("longitude",))
    var_       = rootgrp.createVariable('annual_cycle_mean_of_' + str(var),
                                  np.float32,("time","latitude","longitude",))
    
    
    #attributes
    ## rootgrp
    rootgrp.description = flt_attrs()[var][0] + " from CAETE_1981-2010--> annual cycle"
    rootgrp.source = "CAETE model outputs"
    
    ## time
    time.units = "days since 1850-01-01 00:00:00.0"
    time.calendar = "noleap"
    time.axis='T'

    ## lat
    latitude.units = u"degrees_north"   
    latitude.long_name=u"latitude"
    latitude.standart_name =u"latitude"
    latitude.axis = u'Y'

    ## lon
    longitude.units = "degrees_east"
    longitude.long_name = "longitude"
    longitude.standart_name = "longitude"
    longitude.axis = 'X'
    
    ## var
    var_.units = flt_attrs()[var][1]
    var_._MissingValue = NO_DATA
    
    ## WRITING DATA
    times_fill = np.array([15.5, 45., 74.5, 105., 135.5, 166., 
                           196.5, 227.5, 258., 288.5, 319., 349.5])
    
    time[:] = times_fill
    longitude[:] = np.arange(-179.75, 180, 0.5)
    latitude[:] =  np.arange(-89.75, 90, 0.5)
    var_[:,:,:] = arr
    rootgrp.close()

for fl in range(len(files)):
    fpath = fdir + os.sep + files[fl]
    varname = files[fl].split('.')[0]
    caete_name = fdir + os.sep + varname + '_' + 'annual_cycle_mean_CAETE.nc'
    nc_filename = caete_name
    
    var__fill = read_raster(fpath)
    write_CAETE_output(caete_name, var__fill, varname)
