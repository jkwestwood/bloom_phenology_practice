#PACE Exploratory data for the western part of scotland 
#based off of the NASA Hackathon Code for PACE data 

#import all the essential libraries
import pandas as pd 
import matplotlib.pyplot as plt
import earthaccess
import xarray as xr
import cartopy.crs as ccrs

auth = earthaccess.login(persist=True)

# Search for chlorophyll-a data product (CHL)
# Level 3 Monthly data for 12 months-- 1 degree resolution 
#has broader spatial resolution for the data products 
results = earthaccess.search_data(
    short_name='PACE_OCI_L3M_CHL',  # Chlorophyll-a product
    temporal=("2024-03-01", "2025-02-28"),  # 12 months of data from first month data was available to the end of February 2025
    granule_name="*.MO.*.0p1deg.*"  # Monthly (MO), 0.1 degree resolution
)

#check to make sure there are 12 files 
print(f"Found {len(results)} monthly files")

# Open all files
fileset = earthaccess.open(results)

# Load data with xarray, combining along time dimension -- uses the cloud not my own laptop so allows for large data handling 
ds = xr.open_mfdataset(
    fileset,
    combine="nested",
    concat_dim="time"
)

print(f"Dataset has {ds.dims['time']} time steps")
print(f"Dataset size: {ds.nbytes / 1e9:.2f} GB")

# Create time coordinate for the 12 months
n_times = ds.dims['time']
t = pd.date_range(start="2024-03-01", periods=n_times, freq="MS")
ds = ds.assign_coords(time=t)

# Select chlorophyll-a and subset for western Scotland
# Bounding box: lon (-9 to -4), lat (53 to 60) 
#format is lat_max, lat_min, lon_min, lon_max
chl = ds["chlor_a"].sel(
    lat=slice(60, 53),    # Note: slice goes from high to low for descending coords
    lon=slice(-9, -4)
)
print(f"Chlorophyll-a data shape: {chl.shape}")
print(f"Time range: {chl.time.min().values} to {chl.time.max().values}")

# Create the 12-month chl-a plot
fig = plt.figure(figsize=(16, 10))

chl.plot(
    col="time",
    col_wrap=4,
    robust=True,
    cmap='viridis',
    size=3,                    # Controls height of each subplot
    aspect=1.2,                # Controls width/height ratio (>1 = wider, <1 = taller)
    subplot_kws={"projection": ccrs.epsg(3857)},
    transform=ccrs.PlateCarree(),
    cbar_kwargs={'label': 'Chlorophyll-a (mg/m³)'}
)

# Add coastlines to each subplot for visualization 
for ax in plt.gcf().axes:
    if hasattr(ax, 'coastlines'):
        ax.coastlines(resolution='10m', color='black', linewidth=0.5)
        ax.gridlines(draw_labels=False, alpha=0.3)

#plt.suptitle('Chlorophyll-a Concentration - Western Coast of Scotland (12 Months)', 
             #fontsize=12, y=1.00)
#plt.tight_layout()
plt.savefig('scotland_chl_12months.png', dpi=300, bbox_inches='tight')
plt.show()




# # Calculate and plot monthly statistics
# monthly_mean = chl.mean(dim=['lat', 'lon'])
# monthly_std = chl.std(dim=['lat', 'lon'])

# fig, ax = plt.subplots(figsize=(12, 8))
# monthly_mean.plot(ax=ax, marker='o', linewidth=2, label='Mean')
# ax.fill_between(
#     range(len(monthly_mean)), 
#     monthly_mean - monthly_std, 
#     monthly_mean + monthly_std, 
#     alpha=0.3, 
#     label='±1 Std Dev'
# )
# ax.set_xlabel('Month')
# ax.set_ylabel('Chlorophyll-a (mg/m³)')
# ax.set_title('Monthly Mean Chlorophyll-a Concentration - Western Scotland')
# ax.legend()
# ax.grid(alpha=0.3)
# plt.xticks(rotation=45)
# plt.tight_layout()
# plt.savefig('scotland_chl_timeseries.png', dpi=300, bbox_inches='tight')
# plt.show()