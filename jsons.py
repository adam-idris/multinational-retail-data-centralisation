import pandas as pd

date_df = pd.read_json('date_details.json')
date_df = date_df[date_df['year'].str.isnumeric()]

print(date_df['time_period'].unique())
