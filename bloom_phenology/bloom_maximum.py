#created by Julia on 17/06/2024``

#code that imports previous functions and extracts information for bloom maximum date for each year 
#for all grid cells 

#import all necessary libraries
import numpy as np
import netCDF4 as nc
import pandas as pd
import matplotlib.pyplot as plt
#import functions from the bloom phenology coding script 
from bloom_phenology_coding_script import chla_time_series_grid_cell
from bloom_phenology_coding_script import find_grid_maximum       

def find_chla_maximum(data, year):
    """
    Finds the bloom maximum (peak chlorophyll-a concentration) for entire grid for  specified year.

    Parameters:
    data (netCDF4.Dataset): The netCDF dataset containing chlorophyll-a data.
    year (int): The year for which to find the bloom maximum.
    
    Outputs: 
    tuples of bloom maximum date and bloom maximum chlorophyll-a concentration for each grid cell in the dataset. 
    """

    lat = data.variables['latitude'][:] #calls on the laitude key and exstracts all the numbers
    lon = data.variables['longitude'][:]

    #create 2 empty arrays one for chla and one for dates 
    # use the built in numpy full function and the nan function to assign NaN to grid cells 
    bloom_max_dates = np.full((len(lat), len(lon)),None, dtype = object)
    bloom_max_chla = np.full((len(lat), len(lon)), np.nan)

    #create a nested loop to loop throiugh the range of all lat and lon cells 

    for lat_idx in range(len(lat)):
        for lon_idx in range(len(lon)):
            bloom_date, bloom_chla = chla_time_series_grid_cell(data, lat_idx, lon_idx, year)

            #line to keep NaN values of empty grid cells instead of 0
            if np.all(np.isnan(bloom_chla)):
                continue
            
            #line to get the maximum value
            # calls on the numpy nanargmax functionm which finds the index of the maximum value ignoring Nan values

            max_idx = np.nanargmax(bloom_chla) #use the numpy function to get the index of the maximum value in the bloom_chla array, ignoring NaN values.
                
            bloom_max_dates[lat_idx, lon_idx] = bloom_date[max_idx] #use the index of the maximum value to get the corresponding date from the bloom_date array and assign it to the bloom_max_dates array at the corresponding lat and lon index.
            bloom_max_chla[lat_idx, lon_idx] = bloom_chla[max_idx] #use the index of the maximum value to get the corresponding chlorophyll-a concentration from the bloom_chla array and assign it to the bloom_max_chla array at the corresponding lat and lon index.

    return bloom_max_dates, bloom_max_chla

#create a function to save the bloom maximum date and bloom maximum chlorophyll-a concentration 
# for each grid cell in the dataset to a csv file.
def save_bloom_maximum_to_csv(chla_data, year, filepath_out):
    """
    Saves the bloom maximum (peak chlorophyll-a concentration) for every grid cell to a CSV file.

    Parameters:
    chla_data (netCDF4.Dataset): The netCDF dataset containing chlorophyll-a data.
    year: The year for which to find the bloom maximum.
    filepath_out: The path to the output CSV file.

    Outputs:
    df (pd.DataFrame): A dataframe containing the lat, lon, date and maximum chla for every grid cell.
    """
    lat = chla_data.variables['latitude'][:]
    lon = chla_data.variables['longitude'][:]

    # call previous function to get the bloom max dates and chla for every grid cell
    bloom_max_dates, bloom_max_chla = find_chla_maximum(chla_data, year)

    # build a flat list of rows by looping over every grid cell
    rows = []
    for lat_idx in range(len(lat)):
        for lon_idx in range(len(lon)):
            rows.append({
                'latitude':  lat[lat_idx],
                'longitude': lon[lon_idx],
                'date':      bloom_max_dates[lat_idx, lon_idx],
                'max_chla':  bloom_max_chla[lat_idx, lon_idx]
            })

    # convert to dataframe and save to CSV
    df = pd.DataFrame(rows)
    df.to_csv(filepath_out, index=False)
    print(f"Saved {len(df)} grid cells to {filepath_out}")

    return df


#testing block
if __name__ == "__main__":
    filepath  = "chl_8day_1999_2018_cleaned.nc"
    chla_data = nc.Dataset(filepath)

    year = 2013

    bloom_dates, bloom_chla = find_chla_maximum (chla_data, year)
    df = save_bloom_maximum_to_csv(chla_data=chla_data, year=year, filepath_out=f"bloom_maximum_{year}.csv")
    print(df.head())

    chla_data.close()
   
