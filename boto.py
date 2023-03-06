
import pandas as pd
import numpy as np

dataf = pd.read_csv('products.csv')
dataf = dataf.dropna()

categories = pd.DataFrame({'category': ['homeware', 'toys-and-games', 'food-and-drink', 'pets', 'sports-and-leisure', 'health-and-beauty', 'diy']})
        
unique_cats = set(dataf['category'].unique())
invalid_cats = unique_cats.difference(categories['category'])
        
invalid = dataf['category'].isin(invalid_cats)
dataf = dataf[~invalid]

dataf = dataf.reset_index()

conditions = [(dataf['weight'].str.endswith('kg') == True), 
              (dataf['weight'].str.endswith('ml') == True), 
              (dataf['weight'].str.endswith('oz') == True)]
        
values = ['kg', 'ml', 'oz']
        
dataf['units'] = np.select(conditions, values)
dataf['units'] = dataf['units'].str.replace('0', 'g')

dataf.loc[dataf['weight'].str.endswith(('kg', 'ml', 'oz', 'g .')), 'weight'] = dataf['weight'].str[:-2]
dataf.loc[dataf['weight'].str.endswith('ml'), 'weight'] = dataf['weight'].str[:-2]
dataf.loc[dataf['weight'].str.endswith('g'), 'weight'] = dataf['weight'].str[:-1]


dataf = dataf.reset_index()
dataf = dataf.drop(['Unnamed: 0', 'index', 'level_0'], axis=1)


dataf['mult'] = dataf['weight'].str.contains('x')
subsets = dataf[dataf['mult']]
dataf['quantity'] = subsets['weight'].str[:2]
dataf['quantity'] = dataf['quantity'].fillna(1)

dataf['weight'] = dataf['weight'].str.split('x')

dataf['new_weight'] = ''

for i in range(len(dataf)):
    if (len(dataf['weight'].iloc[i])) == 2:
        dataf['new_weight'][i] = dataf['weight'][i][1]
    else:
        dataf['new_weight'][i] = dataf['weight'][i][0]
        
dataf['new_weight'] = dataf['new_weight'].astype(float)
dataf['quantity'] = dataf['quantity'].astype(float)
dataf['new_weight'] = dataf['new_weight'] * dataf['quantity']

conditions = [(dataf['units'].isin(['ml', 'g']) == True), 
              (dataf['units'].isin(['kg']) == True), 
              (dataf['units'].isin(['oz']) == True)]
        
values = [1000, 1, 0.035274]

dataf['conversion'] = np.select(conditions, values)
dataf['final_weight'] = dataf['new_weight'] / dataf['conversion']       

column_names = ['product_name', 'product_price', 'final_weight', 'category', 'EAN', 'date_added', 'uuid', 'removed', 'product_code']
dataf = dataf[column_names]

dataf['date_added'] = pd.to_datetime(dataf.date_added)

print(dataf.iloc[306])


