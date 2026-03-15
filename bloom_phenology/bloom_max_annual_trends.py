#chla-max time series for each year 

#import necessary libraries 
import pandas as pd 
import numpy as np 
import matplotlib.pyplot as plt
import netCDF4 as nc
from bloom_maximum import find_chla_maximum

def plot_bloom_maximum(data, years): 
    '''Plots the mean bloom maximum across all grid cells for each year
    
    Parameters: 
    data: the dataset 
    years: list of years to analyze 
    
    outputs: plot showing the trends 
    '''
    #create an empty list 
    mean_climax_day = []

    for year in years: 
        #call in previous function 
        bloom_max_dates, bloom_max_chla = find_chla_maximum(chla_data, year)

        # convert each date to day of year (1-365) for each grid cell
        day_grid = np.full(bloom_max_dates.shape, np.nan)

        for i in range(bloom_max_dates.shape[0]):
            for j in range(bloom_max_dates.shape[1]):
                date = bloom_max_dates[i, j]
                if date is not None:
                    day_grid[i, j] = date.timetuple().tm_yday   # e.g. March 15 -> 74

        # average the climax day across all grid cells for this year
        mean_day = np.nanmean(day_grid)
        mean_climax_day.append(mean_day)
        print(f"{year}: mean bloom maximum day of year = {mean_day:.1f}")
# --- plotting ---
    mean_climax_day = np.array(mean_climax_day)

    fig, ax = plt.subplots(figsize=(10, 5))

    # plot the mean day of year for each year
    ax.plot(years, mean_climax_day, marker='o', color='steelblue',
            linewidth=1.5, markersize=6, label='Mean bloom maximum Day of Year')

    # fit and plot a trend line
    z     = np.polyfit(years, mean_climax_day, 1)   # z[0] = slope, z[1] = intercept
    p     = np.poly1d(z)
    trend = p(years)

    ax.plot(years, trend, color='red', linewidth=2,
            linestyle='--', label=f'Trend (slope = {z[0]:.2f} days/year)')

    # labels and formatting
    ax.set_xlabel('Year')
    ax.set_ylabel('Day of Year (1-365)')
    ax.set_title('Bloom Maximum Day of Year — Mean Across All Grid Cells')
    ax.legend()
    ax.grid(True, alpha=0.3)

    plt.tight_layout()
    plt.show()


if __name__ == "__main__":
    filepath  = "chl_8day_1999_2018_cleaned.nc"
    chla_data = nc.Dataset(filepath)
    years = list(range(1999, 2019))
    plot_bloom_maximum(chla_data, years)