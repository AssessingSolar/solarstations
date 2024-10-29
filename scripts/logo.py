import matplotlib.pyplot as plt
from matplotlib.lines import Line2D
import pandas as pd
import cartopy
import cartopy.crs as ccrs

# %%
solarstations_url = 'https://raw.githubusercontent.com/AssessingSolar/solarstations/main/solarstations.csv'
esampstations_url = 'https://raw.githubusercontent.com/AssessingSolar/solarstations/main/esmap_stations.csv'

solarstations = pd.read_csv(solarstations_url)
esmap_stations = pd.read_csv(esampstations_url)
stations = pd.concat([solarstations, esmap_stations], axis='rows', ignore_index=True)

stations.iloc[:3, :8]  # Show part of the DataFrame

# %%

def station_status(time_period):
    if time_period.endswith('-'):
        return 'Active'
    elif (time_period == '') | time_period.endswith('?'):
        return 'Unknown'
    else:
        return 'Inactive'

stations['Status'] = stations['Time period'].map(station_status)

status_dict = {
    'Active': '#008000',  # Green for active stations
    'Unknown': '#3186cc',  # Blue for stations with unknown status
    'Inactive': '#ff422b',  # Red for inactive stations
}

stations['Color'] = stations['Status'].map(status_dict)

z_order_dict = {'Active': 2, 'Unknown': 1, 'Inactive': 0}
stations['z_order'] = stations['Status'].map(z_order_dict)

stations = stations.sort_values('z_order')

legend_elements = []
for status, color in status_dict.items():
    legend_elements.append(Line2D([0], [0], marker='o', lw=0,
                                  label=status, color='none',
                                  markerfacecolor=color, markersize=7)
    )

# %%

crs = ccrs.Orthographic(
    central_longitude=-25,
    central_latitude=20,
)

fig, ax = plt.subplots(figsize=(4, 4), subplot_kw={'projection': crs})

# Set limits of main map [min_lon, max_lon, min_lat, max_lat]
#ax.set_extent([-179, 180, -90, 90])

# Add land borders, coastline, and gridlines to main map
ax.add_feature(cartopy.feature.LAND, facecolor='lightgrey', alpha=0.7, zorder=0)
ax.coastlines(color='black', lw=0.7, alpha=1, zorder=3)
ax.gridlines(draw_labels=False, dms=True, x_inline=False, y_inline=False, alpha=0.7, lw=0.1, zorder=-1)

# Add points of solar stations
# it is important to specify `transform=ccrs.PlateCarree()` to transform the points from
# regular latitude/longitude (PlateCarree) to the specific map projection
stations.plot.scatter(
    ax=ax, x='Longitude', y='Latitude',
    c='Color', alpha=0.95, s=12, edgecolor='k', lw=0.2,
    transform=ccrs.PlateCarree(), zorder=4)

# Create the figure
# ax.legend(handles=legend_elements, loc='lower left',
#           frameon=False, bbox_to_anchor=[0, 0.2])

ax.patch.set_facecolor('lightyellow')#'#fbf8f1')

fig.savefig('solarstations_map.png', dpi=900, bbox_inches='tight', facecolor="none")
plt.show()
