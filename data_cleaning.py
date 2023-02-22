import data_extraction
import pandas as pd
import numpy as np
import data_extraction as de
import database_utils as du

user_df = data_extraction.user_df


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
        
        valid_rows['phone_number'] = valid_rows['phone_number'].str.replace('\W', '', regex=True)
        valid_rows = valid_rows[['first_name', 'last_name', 'date_of_birth', 'company', 'email_address', 'address', 'country', 'country_code', 'calling_code', 'phone_number', 'join_date', 'user_uuid']]
        
        return valid_rows 

clean_data = DataClean()
final = clean_data.clean_user_data(user_df)
