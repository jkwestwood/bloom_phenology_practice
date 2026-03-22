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

def avg_annual_day(chla_data, years): 
    '''Calculate the average of the annual maximum of all the grid cells '''
    lat = chla_data.variables['latitude'][:]
    lon = chla_data.variables['longitude'][:]

    # create a 3D array to store the annual maximum chla for each year and grid cell
    all_years_max = np.full((len(years), len(lat), len(lon)), np.nan)

    for year_idx, year in enumerate(years):
        # use existing function 'find_chla_maximum' to get the bloom max chla for a given year
        bloom_max_dates, bloom_max_chla = find_chla_maximum(chla_data, year)

        #create a nested loop for each day in the year 
        for i in range(len(lat)): 
            for j in range(len(lat)): 
                date = bloom_max_dates[i,j]

                if date is not None: 
                    all_years_max[year_idx, i, j] = date.timetuple().tm_yday

       
        print(f"Loaded year {year}")

    # count how many years have a valid (non-NaN) value for each grid cell
    valid_count = np.sum(~np.isnan(all_years_max), axis=0)

    # calculate stdev but suppress the warning since we are handling it ourselves
    with warnings.catch_warnings():
        warnings.simplefilter("ignore", RuntimeWarning)
        avg_day = np.average(all_years_max, axis=0)

    # set cells with fewer than 2 valid years to NaN, because not enough strong data values
    avg_day[valid_count < 2] = np.nan

    # print a summary to check the values look sensible
    print(f"Avg Day shape       : {avg_day.shape}")
    print(f"Min Annual Day value        : {np.nanmin(avg_day):.4f}")
    print(f"Max Day of Avg value        : {np.nanmax(avg_day):.4f}")
    print(f"Number of NaN cells  : {np.sum(np.isnan(avg_day))}")
    print(f"Number of valid cells: {np.sum(~np.isnan(avg_day))}")

    return avg_day

def stdev_day(chla_data, years): 
     '''Calculate the average of the annual maximum of all the grid cells '''
     lat = chla_data.variables['latitude'][:]
     lon = chla_data.variables['longitude'][:]

    # create a 3D array to store the annual maximum chla for each year and grid cell
     all_years_max = np.full((len(years), len(lat), len(lon)), np.nan)

     for year_idx, year in enumerate(years):
        # use existing function 'find_chla_maximum' to get the bloom max chla for a given year
        bloom_max_dates, bloom_max_chla = find_chla_maximum(chla_data, year)

        #create a nested loop for each day in the year 
        for i in range(len(lat)): 
            for j in range(len(lat)): 
                date = bloom_max_dates[i,j]

                if date is not None: 
                    all_years_max[year_idx, i, j] = date.timetuple().tm_yday

       
        print(f"Loaded year {year}")

    # count how many years have a valid (non-NaN) value for each grid cell
     valid_count = np.sum(~np.isnan(all_years_max), axis=0)

    # calculate stdev but suppress the warning since we are handling it ourselves
     with warnings.catch_warnings():
        warnings.simplefilter("ignore", RuntimeWarning)
        avg_stdev_day = np.nanstd(all_years_max, axis=0)

    # set cells with fewer than 2 valid years to NaN, because not enough strong data values
     avg_stdev_day[valid_count < 2] = np.nan

    # print a summary to check the values look sensible
     print(f"Avg Day shape       : {avg_stdev_day.shape}")
     print(f"Min Annual Day value        : {np.nanmin(avg_stdev_day):.4f}")
     print(f"Max Day of Avg value        : {np.nanmax(avg_stdev_day):.4f}")
     print(f"Number of NaN cells  : {np.sum(np.isnan(avg_stdev_day))}")
     print(f"Number of valid cells: {np.sum(~np.isnan(avg_stdev_day))}")

     return avg_stdev_day



def save_results_to_file(std_grid, annual_avg, lat, lon, filepath_out, avg_day):
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
    new_avg_day   = new_nc.createVariable('avg_day',    'f4', ('latitude', 'longitude'), fill_value=np.nan )

    new_lat[:]       = lat
    new_lon[:]       = lon
    new_std[:]       = std_grid
    new_avg[:]       = annual_avg
    new_avg_day[:]   = avg_day

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

# Add plots and maps for the calculations from above 
#distribution plot for avg chla-maximum
def plot_avg_distribution(annual_avg):
    '''
    Plots the distribution of the annual average maximum chlorophyll-a
    concentration across all grid cells to check for outliers or skewed values.

    Parameters:
    annual_avg : 2D array of annual average values (n_lat, n_lon)
    '''

    # flatten the 2D grid into a 1D array and remove NaN values for plotting
    flat_values = annual_avg.flatten()
    flat_values = flat_values[~np.isnan(flat_values)]

    print(f"Total valid cells    : {len(flat_values)}")
    print(f"Mean value           : {np.mean(flat_values):.4f}")
    print(f"Median value         : {np.median(flat_values):.4f}")
    print(f"Std value            : {np.std(flat_values):.4f}")
    print(f"Min value            : {np.min(flat_values):.4f}")
    print(f"Max value            : {np.max(flat_values):.4f}")
    print(f"Values above 10      : {np.sum(flat_values > 10)}")
    print(f"Values above 50      : {np.sum(flat_values > 50)}")

    fig, axes = plt.subplots(1, 2, figsize=(14, 5))

    # --- left plot: full distribution ---
    axes[0].hist(flat_values, bins=50, color='steelblue', edgecolor='white')
    axes[0].set_xlabel('Annual Average Maximum Chla (mg/m³)')
    axes[0].set_ylabel('Number of Grid Cells')
    axes[0].set_title('Full Distribution')
    axes[0].axvline(np.mean(flat_values), color='red', linestyle='--', label=f'Mean: {np.mean(flat_values):.2f}')
    axes[0].axvline(np.median(flat_values), color='orange', linestyle='--', label=f'Median: {np.median(flat_values):.2f}')
    axes[0].legend()

    # --- right plot: zoomed in to remove extreme outliers ---
    # clip to 95th percentile so outliers dont squash the distribution
    percentile_95 = np.percentile(flat_values, 95)
    clipped_values = flat_values[flat_values <= percentile_95]

    axes[1].hist(clipped_values, bins=50, color='steelblue', edgecolor='white')
    axes[1].set_xlabel('Annual Average Maximum Chla (mg/m³)')
    axes[1].set_ylabel('Number of Grid Cells')
    axes[1].set_title(f'Zoomed to 95th Percentile (below {percentile_95:.2f})')
    axes[1].axvline(np.mean(clipped_values), color='red', linestyle='--', label=f'Mean: {np.mean(clipped_values):.2f}')
    axes[1].axvline(np.median(clipped_values), color='orange', linestyle='--', label=f'Median: {np.median(clipped_values):.2f}')
    axes[1].legend()

    plt.suptitle('Distribution of Annual Average Maximum Chlorophyll-a', fontsize=13)
    plt.tight_layout()
    plt.savefig(r"C:\Users\julia\Desktop\Dissertation\avg_distribution.png", dpi=150, bbox_inches='tight')
    plt.show()
    print("Plot saved and displayed")

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

def map_max_avg(lat, lon, data):
    '''
    Plots the mean annual maximum chlorophyll-a
    concentration for each grid cell on a map.

    Parameters:
    lat  : 1D array of latitude values
    lon  : 1D array of longitude values
    data : 2D array of annual average values (n_lat, n_lon)
    '''

    lon_grid, lat_grid = np.meshgrid(lon, lat)

    fig, ax = plt.subplots(figsize=(12, 8),
                           subplot_kw={'projection': ccrs.PlateCarree()})

    ax.add_feature(cfeature.COASTLINE, linewidth=0.8)
    ax.add_feature(cfeature.LAND, facecolor='lightgrey')
    ax.add_feature(cfeature.BORDERS, linewidth=0.5)
    ax.gridlines(draw_labels=True, linewidth=0.5, linestyle='--', color='grey')

    plot = ax.pcolormesh(lon_grid, lat_grid, data,
                         cmap='coolwarm',
                         transform=ccrs.PlateCarree())

    cbar = plt.colorbar(plot, ax=ax, orientation='vertical', pad=0.05, shrink=0.7)
    cbar.set_label('Mean Annual Maximum Chla (mg/m³)', fontsize=11)

    ax.set_title('Mean Annual Maximum Chlorophyll-a Across All Grid Cells', fontsize=13)

    plt.tight_layout()
    plt.savefig(r"C:\Users\julia\Desktop\Dissertation\avg_max_map.png", dpi=150, bbox_inches='tight')
    plt.show(block=True)
    print("Plot saved and displayed")

def map_day_avg(lat, lon, avg_day): 
    '''
    Plots the mean annual day for maximum chlorophyll-a
    concentration for each grid cell on a map.

    Parameters:
    lat  : 1D array of latitude values
    lon  : 1D array of longitude values
    data : 2D array of annual average values (n_lat, n_lon)
    '''

    lon_grid, lat_grid = np.meshgrid(lon, lat)

    fig, ax = plt.subplots(figsize=(12, 8),
                           subplot_kw={'projection': ccrs.PlateCarree()})

    ax.add_feature(cfeature.COASTLINE, linewidth=0.8)
    ax.add_feature(cfeature.LAND, facecolor='lightgrey')
    ax.add_feature(cfeature.BORDERS, linewidth=0.5)
    ax.gridlines(draw_labels=True, linewidth=0.5, linestyle='--', color='grey')

    plot = ax.pcolormesh(lon_grid, lat_grid, avg_day,
                         cmap='coolwarm',
                         transform=ccrs.PlateCarree())

    cbar = plt.colorbar(plot, ax=ax, orientation='vertical', pad=0.05, shrink=0.7)
    cbar.set_label('Mean Annual Maximum Chla (mg/m³)', fontsize=11)

    ax.set_title('Mean Day of Chl-a Bloom', fontsize=13)

    plt.tight_layout()
    plt.savefig(r"C:\Users\julia\Desktop\Dissertation\avg_day_map.png", dpi=150, bbox_inches='tight')
    plt.show(block=True)
    print("Plot saved and displayed")

def map_day_stdev(lat, lon, std_day): 
     '''
    Plots the mean annual day for maximum chlorophyll-a
    concentration for each grid cell on a map.

    Parameters:
    lat  : 1D array of latitude values
    lon  : 1D array of longitude values
    data : 2D array of annual average values (n_lat, n_lon)
    '''

     lon_grid, lat_grid = np.meshgrid(lon, lat)

     fig, ax = plt.subplots(figsize=(12, 8),
                           subplot_kw={'projection': ccrs.PlateCarree()})

     ax.add_feature(cfeature.COASTLINE, linewidth=0.8)
     ax.add_feature(cfeature.LAND, facecolor='lightgrey')
     ax.add_feature(cfeature.BORDERS, linewidth=0.5)
     ax.gridlines(draw_labels=True, linewidth=0.5, linestyle='--', color='grey')

     plot = ax.pcolormesh(lon_grid, lat_grid, std_day,
                         cmap='coolwarm',
                         transform=ccrs.PlateCarree())

     cbar = plt.colorbar(plot, ax=ax, orientation='vertical', pad=0.05, shrink=0.7)
     cbar.set_label('Standard Deviation of Bloom Day', fontsize=11)

     ax.set_title('Standard Deviation of Day of Maximum Chlorophyll-a Across All Grid Cells', fontsize=13)

     plt.tight_layout()
     plt.savefig(r"C:\Users\julia\Desktop\Dissertation\stdev_day_map.png", dpi=150, bbox_inches='tight')
     plt.show(block=True)
     print("Plot saved and displayed")

#testing block and uploading and testing the new nc datsets 
if __name__ == "__main__":
    filepath     = r"C:\Users\julia\Desktop\Dissertation\chl_8day_cleaned.nc"
    results_path = r"C:\Users\julia\Desktop\Dissertation\bloom_results.nc"

    
    # --- run this block ONCE to calculate and save the results ---
    #after saving the results, comment this block out so you don't have to rerun it
    chla_data   = nc.Dataset(filepath)
    lat         = chla_data.variables['latitude'][:]
    lon         = chla_data.variables['longitude'][:]
    years       = list(range(1999, 2019))
    std_grid    = calculate_std_annual_maximum(chla_data, years)
    annual_avg  = avg_annual_max(chla_data, years)
    avg_day = avg_annual_day(chla_data, years)
    std_day     = stdev_day(chla_data, years)
    chla_data.close()
    save_results_to_file(std_grid, annual_avg, lat, lon, results_path)


    #plotting functions and change the file path to the results path in order to just run on the new saved file data 
    # avg_day, std_day, std_grid, annual_avg, lat, lon = load_results_from_file(results_path)

    # # plot
    # plot_avg_distribution(annual_avg)
    # map_stdev_grid(std_grid, lat, lon)
    # map_max_avg(lat, lon, annual_avg)

   