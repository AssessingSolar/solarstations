import pandas as pd
import requests
url = 'https://energydata.info/api/3/action/datastore_search?resource_id=da73e4b1-7cb1-4c9c-8e54-594fad190a60&limit=500'  
response = requests.get(url)

esmap = pd.DataFrame(response.json()['result']['records'])

columns_dict = {
    'Nearest Settlement': 'Station full name',
    'Site Name': 'Abbreviation',
    'Project Founder': 'Network',
    # Could also use 'documents___reports_url'
    'Measurement Data URL': 'URL',
    'Equipment Owner': 'Owner',
}

esmap = esmap.rename(columns=columns_dict)

esmap['Tier'] = ''
esmap.loc[esmap['Equipment Type'].str.replace(' ', '').str.contains('Tier1')==True, 'Tier'] = 1
esmap.loc[esmap['Equipment Type'].str.replace(' ', '').str.contains('Tier2')==True, 'Tier'] = 2

esmap['State'] = ''
esmap['Data availability'] = 'Freely'

esmap['Components'] = ''
esmap.loc[esmap['Tier']==1, 'Components'] = 'G;B;D'

esmap['Instrument'] = ''
esmap.loc[esmap['Equipment Type'].str.replace(' ', '').str.contains('Tier1')==True, 'Instrument'] = 'Thermopile'

esmap['Comment'] = ''
esmap.loc[esmap['Tier']!=1, 'Comment'] = 'Instrument and components has not been manually checked'

esmap['Time period'] = (
    esmap['commission_date__m_d_y_'].str[:4] 
    + '-'
    + esmap['End of Measurement Campaign'].str[-4:].astype(str).str.replace('None', '')
)

# check if stations exists already
stations = pd.read_csv('../solarstations.csv')
duplicate_rows = []
for index, row in esmap.iterrows():
    if stations['Station full name'].str.contains(row['Station full name']).any():
        duplicate_rows.append(index)

esmap = esmap.drop(duplicate_rows)

header = 'Station full name,Abbreviation,State,Country,Latitude,Longitude,Elevation,Time period,Network,Owner,Comment,URL,Data availability,Tier,Instrument,Components'

columns = header.split(',')

esmap[columns].to_csv('../esmap_stations.csv', sep=',', index=False)
