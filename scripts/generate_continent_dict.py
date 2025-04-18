"""Generate dictionary mapping country name to continent."""
import pandas as pd
import json

# Read list of countries by continent from Wikipedia
cc = pd.read_html('https://simple.wikipedia.org/wiki/List_of_countries_by_continents', header=[0])
cc = cc[:1] + cc[2:]  # skip the territories section

continents = ['Africa', 'Asia', 'Europe', 'North America', 'South America', 'Oceania']


country_continent_dict = {}
for continent, d in zip(continents, cc):

    country_column = \
        [c for c in d.columns if (('english name' in c.lower()) | ('country' in c.lower()))][0]
    for index, row in d.iterrows():
        country = row[country_column].split('[')[0].replace('*', '')
        country_continent_dict[country] = continent


# Variant spellings
country_continent_dict['Czech Republic'] = country_continent_dict['Czechia']
country_continent_dict['USA'] = country_continent_dict['United States']
# Areas that aren't actual countries
country_continent_dict['Antarctica'] = 'Antarctica'
country_continent_dict['Reunion'] = 'Africa'  # Territory of France
country_continent_dict['Mayotte'] = 'Africa'  # Territory of France
country_continent_dict['American Samoa'] = 'Oceania'
country_continent_dict['Canary Islands'] = 'Africa'
country_continent_dict['Greenland'] = 'North America'

with open("../data/country_by_continent.json", "w") as file:
    json.dump(country_continent_dict, file, indent="")
