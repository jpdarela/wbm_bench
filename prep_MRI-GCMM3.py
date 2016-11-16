#python2

import numpy as np
from netCDF4 import Dataset as dt
import ILAMB.Variable as Variable
import netCDF4
import os
import datetime


#STEP 1 - calculate evapotranspiration evspsblsoi + evspsblveg + tran
os.chdir(os.getcwd() + '/MRI-CGCM3')
# OPEN FILES
evsoil = dt('evspsblsoi_Lmon_MRI-CGCM3_midHolocene_r1i1p1_195101-205012.nc', 'r')
evveg = dt('evspsblveg_Lmon_MRI-CGCM3_midHolocene_r1i1p1_195101-205012.nc', 'r')
transp = dt('tran_Lmon_MRI-CGCM3_midHolocene_r1i1p1_195101-205012.nc', 'r')

# Time CAETE 
init = datetime.datetime(1981,1,1)
end  = datetime.datetime(2010,12,31)

t_unit = 'days since 1951-01-01'
calendar = 'standard'

t_init = netCDF4.date2index(init, evsoil.variables['time'],
                            calendar=calendar, select='nearest')
t_end = netCDF4.date2index(end, evsoil.variables['time'],
                            calendar=calendar, select='nearest')


# General dimensions (common to all variables)
lat = evsoil.variables['lat'][:]
lon = evsoil.variables['lon'][:]
times = evsoil.variables['time'][t_init:t_end+1]


# _________________________ET calcs_____________________________________________
# catching data to calculate et

evsoil_data = evsoil.variables['evspsblsoi'][t_init:t_end+1,:,:]
evveg_data = evveg.variables['evspsblveg'][t_init:t_end+1,:,:]
transp_data = transp.variables['tran'][t_init:t_end+1,:,:]

# Close Files
evsoil.close()
evveg.close()
transp.close()

# calculate et
et = evsoil_data + evveg_data + transp_data

# write output
nc_filename = 'et_MRI-CGCM3_1981-2010.nc'

rootgrp = netCDF4.Dataset(nc_filename, mode='w', format='NETCDF4')

la = et[0].shape[0]
lo = et[0].shape[1]

    #dimensions
rootgrp.createDimension("time", None)
rootgrp.createDimension("latitude", la)
rootgrp.createDimension("longitude", lo)


    #variables
time = rootgrp.createVariable(varname="time", datatype=np.float32, dimensions=("time",))
latitude = rootgrp.createVariable(varname="latitude", datatype=np.float32,dimensions=("latitude",))
longitude = rootgrp.createVariable(varname="longitude", datatype=np.float32, dimensions=("longitude",))
var_ = rootgrp.createVariable(varname = 'et', datatype=np.float32,
                                       dimensions=("time","latitude","longitude",))

    #attributes
    ## rootgrp
rootgrp.description =  'MRI-CGCM3-historical model results-1981-2010'
rootgrp.source = "CMIP5-historical"
    ## time
time.units = t_unit
time.calendar = calendar
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
var_.long_name = 'Evapotranspiration'
var_.units = 'kg m-2 s-1'
var_.standard_name='et'
## WRITING DATA
time[:] = times
longitude[:] = lon
latitude[:] =  lat
var_[:,:,:] = et
rootgrp.close()

var = Variable.Variable(filename=nc_filename, variable_name='et')
var_ = var.annualCycle()
ds = netCDF4.Dataset('et_MRI-CGCM3_AC_1981_2010.nc', 'w')
var_.toNetCDF4(ds)
ds.close()
#____________________________________END_ET_calcs_______________________________

#____________________________________RUNOFF_calcs_______________________________
# catching data to calculate runoff

runoff_sub_sur = dt('mrro_Lmon_MRI-CGCM3_midHolocene_r1i1p1_195101-205012.nc', 'r')
wsoil = dt('mrso_Lmon_MRI-CGCM3_midHolocene_r1i1p1_195101-205012.nc', 'r')

runoff_sub_sur_data = runoff_sub_sur.variables['mrro'][t_init:t_end+1,:,:]
wsoil_data = wsoil.variables['mrso'][t_init:t_end+1,:,:]

# Close Files

runoff_sub_sur.close()
wsoil.close()

# write outputs

## runoff 
nc_filename = 'mrro_MRI-CGCM3_1981_2010.nc'

rootgrp = netCDF4.Dataset(nc_filename, mode='w', format='NETCDF4')

la = runoff_sub_sur_data[0].shape[0]
lo = runoff_sub_sur_data[0].shape[1]

    #dimensions
rootgrp.createDimension("time", None)
rootgrp.createDimension("latitude", la)
rootgrp.createDimension("longitude", lo)


    #variables
time = rootgrp.createVariable(varname="time", datatype=np.float32, dimensions=("time",))
latitude = rootgrp.createVariable(varname="latitude", datatype=np.float32,dimensions=("latitude",))
longitude = rootgrp.createVariable(varname="longitude", datatype=np.float32, dimensions=("longitude",))
var_ = rootgrp.createVariable(varname = 'mrro', datatype=np.float32,
                                       dimensions=("time","latitude","longitude",))

    #attributes
    ## rootgrp
rootgrp.description =  'MRI-CGCM3-historical model results-1981-2010'
rootgrp.source = "CMIP5-historical"
    ## time
time.units = t_unit
time.calendar = calendar
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
var_.long_name = 'Total runoff flux'
var_.units = 'kg m-2 s-1'
var_.standard_name='et'
## WRITING DATA
time[:] = times
longitude[:] = lon
latitude[:] =  lat
var_[:,:,:] = runoff_sub_sur_data
rootgrp.close()

var = Variable.Variable(filename=nc_filename, variable_name='mrro')
var_ = var.annualCycle()
ds = netCDF4.Dataset('mrro_MRI-CGCM3_AC_1981_2010.nc', 'w')
var_.toNetCDF4(ds)
ds.close()
# ___ end runoff #################__0-------------------------------------------

## save wsoil
nc_filename = 'mrso_MRI-CGCM3_1981_2010.nc'

rootgrp = netCDF4.Dataset(nc_filename, mode='w', format='NETCDF4')

la = wsoil_data[0].shape[0]
lo = wsoil_data[0].shape[1]

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
rootgrp.description =  'MRI-CGCM3-historical model results-1981-2010'
rootgrp.source = "CMIP5-historical"
    ## time
time.units = t_unit
time.calendar = calendar
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
var_.long_name = 'Soil water content'
var_.units = 'kg m-2'
var_.standard_name='soil_moisture_content'
## WRITING DATA
time[:] = times
longitude[:] = lon
latitude[:] =  lat
var_[:,:,:] = wsoil_data
rootgrp.close()

var = Variable.Variable(filename=nc_filename, variable_name='mrso')
var_ = var.annualCycle()
ds = netCDF4.Dataset('mrso_MRI-CGCM3_AC_1981_2010.nc', 'w')
var_.toNetCDF4(ds)
ds.close()

print "ok"
