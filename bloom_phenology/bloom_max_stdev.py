#finds the standard deviation 
#import the libraries 
import numpy as np 
import netCDF4 as nc 
from bloom_maximum import find_chla_maximum
import warnings
import cartopy.crs as ccrs
import cartopy.feature as cfeature
import matplotlib.pyplot as plt
import numpy as np

#calculations
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
        # use existing function 'find_chla_maximum' to get the bloom max chla for a given year
        bloom_max_dates, bloom_max_chla = find_chla_maximum(chla_data, year)

        # store the annual maximum chla for this year
        all_years_max[year_idx, :, :] = bloom_max_chla

        print(f"Loaded year {year}")

    # count how many years have a valid (non-NaN) value for each grid cell
    valid_count = np.sum(~np.isnan(all_years_max), axis=0)

    # calculate stdev but suppress the warning since we are handling it ourselves
    with warnings.catch_warnings():
        warnings.simplefilter("ignore", RuntimeWarning)
        std_grid = np.nanstd(all_years_max, axis=0)

    # set cells with fewer than 2 valid years to NaN, because not enough strong data values
    std_grid[valid_count < 2] = np.nan

    # print a summary to check the values look sensible
    print(f"std_grid shape       : {std_grid.shape}")
    print(f"Min std value        : {np.nanmin(std_grid):.4f}")
    print(f"Max std value        : {np.nanmax(std_grid):.4f}")
    print(f"Number of NaN cells  : {np.sum(np.isnan(std_grid))}")
    print(f"Number of valid cells: {np.sum(~np.isnan(std_grid))}")

    return std_grid

def avg_annual_max(chla_data, years): 
    '''Calculate the average of the annual maximum of all the grid cells '''
    lat = chla_data.variables['latitude'][:]
    lon = chla_data.variables['longitude'][:]

    # create a 3D array to store the annual maximum chla for each year and grid cell
    all_years_max = np.full((len(years), len(lat), len(lon)), np.nan)

    for year_idx, year in enumerate(years):
        # use existing function 'find_chla_maximum' to get the bloom max chla for a given year
        bloom_max_dates, bloom_max_chla = find_chla_maximum(chla_data, year)

        # store the annual maximum chla for this year
        all_years_max[year_idx, :, :] = bloom_max_chla

        print(f"Loaded year {year}")

    # count how many years have a valid (non-NaN) value for each grid cell
    valid_count = np.sum(~np.isnan(all_years_max), axis=0)

    # calculate stdev but suppress the warning since we are handling it ourselves
    with warnings.catch_warnings():
        warnings.simplefilter("ignore", RuntimeWarning)
        annual_avg = np.average(all_years_max, axis=0)

    # set cells with fewer than 2 valid years to NaN, because not enough strong data values
    annual_avg[valid_count < 2] = np.nan

    # print a summary to check the values look sensible
    print(f"annual_avg shape       : {annual_avg.shape}")
    print(f"Min annual_avg value        : {np.nanmin(annual_avg):.4f}")
    print(f"Max annual_avg value        : {np.nanmax(annual_avg):.4f}")
    print(f"Number of NaN cells  : {np.sum(np.isnan(annual_avg))}")
    print(f"Number of valid cells: {np.sum(~np.isnan(annual_avg))}")

    return annual_avg

def save_results_to_file(std_grid, annual_avg, lat, lon, filepath_out):
    """
    Saves the standard deviation and annual average maximum chla grids to a netCDF file
    so they can be loaded later without rerunning the full calculation.

    Parameters:
    std_grid    : 2D array of standard deviation values (n_lat, n_lon)
    annual_avg  : 2D array of annual average maximum values (n_lat, n_lon)
    lat         : 1D array of latitude values
    lon         : 1D array of longitude values
    filepath_out: path to save the output file e.g. "results.nc"
    """

    new_nc = nc.Dataset(filepath_out, 'w')

    # create dimensions
    new_nc.createDimension('latitude',  len(lat))
    new_nc.createDimension('longitude', len(lon))

    # create and fill variables
    new_lat       = new_nc.createVariable('latitude',   'f4', ('latitude',))
    new_lon       = new_nc.createVariable('longitude',  'f4', ('longitude',))
    new_std       = new_nc.createVariable('std_grid',   'f4', ('latitude', 'longitude'), fill_value=np.nan)
    new_avg       = new_nc.createVariable('annual_avg', 'f4', ('latitude', 'longitude'), fill_value=np.nan)

    new_lat[:]    = lat
    new_lon[:]    = lon
    new_std[:]    = std_grid
    new_avg[:]    = annual_avg

    new_nc.close()
    print(f"Results saved to {filepath_out}")


def load_results_from_file(filepath_in):
    """
    Loads the standard deviation and annual average maximum chla grids
    from a previously saved netCDF file.

    Parameters:
    filepath_in : path to the saved results file

    Returns:
    std_grid   : 2D array of standard deviation values (n_lat, n_lon)
    annual_avg : 2D array of annual average maximum values (n_lat, n_lon)
    lat        : 1D array of latitude values
    lon        : 1D array of longitude values
    """

    results = nc.Dataset(filepath_in, 'r')

    lat        = results.variables['latitude'][:]
    lon        = results.variables['longitude'][:]
    std_grid   = results.variables['std_grid'][:]
    annual_avg = results.variables['annual_avg'][:]

    results.close()

    print(f"Loaded results from {filepath_in}")
    print(f"std_grid shape   : {std_grid.shape}")
    print(f"annual_avg shape : {annual_avg.shape}")

    return std_grid, annual_avg, lat, lon


#testing block 
if __name__ == "__main__":
    filepath     = r"C:\Users\julia\Desktop\Dissertation\chl_8day_cleaned.nc"
    results_path = r"C:\Users\julia\Desktop\Dissertation\bloom_results.nc"

    # --- run this block ONCE to calculate and save the results ---
    # after saving the results, comment this block out so you don't have to rerun it
    chla_data  = nc.Dataset(filepath)
    lat        = chla_data.variables['latitude'][:]
    lon        = chla_data.variables['longitude'][:]
    years      = list(range(1999, 2019))
    std_grid   = calculate_std_annual_maximum(chla_data, years)
    annual_avg = avg_annual_max(chla_data, years)
    chla_data.close()
    save_results_to_file(std_grid, annual_avg, lat, lon, results_path)