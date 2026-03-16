#chla-max time series for each year 

#import necessary libraries 
import pandas as pd 
import matplotlib.pyplot as plt
import netCDF4 as nc
from bloom_maximum import find_chla_maximum

def plot_bloom_maximum_trends(date, max_chla): 
    '''Plots the bloom maximum trend for each grid cell in one year
    
    Parameters: 

    imports a previous function from bloom_maximum.py to extract the bloom maximum date for each grid cell in the dataset for the specified year
    
    outputs: plot showing the yearly trend 

    '''

    plt.plot(date, max_chla)
    plt.xlabel('Date')
    plt.ylabel('Bloom Maximum Chlorophyll-a Concentration (mg/m³)')
    plt.title('Bloom Maximum Trend for Each Grid Cell in 1999')
    plt.show()

  
   
if __name__ == "__main__":
    filepath  = r"C:\Users\julia\Desktop\Dissertation\bloom_maximum_csv\bloom_maximum_1999.csv"
    chla_data = pd.read_csv(filepath)

    # convert date column to datetime, invalid/missing dates become NaT
    chla_data['date'] = pd.to_datetime(chla_data['date'], errors='coerce')

    # drop rows where either date or max_chla is missing
    chla_data = chla_data.dropna(subset=['date', 'max_chla'])

    # groupby date and take the maximum chla across all grid cells for that day
    daily_max = chla_data.groupby('date')['max_chla'].max().reset_index()

    # sort by date just in case it is not already ordered
    daily_max = daily_max.sort_values('date')

    print(daily_max.head())

    plot_bloom_maximum_trends(daily_max['date'], daily_max['max_chla'])

    plt.savefig('bloom_maximum_plot_1999')
    
