#Mapping file for inputted information 
#import all the necessary libraries 
import cartopy.crs as ccrs
import cartopy.feature as cfeature
import matplotlib.pyplot as plt
import numpy as np

#distribution plots 
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

#Maps

# def map_stdev_grid(std_grid, lat, lon):
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


# def map_max_avg(lat, lon, data): 
#     '''
#     Plots the maximum annual average chlorophyll-a
#     concentration for each grid cell on a map.

#     Parameters:
#     std_grid  : 2D array of annual avg (n_lat, n_lon)
#     lat       : 1D array of latitude values
#     lon       : 1D array of longitude values '''

if __name__ == '__main__': 
      # plot
    plot_avg_distribution(annual_avg)
    map_stdev_grid(std_grid, lat, lon)
    map_max_avg(lat, lon, annual_avg)