import pandas as pd

data_index = pd.read_csv('C:/Users/Tiger/Desktop/site_index.csv')
site_id = '1966A'
NDVI_lon_index =int(data_index.loc[data_index['site_id']==site_id, 'NDVI_lon_index'])
print(NDVI_lon_index)
print()
