import data_extraction
import pandas as pd
import numpy as np

user_df = data_extraction.user_df
card_df = data_extraction.card_df
store_df = data_extraction.store_df
products_df = data_extraction.products_df
orders_df = data_extraction.orders_df
dates_df = data_extraction.dates_df


class DataClean:
    
    def clean_user_data(self, dataf):
        
        # Clean country data
        countries = pd.DataFrame({'country': ['United States', 'United Kingdom', 'Germany']})
        
        unique_countries = set(dataf['country'].unique())
        invalid_countries = unique_countries.difference(countries['country'])
        
        invalid = dataf['country'].isin(invalid_countries)
        valid_rows = dataf[~invalid]
    
        # Correct GGB in country code
        dataf = dataf.copy()
        valid_rows = valid_rows.replace(to_replace='GGB', value='GB')
        
        # Add call code to separate column
        
        conditions = [(valid_rows['country'] == 'United States'), 
                      (valid_rows['country'] == 'United Kingdom'), 
                      (valid_rows['country'] == 'Germany')]
        
        values = ['+1', '+44', '+49']
        
        valid_rows['calling_code'] = np.select(conditions, values)
        
        # Clean phone numbers
        
        valid_rows['phone_number'] = valid_rows['phone_number'].replace('\D', '', regex=True)
        valid_rows = valid_rows[['first_name', 'last_name', 'date_of_birth', 'company', 'email_address', 'address', 'country', 'country_code', 'calling_code', 'phone_number', 'join_date', 'user_uuid']]
        
        valid_rows.loc[valid_rows['phone_number'].str.startswith('44'), 'phone_number'] = '0' + valid_rows['phone_number'].str[2:]
        valid_rows.loc[valid_rows['phone_number'].str.startswith('49'), 'phone_number'] = '0' + valid_rows['phone_number'].str[2:]
        valid_rows.loc[valid_rows['phone_number'].str.startswith('00'), 'phone_number'] = '0' + valid_rows['phone_number'].str[2:]
        
        return valid_rows 
    
    def clean_card_data(self, dataf):
        
        no_null = dataf[~dataf['card_number'].isin(['NULL'])]
        return no_null
    
    def clean_store_data(self, dataf):
        
        codes = pd.DataFrame({'country_code': ['US', 'GB', 'DE']})
        
        unique_codes = set(dataf['country_code'].unique())
        invalid_countries = unique_codes.difference(codes['country_code'])
        
        invalid = dataf['country_code'].isin(invalid_countries)
        valid_rows = dataf[~invalid]
        
        valid_rows = valid_rows.replace(to_replace=['eeEurope', 'eeAmerica'], value=['Europe', 'America'])
        
        return valid_rows
    
    def cleaned_product_data(self, dataf):
        
        dataf = dataf.dropna()

        categories = pd.DataFrame({'category': ['homeware', 'toys-and-games', 'food-and-drink', 'pets', 'sports-and-leisure', 'health-and-beauty', 'diy']})
                
        unique_cats = set(dataf['category'].unique())
        invalid_cats = unique_cats.difference(categories['category'])
                
        invalid = dataf['category'].isin(invalid_cats)
        dataf = dataf[~invalid]

        dataf = dataf.reset_index(drop=True)

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
        dataf = dataf.drop(['Unnamed: 0'], axis=1)


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
        
        # Convert dates to same format
        
        dataf['date_added'] = pd.to_datetime(dataf.date_added)
        
        return dataf
        
    def clean_orders_data(self, dataf):
        
        dataf = dataf[['index', 'date_uuid', 'user_uuid', 'card_number', 'store_code', 'product_code', 'product_quantity']]
        return dataf

    def clean_dates_data(self, dataf):
        
        dataf = dataf[dataf['year'].str.isnumeric()]

        return dataf
        
        
clean_data = DataClean()
cleaned_user_data = clean_data.clean_user_data(user_df)
cleaned_card_data = clean_data.clean_card_data(card_df)
cleaned_store_data = clean_data.clean_store_data(store_df)
cleaned_product_data = clean_data.cleaned_product_data(products_df)
cleaned_orders_data = clean_data.clean_orders_data(orders_df)
cleaned_dates_data = clean_data.clean_dates_data(dates_df)