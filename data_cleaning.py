import data_extraction
import pandas as pd
import numpy as np

user_df = data_extraction.user_df
card_df = data_extraction.card_df


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

clean_data = DataClean()
cleaned_data = clean_data.clean_user_data(user_df)
cleaned_card_data = clean_data.clean_card_data(card_df)

print(len(cleaned_card_data))
