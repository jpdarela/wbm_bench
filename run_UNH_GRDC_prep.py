import numpy as np
import gdal
import netCDF4


ds = gdal.Open('runoff_GRDC.tif')
data = ds.ReadAsArray()

lsmk = data[0] == data[0][0][0]

for array in data:
    np.place(array, lsmk, [-9999.0, -9999.0])

lo = np.arange(-179.75, 180, 0.5)
la = np.arange(-55.25, 83, 0.5)
t = np.array([15.5, 45., 74.5, 105., 135.5, 166.,
                           196.5, 227.5, 258., 288.5, 319., 349.5])
nc_filename = 'runoff_GRDC.nc'

rootgrp = netCDF4.Dataset(nc_filename, mode='w', format='NETCDF4')

rootgrp.createDimension("time", None)
rootgrp.createDimension("latitude", la.shape[0])
rootgrp.createDimension("longitude", lo.shape[0])

time = rootgrp.createVariable(varname="time", datatype=np.float32, dimensions=("time",))
latitude = rootgrp.createVariable(varname="latitude", datatype=np.float32,dimensions=("latitude",))
longitude = rootgrp.createVariable(varname="longitude", datatype=np.float32, dimensions=("longitude",))
var_ = rootgrp.createVariable(varname = 'mrro', datatype=np.float32,
                                       dimensions=("time","latitude","longitude",),
                                       fill_value=-9999.0)

rootgrp.description = "GRDC runnof composite--> annual cycle"
rootgrp.source = "UNH-GRDC Composite Runoff Fields <-- http://www.compositerunoff.sr.unh.edu/"
## time
time.units = "days since 1850-01-01"
time.calendar = "noleap"
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
var_.long_name ='Runoff'
var_.units = 'kg m-2 y-1'
var_.standard_name = 'mrro'
var_.missing_value = -9999.0

##filling
time[:] = t
longitude[:] = lo
latitude[:] =  la
var_[:,:,:] = np.fliplr(data)

#closing
ds = None
rootgrp.close()



