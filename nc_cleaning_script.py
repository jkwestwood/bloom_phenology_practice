#clean the .nc files 
#working in the Uk where data is very cloudy and if there are not enough data values to get 
import numpy as np
import netCDF4 as nc

def clean_nc_chla_file(chla_data):
    """
    Removes grid cells with more than 50% missing data.
    
    Parameters:
    chla_data (netCDF4.Dataset): The netCDF dataset containing chlorophyll-a data.
    
    Outputs:
    valid_mask (2D boolean array): True = valid grid cell (less than 50% missing)
    """
    #extract chla data 
    chla = chla_data.variables['chla'][:]

    # count NaNs per cell, divide by total timesteps, keep under 50%
    mask_data = (np.sum(np.isnan(chla), axis=0) / chla.shape[0]) < 0.5 

    chla[:, ~mask_data] = np.nan #only selects the grid cells that are valid and sets the rest to NaN

    return mask_data, chla

def save_clean_chla_to_nc(chla_data, filepath_out):
    """
    Saves the cleaned chlorophyll-a dataset to a new netCDF file.

    Parameters:
    chla_data (netCDF4.Dataset): The netCDF dataset containing chlorophyll-a data.
    filepath_out (str): The path to the output netCDF file.
    """
    # clean the data
    mask_data, chla_clean = clean_nc_chla_file(chla_data)

    # extract original variables
    lat  = chla_data.variables['latitude'][:]
    lon  = chla_data.variables['longitude'][:]
    time = chla_data.variables['time']

    # create new netCDF file
    new_nc = nc.Dataset(filepath_out, 'w')

    # copy dimensions from original file
    new_nc.createDimension('time',      len(time[:]))
    new_nc.createDimension('latitude',  len(lat))
    new_nc.createDimension('longitude', len(lon))

    # create and fill variables — copying units and attributes from original
    new_time      = new_nc.createVariable('time',      'f4', ('time',))
    new_lat       = new_nc.createVariable('latitude',  'f4', ('latitude',))
    new_lon       = new_nc.createVariable('longitude', 'f4', ('longitude',))
    new_chla      = new_nc.createVariable('chla',      'f4', ('time', 'latitude', 'longitude'), fill_value=np.nan)

    # copy units metadata from original file so time conversion still works
    new_time.units    = time.units
    new_time.calendar = getattr(time, 'calendar', 'standard')

    # fill variables with data
    new_time[:]  = time[:]
    new_lat[:]   = lat
    new_lon[:]   = lon
    new_chla[:]  = chla_clean

    new_nc.close()
    print(f"Saved cleaned data to {filepath_out}")


if __name__ == "__main__":
    filepath  = "chl_8day_1999_2018_Julia.nc"
    chla_data = nc.Dataset(filepath)

    save_clean_chla_to_nc(chla_data, filepath_out="chl_8day_cleaned.nc")

    chla_data.close()




