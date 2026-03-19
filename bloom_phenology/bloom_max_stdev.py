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

def map_stdev_grid(std_grid, lat, lon):
    """
    Plots the standard deviation of the annual maximum chlorophyll-a
    concentration for each grid cell on a map.

    Parameters:
    std_grid  : 2D array of standard deviation values (n_lat, n_lon)
    lat       : 1D array of latitude values
    lon       : 1D array of longitude values
    """

    # create a meshgrid so every grid cell has a lat and lon coordinate
    lon_grid, lat_grid = np.meshgrid(lon, lat)

    # set up the map with a standard plate carree projection
    fig, ax = plt.subplots(figsize=(12, 8),
                           subplot_kw={'projection': ccrs.PlateCarree()})

    # add coastlines and land features
    ax.add_feature(cfeature.COASTLINE, linewidth=0.8)
    ax.add_feature(cfeature.LAND, facecolor='lightgrey')
    ax.add_feature(cfeature.BORDERS, linewidth=0.5)
    ax.gridlines(draw_labels=True, linewidth=0.5, linestyle='--', color='grey')

    # plot the standard deviation grid on the map
    plot = ax.pcolormesh(lon_grid, lat_grid, std_grid,
                         cmap='coolwarm',
                         transform=ccrs.PlateCarree())

    # add a colourbar
    cbar = plt.colorbar(plot, ax=ax, orientation='vertical', pad=0.05, shrink=0.7)
    cbar.set_label('Standard Deviation of Annual Maximum Chla (mg/m³)', fontsize=11)

    ax.set_title('Standard Deviation of Annual Maximum Chlorophyll-a\nAcross All Grid Cells',
                 fontsize=13)
    plt.tight_layout()
    plt.savefig(r"C:\Users\julia\Desktop\Dissertation\stdev_map.png", dpi=150, bbox_inches='tight')  # save to file
    plt.show(block=True)
    print("Plot saved and displayed")


if __name__ == "__main__":
    filepath  = r"C:\Users\julia\Desktop\Dissertation\chl_8day_cleaned.nc"
    chla_data = nc.Dataset(filepath)

    # extract lat and lon BEFORE closing the dataset
    lat = chla_data.variables['latitude'][:]
    lon = chla_data.variables['longitude'][:]

    years = list(range(1999, 2019))
    print("\nRunning full standard deviation calculation across all years...")
    std_grid = calculate_std_annual_maximum(chla_data, years)

    # close the dataset BEFORE plotting since we already have lat, lon and std_grid
    chla_data.close()

    # pass lat and lon directly instead of the dataset
    map_stdev_grid(std_grid, lat, lon)