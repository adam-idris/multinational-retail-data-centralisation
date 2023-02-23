import pandas as pd
import data_extraction as de
import data_cleaning as dc
import database_utils as du

connect_db = du.DatabaseConnector()
cleaned_user_data = dc.cleaned_data
cleaned_card_data = dc.cleaned_card_data

connect_db.upload_to_db(cleaned_user_data, 'dim_users')
connect_db.upload_to_db(cleaned_card_data, 'dim_card_details')
