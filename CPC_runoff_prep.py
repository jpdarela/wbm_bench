import numpy as np
import gdal
import netCDF4


ds = netCDF4.Dataset('runof.sfc.mon.1981-2010.ltm.nc')
data = ds.variables['runof'][:]

data_out = np.roll(data, 96)

new_lon = np.arange(-(180 - ((360 / 192.) / 2)), 180, (360 / 192.))
new_lat = np.arange(-(90 - ((180 / 94.) / 2)), 90, (180 / 94.))


nc_filename = 'runof_cpc.nc'

rootgrp = netCDF4.Dataset(nc_filename, mode='w', format='NETCDF4')

la = data[0].shape[0]
lo = data[0].shape[1]

    #dimensions
rootgrp.createDimension("time", None)
rootgrp.createDimension("latitude", la)
rootgrp.createDimension("longitude", lo)


    #variables
time = rootgrp.createVariable(varname="time", datatype=np.float32, dimensions=("time",))
latitude = rootgrp.createVariable(varname="latitude", datatype=np.float32,dimensions=("latitude",))
longitude = rootgrp.createVariable(varname="longitude", datatype=np.float32, dimensions=("longitude",))
var_ = rootgrp.createVariable(varname = 'annual_cycle_mean_of_mrro', datatype=np.float32,
                                       dimensions=("time","latitude","longitude",))

    #attributes
    ## rootgrp
rootgrp.description =  'NCEP Reanalysis Derived Products'
rootgrp.source = "http://www.esrl.noaa.gov/psd"
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
var_.long_name = 'Surface Runoff'
var_.units = 'kg m-2'
var_.standard_name='soil moisture'
## WRITING DATA
times_fill = np.array([15.5, 45., 74.5, 105., 135.5, 166.,
                       196.5, 227.5, 258., 288.5, 319., 349.5])
time[:] = times_fill
longitude[:] = new_lon
latitude[:] =  new_lat
var_[:,:,:] = np.fliplr(data_out)
rootgrp.close()
