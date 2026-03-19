#Mapping file for inputted information 
#import all the necessary libraries 
import cartopy.crs as ccrs
import cartopy.feature as cfeature
import matplotlib.pyplot as plt
import numpy as np

def map_stdev_grid(std_grid, chla_data):
    """
    Plots the standard deviation of the annual maximum chlorophyll-a
    concentration for each grid cell on a map.

    Parameters:
    std_grid  : 2D array of standard deviation values (n_lat, n_lon)
    chla_data : the netCDF dataset containing chlorophyll-a data (used to get lat/lon)
    """

    lat = chla_data.variables['latitude'][:]
    lon = chla_data.variables['longitude'][:]

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
    plt.show()


def test_map_stdev_grid():
    """
    Tests the map_stdev_grid function using the real dataset and
    the calculate_std_annual_maximum function.
    """

    print("Loading dataset...")
    filepath  = r"C:\Users\julia\Desktop\Dissertation\chl_8day_1999_2018_cleaned.nc"
    chla_data = nc.Dataset(filepath)

    years = list(range(1999, 2019))

    print("Calculating standard deviation across all years...")
    std_grid = calculate_std_annual_maximum(chla_data, years)

    # basic checks before plotting
    print(f"std_grid shape      : {std_grid.shape}")
    print(f"Min std value       : {np.nanmin(std_grid):.4f}")
    print(f"Max std value       : {np.nanmax(std_grid):.4f}")
    print(f"Number of NaN cells : {np.sum(np.isnan(std_grid))}")
    print(f"Number of valid cells: {np.sum(~np.isnan(std_grid))}")

    print("Plotting map...")
    map_stdev_grid(std_grid, chla_data)

    chla_data.close()
    print("Done.")
