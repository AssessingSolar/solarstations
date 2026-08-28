```{marimo} python
import marimo as mo
import pandas as pd
import numpy as np
#import kgcpy
```


```{marimo} python
main_url = "https://raw.githubusercontent.com/AssessingSolar/solarstations/refs/heads/main/solarstations.csv"
esmap_url = "https://raw.githubusercontent.com/AssessingSolar/solarstations/refs/heads/main/esmap_stations.csv"
country_by_continent_url = "https://raw.githubusercontent.com/AssessingSolar/solarstations/refs/heads/main/data/country_by_continent.json"
nasa_power_url = "https://raw.githubusercontent.com/AssessingSolar/solarstations/refs/heads/main/data/nasa_power_annual_irradiance_global.csv"

main_stations = pd.read_csv(main_url, dtype={'Tier': str}).fillna('')
esmap_stations = pd.read_csv(esmap_url, dtype={'Tier': str}).fillna('')
stations = pd.concat([main_stations, esmap_stations], axis='rows', ignore_index=True)

country_by_continent = pd.read_json(country_by_continent_url, typ="series").to_dict()

stations['Continent'] = stations['Country'].map(country_by_continent)

#stations['Koeppen Geiger classification'] = stations.apply(lambda x: kgcpy.lookupCZ(x['Latitude'], x['Longitude']), axis=1)
#kg_climates = {'A': 'Tropical', 'B': 'Dry', 'C': 'Temperate', 'D': 'Continental', 'E': 'Polar', 'O': 'Ocean'}
#stations['Koeppen Geiger climate zone'] = stations['Koeppen Geiger classification'].apply(lambda x: kg_climates[x[0]])

instrumentation = stations['Instrumentation'].str.split(';', expand=True)
is_tier_1 = (instrumentation=='G').any(axis=1) & (instrumentation=='B').any(axis=1) & (instrumentation=='D').any(axis=1)
stations['Tier'] = 2 - is_tier_1.astype(int)

annual_irradiance = pd.read_csv(nasa_power_url, index_col=[0, 1])
for index, row in stations.iterrows():
    lat_round = round(row['Latitude']*2-0.5, 0)/2 + 0.25
    lon_round = round(row['Longitude']*2-0.5, 0)/2 + 0.25
    try:
        stations.loc[index, ['GHI_typical_kWh_m2', 'DHI_typical_kWh_m2', 'DNI_typical_kWh_m2']] = \
            annual_irradiance.loc[(lat_round, lon_round), :]
    except KeyError as e:
        pass
    # Manual add data missing from the climatological file (data retrieved from NASA's webinterface)
    if row['Station name'] == 'Funafuti':
        stations.loc[index, ['GHI_typical_kWh_m2', 'DHI_typical_kWh_m2', 'DNI_typical_kWh_m2']] = \
            np.array([5.33*365, 2.12*365, 4.37*365]).astype(int)
    if row['Station name'] == 'South Pole':
        stations.loc[index, ['GHI_typical_kWh_m2', 'DHI_typical_kWh_m2', 'DNI_typical_kWh_m2']] = \
            np.array([3.0*365, 1.38*365, 5.13*365]).astype(int)

stations = stations[~stations['Instrumentation'].str.contains('G;Ds')]  # remove Tier 3 stations

stations = stations.sort_values('Station name', ignore_index=True)

# Write file containing all columns, linked to above
stations.to_csv('./SolarStationsOrg-station-catalog.csv', index=False)

table = mo.ui.table(
    stations,
    pagination=True,
    freeze_columns_left=["Station name"],
    page_size=20,  # default is 10
    show_download=True,
    column_widths={"Station name": 180, "URL": 80},
)
```

```{marimo} python
table
```