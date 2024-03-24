import pandas as pd
import requests
url = 'https://energydata.info/api/3/action/datastore_search?resource_id=da73e4b1-7cb1-4c9c-8e54-594fad190a60&limit=500'  
response = requests.get(url)

df = pd.DataFrame(response.json()['result']['records'])

columns_dict = {
    'Nearest Settlement': 'Station full name',
    'Site Name': 'Abbreviation',
    'Project Founder': 'Network',
    # Could also use 'documents___reports_url'
    'Measurement Data URL': 'URL',
    'Equipment Owner': 'Owner',
}

df = df.rename(columns=columns_dict)

df['Tier'] = ''
df.loc[df['Equipment Type'].str.replace(' ', '').str.contains('Tier1')==True, 'Tier'] = 1
df.loc[df['Equipment Type'].str.replace(' ', '').str.contains('Tier2')==True, 'Tier'] = 2

df['State'] = ''
df['Data availability'] = 'Freely'

df['Components'] = ''
df.loc[df['Tier']==1, 'Components'] = 'G;B;D'

df['Instrument'] = 'Thermopile'

df['Comment'] = ''
df.loc[df['Tier']!=1, 'Comment'] = 'Instrument and components has not been manually checked'

df['Time period'] = (
    df['commission_date__m_d_y_'].str[:4] 
    + '-'
    + df['End of Measurement Campaign'].str[-4:].astype(str).str.replace('None', '')
)

header = 'Station full name,Abbreviation,State,Country,Latitude,Longitude,Elevation,Time period,Network,Owner,Comment,URL,Data availability,Tier,Instrument,Components'

columns = header.split(',')

df[columns].to_csv('../esmap_stations.csv', sep=',', index=False)
