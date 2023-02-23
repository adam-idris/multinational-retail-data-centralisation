import pandas as pd
import tabula
import database_utils as du
from functools import reduce

db_connector = du.DatabaseConnector()

class DataExtractor:
    
    def read_rds_table(self, table_name):
        self.table = table_name
        return pd.read_sql_table(self.table, db_connector.init_db_engine())
    
    def retrieve_pdf_data(self):
        pdf_to_df = tabula.read_pdf('https://data-handling-public.s3.eu-west-1.amazonaws.com/card_details.pdf', pages='all')
        dataf = pd.concat(pdf_to_df, ignore_index=True)
        return dataf

extract_table = DataExtractor()
user_df = extract_table.read_rds_table('legacy_users')
card_df = extract_table.retrieve_pdf_data()
print(card_df)