#import all necessary libraries
import numpy as np
import netCDF4
import pandas as pd
from scipy.signal import savgol_filter
import numpy as np
import netCDF4

fp = 'chl_8day_1999_2018_Julia.nc'
nc = netCDF4.Dataset(fp)

# Pick your grid cell (lat and long) and year
lat_idx = 10
lon_idx = 10
year = 2018

# assign variables from the nc file l
time_var = nc.variables['time'][:]
time_units = nc.variables['time'].units

#create the datset from the time variable and units
dates = netCDF4.num2date(time_var, time_units)
years = np.array([d.year for d in dates])

# Slice out by year at that chosen grid cell
yr_mask = years == year
time_yr = time_var[yr_mask]
chl = nc.variables['chla'][yr_mask, lat_idx, lon_idx]

# Convert masked values to NaN using the filled method of masked arrays via numpy, 
# then to float values for interpolation and smoothing. 
# This is necessary because the original data may have masked values that need 
# to be handled as NaNs for the subsequent processing steps.    
chl = np.ma.filled(chl.astype(float), np.nan)



# Fill NaNs values using  
nans = np.isnan(chl) #determine if its an nan
x = np.arange(len(chl)) #creates an array of equally spaced values within a defined interval in this its year
chl[nans] = np.interp(x[nans], x[~nans], chl[~nans]) #use the numpy interpolation function to fill in the NaN values based on the non-NaN values in the data.

#calculate the Derivatives
#use the numpy gradient function to calculate the first 
# and second derivatives of the chlorophyll-a concentration with respect to time.
#the tool is defined as the change in y/change in x, where y is the chlorophyll-a concentration and x is time.
dchl_dt = np.gradient(chl, time_yr)
d2chl_dt2 = np.gradient(dchl_dt, time_yr)

# Find onset after annual minimum
min_idx = np.argmin(chl) #find the index of the minimum chl-a value 

#loop through the range of the data from the minumum index to the end of the dataset
for k in range(min_idx, len(chl) - 1):

    #uses boolean to determine if the first derivative is positive (indicating an increase in chlorophyll-a concentration) 
    # and if the second derivative is also positive (indicating that the rate of increase is accelerating). == onset
    #if the requirements are met then that is the day of the bloom and get the chl-a value of that day 
    if dchl_dt[k] > 0 and d2chl_dt2[k] > 0:
        onset_doy = dates[np.where(yr_mask)[0][k]].timetuple().tm_yday

        #format the print statements so they are easier to read 
        print(f"Bloom onset: day {onset_doy} of {year}")
        print(f"Chl-a value at onset: {chl[k]:.4f}")
        break #signals to exit the loop 


#determine the size of the dataset 
lats = nc.variables['latitude'][:]
lons = nc.variables['longitude'][:]

print(f"Latitude points: {len(lats)}")
print(f"Longitude points: {len(lons)}")
print(f"Total grid cells: {len(lats) * len(lons)}")

nc.close()




