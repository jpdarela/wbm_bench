import numpy as np
import netCDF4
from ILAMB.Variable import Variable

ds = netCDF4.Dataset('GLDAS_NOAH10_M.A200101_201501.totalH2O.nc', 'r')
data = np.fliplr(ds.variables['Water_Thickness'][:]) * 10. # data in mm == kg m-2

ds.close()

lon = np.arange(0.5, 360, 1.)
lat = np.arange(-89.5, 90, 1.)


time_arr = np.array([-350,-319,-289,-258,-228,-197,-167,-136,-106,-75,-45,-15,15,46,
        76,107,137,168,198,229,259,290,320,350,380,411,441,472,502,533,
        563,594,624,655,685,715,745,776,806,837,867,898,928,959,989,1020,
        1050,1081,1111,1142,1172,1203,1233,1264,1294,1325,1355,1386,1416,
        1446,1476,1507,1537,1568,1598,1629,1659,1690,1720,1751,1781,1811,
        1841,1872,1902,1933,1963,1994,2024,2055,2085,2116,2146,2176,2206,
        2237,2267,2298,2328,2359,2389,2420,2450,2481,2511,2542,2572,2603,
        2633,2664,2694,2725,2755,2786,2816,2847,2877,2907,2937,2968,2998,
        3029,3059,3090,3120,3151,3181,3212,3242,3272,3302,3333,3363,3394,
        3424,3455,3485,3516,3546,3577,3607,3637,3667,3698,3728,3759,3789,
        3820,3850,3881,3911,3942,3972,4003,4033,4064,4094,4125,4155,4186,
        4216,4247,4277,4308,4338,4368,4398,4429,4459,4490,4520,4551,4581,
        4612,4642,4673,4703,4733,4763])


nc_filename = 'wsoil_GLDAS-NOAH.nc'

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
var_ = rootgrp.createVariable(varname = 'mrso', datatype=np.float32,
                                       dimensions=("time","latitude","longitude",))

    #attributes
    ## rootgrp
rootgrp.description =  'Soil water content'
rootgrp.source = "GLDAS NOAH dataset"
    ## time
time.units = "days since 2002-01-01"
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

## WRITING DATA
times_fill = time_arr
time[:] = times_fill
longitude[:] = lon
latitude[:] =  lat
var_[:,:,:] = np.fliplr(data)
rootgrp.close()


var = Variable(filename=nc_filename, variable_name='mrso')
an_var=var.annualCycle()
ds = netCDF4.Dataset('wsoil_GLDAS_NOAH_AC.nc', mode='w', format='NETCDF4')
an_var.toNetCDF4(ds)
ds.close()


