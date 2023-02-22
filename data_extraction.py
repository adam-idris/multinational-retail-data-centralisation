import pandas as pd
import database_utils as du

db_connector = du.DatabaseConnector()

class DataExtractor:
    
    def read_rds_table(self, table_name):
        self.table = table_name
        return pd.read_sql_table(self.table, db_connector.init_db_engine())

extract_table = DataExtractor()
user_df = extract_table.read_rds_table('legacy_users')