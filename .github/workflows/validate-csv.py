import requests
import pandas as pd
import numpy as np
import json
import sys


with open('country_by_continent.json') as f:
    country_data = json.load(f)


def check_country(row):
    country = row['Country']
    if country not in country_data.keys():
        return f"Not a valid country: {country}"
    return None


def check_url(row):
    url = row['URL']
    if not isinstance(url, str) and np.isnan(url):
        return None  # URL is optional

    domains_to_skip = [
        'www.bom.gov.au',  # this website rejects automated http requests
        'rratlas.energy.gov.sa',  # times out and reaches max retries
        'climate.lzu.edu.cn',
        'niwe.res.in',
        'dwd.de/DE/forschung/atmosphaerenbeob',
    ]
    for domain in domains_to_skip:
        if domain in url:
            return None  # URL is a special case; don't check it

    # use HEAD request for efficiency
    response = requests.head(url, timeout=60)
    try:
        response.raise_for_status()
    except Exception as e:
        return "invalid URL: " + str(e)

    return None


def check_elevation(row):
    elevation = row['Elevation']
    if np.isnan(elevation):
        return None  # elevation is optional

    if not isinstance(elevation, float):
        return f"Elevation must be type 'float': {elevation}"
    if not -500 < elevation < 9000:
        return f"Elevation must be between -500 and 9000 meters: {elevation}"

    return None


def check_coordinates(row):
    lat = row['Latitude']
    lon = row['Longitude']

    if not isinstance(lat, float):
        return f"Latitude must be type 'float': {lat}"
    if not -90 <= lat <= 90:
        return f"Latitude must be between -90 and 90: {lat}"

    if not isinstance(lon, float):
        return f"Longitude must be type 'float': {lon}"
    if not -180 <= lon <= 180:
        return f"Longitude must be between -180 and 180: {lon}"

    return None


def check_data_availability(row):
    data_availability = row['Data availability']
    if data_availability not in ['Freely', 'Upon request', 'Not available', '']:
        return f"Not a valid entry for Data Availability: {data_availability}"


validation_functions = [
    check_country,
    check_url,
    check_elevation,
    check_coordinates,
    check_data_availability,
]

if __name__ == "__main__":

    filename = 'solarstations.csv'
    df = pd.read_csv(filename)

    found_a_problem = False

    for i, row in df.iterrows():
        for func in validation_functions:
            try:
                msg = func(row)
                if msg is None:
                    continue
            except Exception as e:
                msg = str(e)

            check_name = func.__name__
            line_num = i + 2  # +1 for header, +1 for zero-based indexing
            log_output = f"solarstations.csv, line {line_num}: {msg}"
            print(log_output)

            found_a_problem = True

    if found_a_problem:
        sys.exit(1)  # fail the GH Action
