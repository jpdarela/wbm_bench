##PYTHON2

import numpy as np
import os
import glob
import gdal
import netCDF4


files = sorted(glob.glob1(os.getcwd(), '*.nc'))

# a mask for GLEAM et data

ds = gdal.Open(files[0])
no_data = float(ds.GetMetadata_Dict()['et#_FillValue'])
lat, lon = ds.ReadAsArray().shape
lsmk = ds.ReadAsArray() == no_data
ds =None

#lsmk = np.load('mask.npy')

data_out = np.zeros(shape=(len(files),lat,lon,),dtype=np.float32)
time_arr = []


def read_nc(filename, data_out):

    global time_arr
    ds = gdal.Open(filename)
    raw_data = ds.ReadAsArray()
    np.place(raw_data, lsmk, [no_data, no_data])
    print raw_data.shape, '\n'
    t = np.int32(ds.GetMetadata_Dict()['et#time'])
    data_out[len(time_arr)] = raw_data
    time_arr.append(t)
    ds = None


def write_nc(nc_filename, arr, var, time_array):
    t, la, lo,  = arr.shape

    # create netcdf file
    rootgrp = netCDF4.Dataset(nc_filename, mode='w', format='NETCDF4')

    #dimensions
    rootgrp.createDimension("time", None)
    rootgrp.createDimension("latitude", la)
    rootgrp.createDimension("longitude", lo)


    #variables
    time      = rootgrp.createVariable(varname="time", datatype=np.float32, dimensions=("time",))
    latitude  = rootgrp.createVariable(varname="latitude", datatype=np.float32,dimensions=("latitude",))
    longitude = rootgrp.createVariable(varname="longitude", datatype=np.float32, dimensions=("longitude",))
    var_      = rootgrp.createVariable(varname = var, datatype=np.float32,
                                       dimensions=("time","latitude","longitude",),
                                       fill_value=no_data)

    #attributes
    ## rootgrp
    rootgrp.description = "MODIS_Evapotranpiration_2000-2010--> annual cycle"
    rootgrp.source = "MODIS"
    ## time
    time.units = "days since 1850-01-01"
    time.calendar = "gregorian"
    time.axis='T'
    ## lat
    latitude.units = "degrees_north"
    latitude.long_name= "latitude"
    latitude.standart_name = "latitude"
    latitude.axis =  'Y'
    ## lon
    longitude.units = "degrees_east"
    longitude.long_name = "longitude"
    longitude.standart_name = "longitude"
    longitude.axis = 'X'
    ## var
    var_.long_name='Evapotranspiration'
    var_.units = 'kg m-2 s-1'
    var_.standard_name='et'
    var_.missing_value=no_data

    ## WRITING DATA
    times_fill = time_array
    time[:] = times_fill

    longitude[:] = np.arange(-179.75, 180, 0.5)
    latitude[:] =  np.arange(-89.75, 90, 0.5)

    var_[:,:,:] = np.fliplr(arr)
    rootgrp.close()



for f in files:
    print f,
    read_nc(f, data_out)


time_array = np.array(time_arr, dtype=np.float32)
write_nc('et_MODIS_2000_2010.nc', data_out, 'et', time_array)








