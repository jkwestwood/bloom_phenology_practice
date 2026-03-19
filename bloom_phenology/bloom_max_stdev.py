#finds the standard deviation 
#import the libraries 
import numpy as np 
import netCDF4 as nc 
from bloom_maximum import find_chla_maximum
import warnings


def calculate_std_annual_maximum(chla_data, years):
    """
    Calculates the standard deviation of the annual maximum chlorophyll-a 
    concentration for each grid cell across all years.

    Parameters:
    chla_data : the netCDF dataset containing chlorophyll-a data
    years     : a list of years to analyse e.g. [1999, 2000, 2001]

    Returns:
    std_grid (2D array): standard deviation of the annual maximum chla 
                         for each grid cell across all years
    """

    lat = chla_data.variables['latitude'][:]
    lon = chla_data.variables['longitude'][:]

    # create a 3D array to store the annual maximum chla for each year and grid cell
    all_years_max = np.full((len(years), len(lat), len(lon)), np.nan)

    for year_idx, year in enumerate(years):

        # use your existing function to get the bloom max chla for this year
        bloom_max_dates, bloom_max_chla = find_chla_maximum(chla_data, year)

        # debug checks - add these temporarily
        print(f"Year {year}:")
        print(f"  bloom_max_chla shape : {bloom_max_chla.shape}")
        print(f"  Non-NaN values       : {np.sum(~np.isnan(bloom_max_chla))}")
        print(f"  Max chla value       : {np.nanmax(bloom_max_chla) if np.any(~np.isnan(bloom_max_chla)) else 'all NaN'}")

        # store the annual maximum chla for this year
        all_years_max[year_idx, :, :] = bloom_max_chla

        print(f"Loaded year {year}")

    # count how many years have a valid (non-NaN) value for each grid cell
    valid_count = np.sum(~np.isnan(all_years_max), axis=0)

    # calculate std but suppress the warning since we are handling it ourselves
    with warnings.catch_warnings():
        warnings.simplefilter("ignore", RuntimeWarning)
        std_grid = np.nanstd(all_years_max, axis=0)

    # set cells with fewer than 2 valid years to NaN
    std_grid[valid_count < 2] = np.nan

    # print a summary to check the values look sensible
    print(f"std_grid shape       : {std_grid.shape}")
    print(f"Min std value        : {np.nanmin(std_grid):.4f}")
    print(f"Max std value        : {np.nanmax(std_grid):.4f}")
    print(f"Number of NaN cells  : {np.sum(np.isnan(std_grid))}")
    print(f"Number of valid cells: {np.sum(~np.isnan(std_grid))}")

    return std_grid


#testing block
if __name__ == "__main__":
    filepath  = r"C:\Users\julia\Desktop\Dissertation\chl_8day_1999_2018_cleaned.nc"
    chla_data = nc.Dataset(filepath)

    # test find_chla_maximum on its own for just one year
    print("Testing find_chla_maximum for 1999...")
    bloom_max_dates, bloom_max_chla = find_chla_maximum(chla_data, 1999)

    print(f"bloom_max_chla shape : {bloom_max_chla.shape}")
    print(f"Non-NaN values       : {np.sum(~np.isnan(bloom_max_chla))}")
    print(f"Max chla value       : {np.nanmax(bloom_max_chla) if np.any(~np.isnan(bloom_max_chla)) else 'all NaN'}")

    chla_data.close()


