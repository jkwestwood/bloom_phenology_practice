#Bloom apex and bloom phenology code for The UK 
#import all necessary libraries 
from datetime import datetime
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import netCDF4 as nc

def chla_time_series_grid_cell(chla_data, lat_idx, lon_idx, year):
    """
    Extracts the chlorophyll-a concentration time series for a specified grid cell and year.

    Parameters:
    chla_data (netCDF4.Dataset): The netCDF dataset containing chlorophyll-a data.
    lat_idx (int): The latitude index of the grid cell.
    lon_idx (int): The longitude index of the grid cell.
    year (int): The year for which to extract the data.

    Returns:
    tuple: time_year (array of datetimes), chla_year (array of chl-a values)
    """
    # extract data variables from the netCDF file
    lat  = chla_data.variables['latitude'][:]
    long = chla_data.variables['longitude'][:]
    time = chla_data.variables['time']
    chla = chla_data.variables['chla'][:]

    # correct the time
    time_dates = nc.num2date(time[:], units=time.units, calendar=getattr(time, 'calendar', 'standard'))
    time_dates = np.array([datetime(d.year, d.month, d.day) for d in time_dates])

    # filter to the requested year
    year_mask = np.array([d.year == year for d in time_dates])
    time_year = time_dates[year_mask]
    chla_year = chla[year_mask, lat_idx, lon_idx]

    # mask fill/missing values
    chla_year = np.ma.filled(chla_year, fill_value=np.nan)

    return time_year, chla_year          # ← return so other functions can use these


def plot_chla_time_series_grid_cell(chla_data, lat_idx, lon_idx, year):
    """
    Plots the chlorophyll-a concentration time series for a specified grid cell and year.

    Parameters:
    chla_data (netCDF4.Dataset): The netCDF dataset containing chlorophyll-a data.
    lat_idx (int): The latitude index of the grid cell.
    lon_idx (int): The longitude index of the grid cell.
    year (int): The year for which to plot the data.

    Returns:
    None: Displays a plot of chlorophyll-a concentration over time for the specified grid cell and year.
    """
    # call previous function to get the extracted data   ← reusing chla_time_series_grid_cell
    time_year, chla_year = chla_time_series_grid_cell(chla_data, lat_idx, lon_idx, year)

    fig, ax = plt.subplots(figsize=(12, 5))
    ax.plot(time_year, chla_year, marker='o', linestyle='-', color='green', markersize=4, label='Chl-a')
    ax.set_title(f'Chlorophyll-a Concentration for Grid Cell ({lat_idx}, {lon_idx}) in {year}')
    ax.set_xlabel('Date')
    ax.set_ylabel('Chlorophyll-a Concentration (mg/m³)')
    ax.xaxis.set_major_formatter(mdates.DateFormatter('%b'))
    ax.xaxis.set_major_locator(mdates.MonthLocator())
    plt.xticks(rotation=45)
    ax.grid(True, alpha=0.3)
    ax.legend()
    plt.tight_layout()
    plt.show()


def find_grid_maximum(chla_data, lat_idx, lon_idx, year):
    """
    Finds the bloom maximum (peak chlorophyll-a concentration) for a specified grid cell and year.

    Parameters:
    chla_data (netCDF4.Dataset): The netCDF dataset containing chlorophyll-a data.
    lat_idx (int): The latitude index of the grid cell.
    lon_idx (int): The longitude index of the grid cell.
    year (int): The year for which to find the bloom maximum.

    Returns:
    tuple: bloom_max_date (datetime), bloom_max_chla (float)
    """
    # call previous function to get the extracted data  
    time_year, chla_year = chla_time_series_grid_cell(chla_data, lat_idx, lon_idx, year)

    # find bloom maximum
    max_idx        = np.nanargmax(chla_year)
    bloom_max_date = time_year[max_idx]
    bloom_max_chla = chla_year[max_idx]

    return bloom_max_date, bloom_max_chla


#testing block 
if __name__ == "__main__":
    #load the dataset
    filepath  = "chl_8day_cleaned.nc"
    chla_data = nc.Dataset(filepath)
 
 # 20 46
    lat_idx = 20
    lon_idx = 46
    year    = 2005

    plot_chla_time_series_grid_cell(chla_data=chla_data, lat_idx=lat_idx, lon_idx=lon_idx, year=year)

    bloom_date, bloom_chla = find_grid_maximum(chla_data=chla_data, lat_idx=lat_idx, lon_idx=lon_idx, year=year)
    print(f"Bloom maximum: {bloom_chla:.3f} mg/m³ on {bloom_date.strftime('%d %b %Y')}")

    chla_data.close()



# # Original Monolithic code for bloom phenology, will be converted to a function after testing and analysis of the grid cells.
# # extract data variables from the netCDF file
# lat = chla_data.variables['latitude'][:]
# long = chla_data.variables['longitude'][:]
# time = chla_data.variables['time']
# chla = chla_data.variables['chla'][:]

# #correct the time 
# time_dates = nc.num2date(time[:], units=time.units, calendar=getattr(time, 'calendar', 'standard'))
# time_dates = np.array([datetime(d.year, d.month, d.day) for d in time_dates])

# #extract grid by grid cell data for the UK
# #extract the index for a specified grid cell and year
# lat_idx = 10
# lon_idx = 10
# year = 2018

# #filter to the requested year 
# year_mask = np.array([d.year == year for d in time_dates]) 
# time_year = time_dates[year_mask]
# chla_year = chla[year_mask, lat_idx, lon_idx]

# # Mask fill/missing values
# chla_year = np.ma.filled(chla_year, fill_value=np.nan)


# #plot the entire year of chl-a data for the specified grid cell
# # plot the entire year of chl-a data for the specified grid cell
# fig, ax = plt.subplots(figsize=(12, 5))
# ax.plot(time_year, chla_year, marker='o', linestyle='-', color='green', markersize=4, label='Chl-a')  # ← time_year and chla_year not time and chla
# ax.set_title(f'Chlorophyll-a Concentration for Grid Cell ({lat_idx}, {lon_idx}) in {year}')
# ax.set_xlabel('Date')
# ax.set_ylabel('Chlorophyll-a Concentration (mg/m³)')
# ax.xaxis.set_major_formatter(mdates.DateFormatter('%b'))
# ax.xaxis.set_major_locator(mdates.MonthLocator())
# plt.xticks(rotation=45)
# ax.grid(True, alpha=0.3)
# ax.legend()
# plt.tight_layout()
# plt.show()

# chla_data.close()