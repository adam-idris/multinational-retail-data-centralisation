import data_extraction as de
import data_cleaning as dc
import database_utils as du

connect_db = du.DatabaseConnector()
cleaned_user_data = dc.cleaned_user_data
cleaned_card_data = dc.cleaned_card_data
cleaned_store_data = dc.cleaned_store_data
cleaned_products_data = dc.cleaned_product_data
cleaned_orders_data = dc.cleaned_orders_data
cleaned_dates_data = dc.cleaned_dates_data

connect_db.upload_to_db(cleaned_user_data, 'dim_users')
connect_db.upload_to_db(cleaned_card_data, 'dim_card_details')
connect_db.upload_to_db(cleaned_store_data, 'dim_store_details')
connect_db.upload_to_db(cleaned_products_data, 'dim_products_details')
connect_db.upload_to_db(cleaned_orders_data, 'dim_orders_details')
connect_db.upload_to_db(cleaned_dates_data, 'dim_date_times')

