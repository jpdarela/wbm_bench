import numpy as np
import netCDF4

ds = netCDF4.Dataset('soilw.mon.ltm.v2.nc', 'r')
data = ds.variables['soilw'][:]

data_out = np.zeros(shape=data.shape, dtype=np.float32)
data_out1 = np.zeros(shape=data.shape, dtype=np.float32)
data_out[:,:,:] = data

NO_DATA = [-9999.0, -9999.0]

no_data = data_out[0][0][0]

lsmk_prov = data_out[0] == no_data

lsmk = np.roll(lsmk_prov, 360)

for index in range(data_out.shape[0]):
    data_out1[index] = np.roll(data_out[index], 360)
    
for array in data_out1:
    np.place(array, lsmk, NO_DATA)

nc_filename = 'wsoil_cpc.nc'

rootgrp = netCDF4.Dataset(nc_filename, mode='w', format='NETCDF4')

la = lsmk.shape[0]
lo = lsmk.shape[1]

    #dimensions
rootgrp.createDimension("time", None)
rootgrp.createDimension("latitude", la)
rootgrp.createDimension("longitude", lo)


    #variables
time = rootgrp.createVariable(varname="time", datatype=np.float32, dimensions=("time",))
latitude = rootgrp.createVariable(varname="latitude", datatype=np.float32,dimensions=("latitude",))
longitude = rootgrp.createVariable(varname="longitude", datatype=np.float32, dimensions=("longitude",))
var_ = rootgrp.createVariable(varname = 'annual_cycle_mean_of_mrso', datatype=np.float32,
                                       dimensions=("time","latitude","longitude",),
                                       fill_value=NO_DATA[0])

    #attributes
    ## rootgrp
rootgrp.description =  'Soil water content'
rootgrp.source = "http://www.esrl.noaa.gov/psd/data/gridded/data.cpcsoil.html"
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
var_.long_name = 'Soil Water content '
var_.units = 'kg m-2'
var_.standard_name='soil moisture'
var_.missing_value=NO_DATA[0]
## WRITING DATA
times_fill = np.array([15.5, 45., 74.5, 105., 135.5, 166.,
                       196.5, 227.5, 258., 288.5, 319., 349.5])
time[:] = times_fill
longitude[:] = np.arange(-179.75, 180, 0.5)
latitude[:] =  np.arange(-89.75, 90, 0.5)
var_[:,:,:] = np.fliplr(data_out1)
rootgrp.close()

