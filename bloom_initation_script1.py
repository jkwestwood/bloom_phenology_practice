
#bloom onset repeatability script 
import numpy as np
import netCDF4
from scipy.signal import savgol_filter
import pandas as pd

#look at the previous bloom initiation script and compare it to the new one. 
# The previous script was designed to calculate the bloom onset for a single grid cell and year,
#  while this script it to create a function that can be applied to all grid cells and years in the dataset, 
# and to store the results in a structured format (DataFrame) for further analysis.

def calc_bloom_onset(fp, smooth_window=5, polyorder=2, nan_threshold=0.5):
    '''
    Calculate bloom onset day-of-year for each grid cell and year in a NetCDF file.
    
    Parameters:
        fp             : file path to .nc file
        smooth_window  : Savitzky-Golay window length (default 5)
        polyorder      : Savitzky-Golay polynomial order (default 2)
        nan_threshold  : skip cell if more than this fraction are NaN (default 0.5)
    
    Returns:
        df             : DataFrame with columns [year, lat, lon, onset_doy]
        onset_store    : raw numpy array of shape (years, lat, lon)
    '''
    nc = netCDF4.Dataset(fp)

    #assign variables from the nc file 
    time_var = nc.variables['time'][:]
    time_units = nc.variables['time'].units
    dates = netCDF4.num2date(time_var, time_units)
    years = np.array([d.year for d in dates])

    chl_all = nc.variables['chla'][:]
    lats = nc.variables['latitude'][:]
    lons = nc.variables['longitude'][:]

    lat_size = chl_all.shape[1]
    lon_size = chl_all.shape[2]
    unique_years = np.unique(years)

    onset_store = np.full((len(unique_years), lat_size, lon_size), np.nan)

    # Loop through each year 
    for y, year in enumerate(unique_years):
        #create variables for each individual year 
        yr_mask = years == year
        time_yr = time_var[yr_mask]
        chl_yr = chl_all[yr_mask, :, :]


        #nested loop to go through each cell in the range of lat and lon and calculate the bloom onset for each cell and year
        for i in range(lat_size):
            for j in range(lon_size):
                try:
                    chl = np.ma.filled(chl_yr[:, i, j].astype(float), np.nan)

                    if np.all(np.isnan(chl)) or np.sum(np.isnan(chl)) > len(chl) * nan_threshold:
                        continue

                    nans = np.isnan(chl)
                    x = np.arange(len(chl))
                    chl[nans] = np.interp(x[nans], x[~nans], chl[~nans])

                    chl_smooth = savgol_filter(chl, window_length=smooth_window, polyorder=polyorder)

                    dchl_dt = np.gradient(chl_smooth, time_yr)
                    d2chl_dt2 = np.gradient(dchl_dt, time_yr)

                    min_idx = np.argmin(chl_smooth)
                    for k in range(min_idx, len(chl_smooth) - 1):
                        if dchl_dt[k] > 0 and d2chl_dt2[k] > 0:
                            onset_store[y, i, j] = dates[np.where(yr_mask)[0][k]].timetuple().tm_yday
                            break

                except Exception as e:
                    print(f"Error at year {year}, lat {i}, lon {j}: {e}")
                    continue

        print(f"Done year {year}")

    # Build dataframe
    rows = []
    for y, year in enumerate(unique_years):
        for i in range(lat_size):
            for j in range(lon_size):
                val = onset_store[y, i, j]
                if not np.isnan(val):
                    rows.append({
                        'year': year,
                        'lat': lats[i],
                        'lon': lons[j],
                        'onset_doy': val
                    })

    df = pd.DataFrame(rows)
    nc.close()

    return df, onset_store


# --- Run it ---
df, onset_store = calc_bloom_onset('chl_8day_1999_2018_Julia.nc')

print(df.head(20))
print(df.describe())

# Save to CSV
df.to_csv('bloom_onset.csv', index=False)

# Yearly summary
yearly_summary = df.groupby('year')['onset_doy'].agg(
    mean_onset='mean',
    median_onset='median',
    std_onset='std',
    n_cells='count'
).round(1)

print(yearly_summary)