"""Functions to retrieve data from NASA POWER."""

import pandas as pd
import numpy as np
import requests


DEFAULT_PARAMETERS = [
    'ALLSKY_SFC_SW_DNI', 'ALLSKY_SFC_SW_DIFF', 'ALLSKY_SFC_SW_DWN']

url = 'https://power.larc.nasa.gov/api/temporal/climatology/point'


def get_nasa_power_annual(latitude, longitude, community='RE',
                          parameters=DEFAULT_PARAMETERS):
    """
    Retrieve data from NASA POWER.

    Parameters
    ----------
    latitude : float
        Latitude, north is positive. [degrees]
    longitude : float
        Longitude, east is positive. [degrees]
    community : str, optional
        Community type. The default is 'RE'.
    parameters : TYPE, optional
        List of weather parameters. The default is :const:`DEFAULT_PARAMETERS`.

    Returns
    -------
    data : pd.DataFrame
        Weather data
    meta : dict
        Dictionary with metadata.
    """
    params = {
        'latitude': latitude,
        'longitude': longitude,
        'community': community,
        'parameters': ','.join(parameters),
        'format': 'JSON',
        'user': 'DAVE',
    }

    res = requests.get(url, params=params)

    data = pd.DataFrame(data=res.json()['properties']['parameter'])

    days = np.array(
        [31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31, 365])
    # convert from kWh/m^2/day to kWh/m^2/yr
    data = data.multiply(days, axis='rows')

    data = data.rename(columns={
        'ALLSKY_SFC_SW_DWN': 'GHI_annual_kWh_m2',
        'ALLSKY_SFC_SW_DNI': 'DNI_annual_kWh_m2',
        'ALLSKY_SFC_SW_DIFF': 'DHI_annual_kWh_m2',
    })
    data = data.rename(index={'ANN': 'Annual'})
    data = data.loc['Annual', :]
    meta = {}
    return data, meta
