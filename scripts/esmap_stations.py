import pandas as pd
import requests

url = 'https://energydata.info/api/3/action/datastore_search?resource_id=da73e4b1-7cb1-4c9c-8e54-594fad190a60&limit=500'

response = requests.get(url)

esmap = pd.DataFrame(response.json()['result']['records'])

columns_dict = {
    'Nearest Settlement': 'Station name',
    'Site Name': 'Abbreviation',
    # 'Project Founder': 'Network',
    # Could also use 'documents___reports_url'
    'Measurement Data URL': 'URL',
    'Equipment Owner': 'Owner',
}

country_corrections = {
    'Guinée-Bissau': 'Guinea-Bissau',  # Change to English spelling
    'Bénin': 'Benin',  # Change to English spelling
    'Guinée': 'Guinea',  # Change to English spelling
}

esmap = esmap.rename(columns=columns_dict)

esmap['Network'] = 'ESMAP'

pd.set_option('future.no_silent_downcasting', True)  # avoid warning
esmap['Tier'] = ''
esmap.loc[esmap['Equipment Type'].str.strip().str.contains('Tier1').fillna(False), 'Tier'] = 1
esmap.loc[esmap['Equipment Type'].str.strip().str.contains('Tier2').fillna(False), 'Tier'] = 2

esmap['State'] = ''
esmap['Data availability'] = 'Freely'

esmap['Instrumentation'] = ''
esmap.loc[esmap['Tier'] == 1, 'Instrumentation'] = 'G;B;D'

esmap['Comment'] = ''
esmap.loc[esmap['Tier'] != 1, 'Comment'] = 'Instrument and components have not been checked manually.'

start_year = esmap['commission_date__m_d_y_'].str[:4]
end_year = esmap['End of Measurement Campaign'].str[-4:].astype(str).str.replace('None', '')
esmap['Time period'] = start_year + '-' + end_year
esmap.loc[start_year == end_year, 'Time period'] = start_year

# check if stations exists already
stations = pd.read_csv('../solarstations.csv')
duplicate_rows = []
for index, row in esmap.iterrows():
    if row['Station name'] in stations['Station name'].values:
        if row['Station name'] not in ['Hyderabad', 'Peshawar']:
            duplicate_rows.append(index)
    if row['Country'] in country_corrections.keys():
        esmap.loc[index, 'Country'] = country_corrections[row['Country']]

esmap = esmap.drop(duplicate_rows)

header = 'Station name,Abbreviation,State,Country,Latitude,Longitude,Elevation,Time period,Network,Owner,Comment,URL,Data availability,Instrumentation'

columns = header.split(',')

esmap[columns].to_csv('../esmap_stations.csv', sep=',', index=False)
