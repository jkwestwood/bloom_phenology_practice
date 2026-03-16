#calculating the bloom climax 
#importing necessary libraries
from datetime import datetime
import numpy as np
import netCDF4 as nc
from bloom_phenology_coding_script import chla_time_series_grid_cell

def calculate_bloom_climax(chla_data, year):
    """
    Calculates the bloom climax (peak chlorophyll-a concentration) for each grid cell in the dataset for a specified year, loops
    through each grid cell and calculates the climax by the change in chla over change in time.

    Parameters:
    chla_data: The netCDF dataset containing chlorophyll-a data.
    year: The year for which to calculate the bloom climax.

    Returns:
    bloom_climax (2D array): A 2D array containing the bloom climax (peak chlorophyll-a concentration) for each grid cell in the dataset for the specified year.
    """
    #load all variables into the function 
    lat = chla_data.variables['latitude'][:]
    lon = chla_data.variables['longitude'][:]
    chla = chla_data.variables['chla'][:]
    time = chla_data.variables['time']

    #convert time to datetime objects
    time_dates = nc.num2date(time[:], units=time.units, calendar=getattr(time, 'calendar', 'standard'))
    time_dates = np.array([datetime(d.year, d.month, d.day) for d in time_dates])  #d is the interator                         )   

    #run the analysis for each year-- extract each year
    year_mask = np.array([d.year == year for d in time_dates])
    chla_year = chla[year_mask, :, :] #extracts the chla data for each grid cell :,:... the specified year using the year_mask to index the time dimension of the chla array.
    time_year = time_dates[year_mask]

    #create an empty array to store the bloom climax values for each grid cell
    n_lat = len(lat)
    n_lon = len(lon)
    bloom_climax = np.full((n_lat,n_lon), np.nan)

    #loop through each grid cell 
    for i in range(n_lat): 
        for j in range(n_lon): 

           chla_cell = chla_year[:, i, j] #extracts the chlorophyll-a concentration time series for the current grid cell (i, j) across all time steps in the specified year.
           max_rate = -np.inf #initialize the maximum rate of change to negative infinity to ensure any valid rate will be higher.
           climax_index = 0 #initialize the index of the bloom climax to 0

           for k in range(len(time_year)-1): #loop through the time steps for the current grid cell, stopping one step before the end to avoid index out of range errors when calculating the rate of change.
             
             #calculate change in chla between each timestep 
             dchla = chla_cell[k+1] - chla_cell[k] #calculates the change in chlorophyll-a concentration between consecutive time steps k and k+1 for the current grid cell.
             dt = (time_year[k+1] - time_year[k]).days

             #calculate the rate of change 
             rate = dchla/dt

             #check to see if rate is higher that the previous rate 

             if rate > max_rate:
                max_rate = rate #if the current rate of change is greater than the previously recorded maximum rate, update max_rate to the current rate.
                climax_index = k+1 #update the index of the bloom climax to the current time step k+1, which corresponds to the time step where the maximum rate of change occurs.  

            # store the chla value at the climax timestep for this grid cell
                bloom_climax[i, j] = chla_cell[climax_index]

    return bloom_climax


if __name__ == "__main__":
    chla_data = nc.Dataset('chl_8day_1999_2018_cleaned.nc')
    year = 2001
    bloom_climax = calculate_bloom_climax(chla_data, year)
    print(f"bloom climax for {year}: {bloom_climax}")