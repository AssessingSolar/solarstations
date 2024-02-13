import pandas as pd

filename = 'geba_stations.xlsx'

dhi = pd.read_excel(filename, sheet_name='DHI', index_col='SGKEY')

dni = pd.read_excel(filename, sheet_name='DNI', index_col='SGKEY')


both_dhi_dni = list(set(dhi.index).intersection(set(dni.index)))



tier_1 = dni.loc[both_dhi_dni, :]
tier_1 = tier_1[~tier_1['Station name'].str.contains('BSRN')]
tier_1 = tier_1[~tier_1['Station name'].str.contains('SURFRAD')]
tier_1 = tier_1[~tier_1['ICC'].str.contains('AUS')]


# 2866            Glenlitta Ave  AUS  144.95 -37.70  ...   1997   2004    71   STANDARD