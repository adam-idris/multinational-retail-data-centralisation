import database_utils
import pandas as pd

db_connector = database_utils.DatabaseConnector()

class DataExtractor:
    
    def read_rds_table(self, table_name):
        self.table = table_name
        return pd.read_sql_table(self.table, db_connector.init_db_engine())

extract_table = DataExtractor()
user_df = extract_table.read_rds_table('legacy_users')

print(user_df['country'].value_counts())

