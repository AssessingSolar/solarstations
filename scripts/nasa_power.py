"""Functions to retrieve data from NASA POWER."""

import pandas as pd
import requests
import numpy as np

DEFAULT_PARAMETERS = [
    'ALLSKY_SFC_SW_DNI', 'ALLSKY_SFC_SW_DIFF', 'ALLSKY_SFC_SW_DWN']

URL = 'https://power.larc.nasa.gov/api/temporal/climatology/regional?'


def get_nasa_power(latitude, longitude, start='2001-01-01', end='2020-01-01',
                   community='RE', parameters=DEFAULT_PARAMETERS, url=URL):

    latitude_min, latitude_max = latitude  # bottom, top
    longitude_min, longitude_max = longitude  # left, right

    params = {
        'start': pd.Timestamp(start).year,
        'end': pd.Timestamp(end).year,
        'latitude-min': latitude_min,
        'latitude-max': latitude_max,
        'longitude-min': longitude_min,
        'longitude-max': longitude_max,
        'community': community,
        'parameters': ','.join(parameters),
        'format': 'json',
        'user': 'DAVE',
    }

    res = requests.get(url, params=params)
    res.raise_for_status()

    meta = res.json()['header']
    meta['parameters'] = res.json()['parameters']

    data = pd.json_normalize(data=res.json()['features'])

    data = data.replace(-999, np.nan)

    data = data.rename(columns={
        'properties.parameter.ALLSKY_SFC_SW_DWN.ANN': 'GHI_typical_kWh_m2',
        'properties.parameter.ALLSKY_SFC_SW_DIFF.ANN': 'DHI_typical_kWh_m2',
        'properties.parameter.ALLSKY_SFC_SW_DNI.ANN': 'DNI_typical_kWh_m2',
    })

    data[['longitude', 'latitude']] = \
        pd.DataFrame(data['geometry.coordinates'].to_list()).iloc[:, :-1]

    data = data.set_index(['latitude', 'longitude'])

    data = \
        data[['GHI_typical_kWh_m2', 'DHI_typical_kWh_m2', 'DNI_typical_kWh_m2']]

    data = data.multiply(365)  # convert kWh/m2/day to kWh/m2/yr

    return data, meta


# %%
step_size = 10  # max allowed box dimension
latitudes = np.arange(-90, 90, step_size)
longitudes = np.arange(-180, 180, step_size)

dfs = []
for lat in latitudes:
    latitude = [lat, lat + step_size]
    for lon in longitudes:
        longitude = [lon, min(lon + step_size, 179)]
        data, _ = get_nasa_power(latitude, longitude)
        dfs.append(data)

df = pd.concat(dfs, axis='rows')

df.round(0).to_csv('data/nasa_power_annual_irradiance_global.csv')
