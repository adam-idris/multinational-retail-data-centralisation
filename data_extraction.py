import pandas as pd
import tabula
import database_utils as du
import requests
import json

db_connector = du.DatabaseConnector()
header_details = {'x-api-key':'yFBQbwXe9J3sd6zWVAMrK6lcxxr0q1lr2PT6DDMX'}
number_of_stores = 'https://aqj7u5id95.execute-api.eu-west-1.amazonaws.com/prod/number_stores'
retrieve_stores = 'https://aqj7u5id95.execute-api.eu-west-1.amazonaws.com/prod/store_details/{store_number}'

class DataExtractor:
    
    def read_rds_table(self, table_name):
        self.table = table_name
        return pd.read_sql_table(self.table, db_connector.init_db_engine())
    
    def retrieve_pdf_data(self):
        pdf_to_df = tabula.read_pdf('https://data-handling-public.s3.eu-west-1.amazonaws.com/card_details.pdf', pages='all')
        dataf = pd.concat(pdf_to_df, ignore_index=True)
        return dataf

    def list_number_of_stores(self, stores, header):
        r = requests.get(stores, headers=header)
        return r.text

    def retrieve_stores_data(self, stores, header):
        all_stores = []
        for i in range(1,451):
            new_stores = stores.replace('{store_number}', str(i))
            r = requests.get(new_stores, headers=header)
            dictionary = json.loads(r.text)
            all_stores.append(dictionary)
            df = pd.DataFrame(all_stores)
        return df

extract_table = DataExtractor()
# user_df = extract_table.read_rds_table('legacy_users')
# card_df = extract_table.retrieve_pdf_data()

print(extract_table.retrieve_stores_data(retrieve_stores, header_details))

