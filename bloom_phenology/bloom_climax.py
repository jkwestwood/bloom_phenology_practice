#calculating the bloom climax 

#importing necessary libraries
from datetime import datetime
import numpy as np
import netCDF4 as nc
from bloom_phenology_coding_script import chla_time_series_grid_cell

def calculate_bloom_climax(chla_data, year):
    """
    Calculates the bloom climax (peak chlorophyll-a concentration) for each grid cell in the dataset for a specified year.

    Parameters:
    chla_data: The netCDF dataset containing chlorophyll-a data.
    year: The year for which to calculate the bloom climax.

    Returns:
    bloom_climax (2D array): A 2D array containing the bloom climax (peak chlorophyll-a concentration) for each grid cell in the dataset for the specified year.
    """
    # load all variables once outside the loop
    lat        = chla_data.variables['latitude'][:]
    lon        = chla_data.variables['longitude'][:]
    time       = chla_data.variables['time']
    chla       = chla_data.variables['chla'][:]

    # convert time once outside the loop
    time_dates = nc.num2date(time[:], units=time.units, calendar=getattr(time, 'calendar', 'standard'))
    time_dates = np.array([datetime(d.year, d.month, d.day) for d in time_dates])

    # filter to the requested year once outside the loop
    year_mask  = np.array([d.year == year for d in time_dates])
    chla_year  = chla[year_mask, :, :]    # shape: (n_timesteps_in_year, n_lat, n_lon)

    # pre-allocate output array shaped (n_lat, n_lon)
    bloom_climax = np.full((len(lat), len(lon)), np.nan)

    for lat_idx in range(len(lat)):
        for lon_idx in range(len(lon)):
            chla_cell = chla_year[:, lat_idx, lon_idx]

            # skip grid cells that are entirely NaN
            if np.all(np.isnan(chla_cell)):
                continue
            # store the peak chla value for this grid cell
            bloom_climax[lat_idx, lon_idx] = np.nanmax(chla_cell)


    return bloom_climax

if __name__ == "__main__":
    chla_data = nc.Dataset('chl_8day_1999_2018_cleaned.nc')
    year = 2001
    bloom_climax = calculate_bloom_climax(chla_data, year)
    print(bloom_climax)