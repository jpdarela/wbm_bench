import os
import numpy as np
import netCDF4
import matplotlib.pyplot as plt



data_dir_one = './CCI-ESA-soilw-v02.2/1981'
days  = sorted(os.listdir(data_dir_one))

# catch metadata commom to all files
ds = netCDF4.Dataset(data_dir_one + os.sep + days[125], 'r')

lent, lenla, lenlon = ds.variables['sm'][:].shape
lat = ds.variables['lat'][:]
lon = ds.variables['lon'][:]

ds.close()


#ly_time = ds.variables['time'][:]

#time = len(days)

data_dir = './CCI-ESA-soilw-v02.2'
years = sorted(os.listdir(data_dir))
for year in years:
    files = os.listdir(data_dir + os.sep + year)
    # create things to fill year netcdf file
    data_out = np.zeros(shape=(len(files), lenla, lenlon))
    time_arr = np.array((), dtype=np.float64)
    print year, len(files)
    for i,fh in enumerate(files):
        ds = netCDF4.Dataset(fh, 'r')
        data_ds = ds.variable['sm'][:]
        time_arr = np.hstack((time_arr, ds.variable['time'][:]))
        file_path = year + '/' + fh,
        print i,fh,file_path
        ds.close()


#plt.imshow(data_ds[0])
#plt.colorbar()
#plt.show() 
#ds.close()
