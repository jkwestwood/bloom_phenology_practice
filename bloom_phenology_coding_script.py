#Bloom apex and bloom phenology code for The UK 

#import all necessary libraries 
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import netCDF4 as nc

#read and import the netCDF data 
filepath= "chl_8day_1999_2018_Julia.nc"   
chla_data= nc.Dataset(filepath)
print(chla_data.variables.keys())

#add in data for data cleaning and drop grids if the data is over 50% missing

# extract data variables from the netCDF file
lat = chla_data.variables['latitude'][:]
long = chla_data.variables['longitude'][:]
time = chla_data.variables['time'][:]
chla = chla_data.variables['chla'][:]

#extract grid by grid cell data for the UK
#extract the index for a specified grid cell and year
lat_idx = 10
lon_idx = 10

#extract data for a specific year
year = 2018


#plot the entire year of chl-a data for the specified grid cell
plt.figure(figsize=(10, 5))
plt.plot(time, chla, marker='o', linestyle='-')
plt.title(f'Chlorophyll-a Concentration for Grid Cell ({lat_idx}, {lon_idx}) in {year}')
plt.xlabel('Date')
plt.ylabel('Chlorophyll-a Concentration (mg/m³)')
plt.grid()
plt.show()

#convert to a functions once the I have analyzed the grid cells 
