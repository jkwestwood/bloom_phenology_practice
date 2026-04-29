#Moana product exploration
# #code is based on https://www.youtube.com/watch?v=9pH9j0qXtZA
#import libraries
import earthaccess 
import xarray as xr
import matplotlib.pyplot as plt
import numpy as np
import cartopy.crs as ccrs
import cartopy.feature as cfeature
import gc 

#add authentication
auth = earthaccess.login(persist=True)

results = earthaccess.search_data(
    short_name='PACE_OCI_L4M_MOANA', 
    temporal=('2024-09-01', '2024-09-02'),
    granule_name='*8D*'
)

print(f"Found {len(results)} granules")
for res in results:
    print(res.data_links())


fileset = earthaccess.open(results)
ds = xr.open_dataset(fileset[0])

phyto_info = {
    'prococcus_moana': {'color': 'green',   'label': 'Prochlorococcus'},
    'syncoccus_moana': {'color': 'cyan',    'label': 'Synechococcus'},
    'picoeuk_moana':{'color': 'magenta', 'label': 'Picoeukaryotes'}
}

# UK bounding box — lat is descending so slice high tolow
LON_MIN, LON_MAX = -15, 10
LAT_MIN, LAT_MAX =  45, 65

ds_uk = ds.sel(
    lat=slice(LAT_MAX, LAT_MIN),   # 65 → 45 (descending)
    lon=slice(LON_MIN, LON_MAX)
)

print(f"UK subset shape: {ds_uk['syncoccus_moana'].shape}")  # sanity check

#  1. UK REGIONAL MAPS 
fig, axes = plt.subplots(
    1, 3, figsize=(15, 5),
    subplot_kw={'projection': ccrs.PlateCarree()}
)
fig.suptitle('Phytoplankton around the UK – PACE MOANA (Aug–Sep 2024)',
             fontsize=13, fontweight='bold')

for ax, (var, info) in zip(axes, phyto_info.items()):
    data = ds_uk[var].values  # plain numpy, no squeeze needed

    im = ax.pcolormesh(
        ds_uk['lon'].values,
        ds_uk['lat'].values,
        data,
        transform=ccrs.PlateCarree(),
        cmap='plasma',
        shading='nearest'   # avoids the shape mismatch entirely
    )
    ax.add_feature(cfeature.LAND, color='lightgrey', zorder=1)
    ax.add_feature(cfeature.COASTLINE, linewidth=0.6, zorder=2)
    ax.add_feature(cfeature.BORDERS, linewidth=0.4, zorder=2)
    ax.set_extent([LON_MIN, LON_MAX, LAT_MIN, LAT_MAX], crs=ccrs.PlateCarree())

    gl = ax.gridlines(draw_labels=True, linewidth=0.3, alpha=0.5)
    gl.top_labels = False
    gl.right_labels = False

    ax.set_title(info['label'], fontsize=11, color=info['color'])
    plt.colorbar(im, ax=ax, orientation='horizontal',
                 pad=0.08, label='cells mL⁻¹', shrink=0.9)

plt.tight_layout()
plt.savefig('uk_maps.png', dpi=150, bbox_inches='tight')
plt.show()


# 2. LATITUDINAL PROFILES (50–60°N) 
# lat descending, so slice(60, 50)
syn  = ds['syncoccus_moana'].sel(lat=slice(60, 50)).median(dim='lon')
pro  = ds['prococcus_moana'].sel(lat=slice(60, 50)).median(dim='lon')
pico = ds['picoeuk_moana'].sel(lat=slice(60, 50)).median(dim='lon')

fig, ax = plt.subplots(figsize=(6, 8))

ax.plot(syn.values,  syn['lat'].values,  color='cyan',    lw=2, label='Synechococcus')
ax.plot(pro.values,  pro['lat'].values,  color='green',   lw=2, label='Prochlorococcus')
ax.plot(pico.values, pico['lat'].values, color='magenta', lw=2, label='Picoeukaryotes')

ax.set_xlabel('Median cell concentration (cells mL⁻¹)', fontsize=11)
ax.set_ylabel('Latitude (°N)', fontsize=11)
ax.set_title('Latitudinal variation in phytoplankton\n(50–60°N, Aug–Sep 2024)', fontsize=12)
ax.legend(fontsize=10)
ax.grid(True, alpha=0.3)

plt.tight_layout()
plt.savefig('latitudinal_profiles.png', dpi=150, bbox_inches='tight')
plt.show()

# 3. LOG SCALE MAPS (the data range is huge~ 0 to 2.8 billion shows greater variability, so log scale is more informative) 
from matplotlib.colors import LogNorm
    
fig, axes = plt.subplots(
    1, 3, figsize=(15, 5),
    subplot_kw={'projection': ccrs.PlateCarree()}
)
fig.suptitle('Phytoplankton UK (log scale) – PACE MOANA (Aug–Sep 2024)',
             fontsize=13, fontweight='bold')

for ax, (var, info) in zip(axes, phyto_info.items()):
    data = ds_uk[var].values
    # Replace 0/negative with NaN for log scale
    data = np.where(data > 0, data, np.nan)

    im = ax.pcolormesh(
        ds_uk['lon'].values,
        ds_uk['lat'].values,
        data,
        transform=ccrs.PlateCarree(),
        cmap='viridis',
        norm=LogNorm(),
        shading='nearest'
    )
    ax.add_feature(cfeature.LAND, color='lightgrey', zorder=1)
    ax.add_feature(cfeature.COASTLINE, linewidth=0.6, zorder=2)
    ax.set_extent([LON_MIN, LON_MAX, LAT_MIN, LAT_MAX], crs=ccrs.PlateCarree())

    gl = ax.gridlines(draw_labels=True, linewidth=0.3, alpha=0.5)
    gl.top_labels = False
    gl.right_labels = False

    ax.set_title(info['label'], fontsize=11, color=info['color'])
    plt.colorbar(im, ax=ax, orientation='horizontal',
                 pad=0.08, label='cells mL⁻¹ (log)', shrink=0.9)

plt.tight_layout()
plt.savefig('uk_maps_log.png', dpi=150, bbox_inches='tight')
plt.show()

#removes any access memory in the RAM to prevent overflow
gc.collect()