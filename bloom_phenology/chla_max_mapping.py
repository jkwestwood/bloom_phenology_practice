#script that create maps for the bloom maximum date and bloom maximum chlorophyll-a concentration for each grid cell in the dataset.

#import all the necessary libraries
import netCDF4 as nc
import matplotlib.pyplot as plt
import matplotlib.colors as mcolors
import matplotlib.dates as mdates
import numpy as np
from datetime import datetime
#import functions from the bloom phenology coding script
from bloom_maximum import find_chla_maximum

#create a mapping function 
def create_chla_maximum_maps(chla_data, year):
    """
    Creates maps for the bloom maximum date and bloom maximum chlorophyll-a concentration for each grid cell in the dataset.

    Parameters:
    chla_data: The netCDF dataset containing chlorophyll-a data.
    year: The year for which to find the bloom maximum.

    Outputs:
    Two maps: one for the bloom maximum date and one for the bloom maximum chlorophyll-a concentration for each grid cell in the dataset.
    """

    # call on the find_chla_maximum function to get the bloom maximum date and chla for each grid cell
    bloom_max_dates, bloom_max_chla = find_chla_maximum(chla_data, year)

    # convert datetime objects to day-of-year (1-365) so imshow can plot them as floats
    bloom_max_doy = np.full(bloom_max_dates.shape, np.nan)  # pre-fill with NaN for land/missing cells
    for i in range(bloom_max_dates.shape[0]):
        for j in range(bloom_max_dates.shape[1]):
            if bloom_max_dates[i, j] is not None:
                bloom_max_doy[i, j] = bloom_max_dates[i, j].timetuple().tm_yday  # extract day of year

    # create a map for the bloom maximum date (as day of year)
    plt.figure(figsize=(10, 6))
    img = plt.imshow(bloom_max_doy, cmap='viridis', interpolation='none')
    cbar = plt.colorbar(img, label='Day of Year')
    plt.title(f'Bloom Maximum Date for {year}')
    plt.xlabel('Longitude Index')
    plt.ylabel('Latitude Index')
    plt.show()

    # create a map for the bloom maximum chlorophyll-a concentration
    plt.figure(figsize=(10, 6))
    img = plt.imshow(bloom_max_chla, cmap='viridis', interpolation='none')
    plt.colorbar(img, label='Bloom Maximum Chlorophyll-a Concentration (mg/m³)')
    plt.title(f'Bloom Maximum Chlorophyll-a Concentration for {year}')
    plt.xlabel('Longitude Index')
    plt.ylabel('Latitude Index')
    plt.show()

if __name__ == "__main__":
    chla_data = nc.Dataset('chl_8day_1999_2018_Julia.nc')
    year = 2018
    create_chla_maximum_maps(chla_data, year)