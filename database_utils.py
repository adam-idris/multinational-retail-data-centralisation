import yaml
from sqlalchemy import create_engine
from sqlalchemy import inspect

class DatabaseConnector:
    
    def read_db_creds(self):
        with open('db_creds.yaml') as f:
            self.db_creds = yaml.safe_load(f)
            return self.db_creds
    
    def init_db_engine(self):
        
        creds = self.read_db_creds()
        host = creds['RDS_HOST']
        user = creds['RDS_USER']
        passwd = creds['RDS_PASSWORD']
        database = creds['RDS_DB_TYPE']
        port = creds['RDS_PORT']
        db_name = creds['RDS_DATABASE']

        engine = create_engine(f"{database}://{user}:{passwd}@{host}:{port}/{db_name}")
        return engine.connect()

    def list_db_tables(self):
        inspector = inspect(self.init_db_engine())
        return inspector.get_table_names()


readyaml = DatabaseConnector()
print(readyaml.list_db_tables())