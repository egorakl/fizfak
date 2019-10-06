from scipy.io.netcdf import netcdf_file
import numpy as np
import json
import matplotlib.pyplot as plt

coord = [39.66, 117.21] #Beijing

with netcdf_file(r'MSR-2.nc', mmap = False) as f:
    for i in f.variables:
        print(i, f.variables[i].units, f.variables[i].shape)
    variables = f.variables

month = variables['time'].data[:]
ozone = variables['Average_O3_column'].data[:]

lat_i = np.searchsorted(variables['latitude'].data, coord[0])
lon_i = np.searchsorted(variables['longitude'].data, coord[1])

plt.figure(figsize=(12,5))
allm, = plt.plot(month, ozone[:,lat_i,lon_i], 'g')
jan, = plt.plot(month[::12], ozone[::12,lat_i,lon_i],'b')
jun, = plt.plot(month[6::12], ozone[6::12,lat_i,lon_i] , 'r')
plt.legend((allm, jan, jun),('Все месяцы','Все январи','Все июли'))
plt.xlabel('Месяц')
plt.ylabel('Содержание озона')
plt.legend()
plt.savefig('ozon.png')
plt.show()

data = {
    "city": "Beijing",
    "coordinates": coord,
    "jan": {
        "min": float(np.min(month[::12])),
        "max": float(np.max(month[::12])),
        "mean": float(np.mean(month[::12]))
    },
    "jul": {
        "min": float(np.min(month[6::12])),
        "max": float(np.max(month[6::12])),
        "mean": float(np.mean(month[6::12]))
    },
    "all": {
        "min": float(np.min(month)),
        "max": float(np.max(month)),
        "mean": float(np.mean(month))
    }
}

with open('ozon.json', 'w') as out:  
    json.dump(data, out)
