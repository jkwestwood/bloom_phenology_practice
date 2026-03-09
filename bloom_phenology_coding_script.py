#Bloom apex and bloom phenology code for The UK 
#created by jkw 

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
#import seaborn as sns
import netCDF4 as nc


#read and import the netCDF data 
filepath= "chl_8day_1999_2018_Julia.nc"   
chla_data= nc.Dataset(filepath)

print(chla_data.variables.keys())

# extract data variables from the netCDF file
# lat = chla_data.variables['latitude'][:]
# long = chla_data.variables['lon'][:]
# time = chla_data.variables['time'][:]
# chla = chla_data.variables['chla'][:]

#extract grid by grid cell data for the UK
#extract the index for a specified grid cell and year
lat_idx = 10
lon_idx = 10
year = 2018

time_var = chla_data.variables['time'][:]
time_units = chla_data.variables['time'].units
dates = nc.num2date(time_var, time_units)
years = np.array([d.year for d in dates])
yr_mask = years == year
time_yr = time_var[yr_mask]
chl = chla_data.variables['chla'][yr_mask, lat_idx, lon_idx]

#plot the entire year of chl-a data for the specified grid cell
plt.figure(figsize=(10, 5))
plt.plot(dates[yr_mask], chl, marker='o', linestyle='-')
plt.title(f'Chlorophyll-a Concentration for Grid Cell ({lat_idx}, {lon_idx}) in {year}')
plt.xlabel('Date')
plt.ylabel('Chlorophyll-a Concentration (mg/m³)')
plt.grid()
plt.show()


#convert to a functions once the I have analyzed the grid cells 






# #functions 
# def read_data(filepath):
#     chla_data= nc.Dataset(filepath)
#     return chla_data


# if __name__ == "__main__":
#     filepath = "chl_8day_1999_2018_Julia.nc"