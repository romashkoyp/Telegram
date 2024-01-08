# Code merges two CSV files by ID to make single CSV

import pandas as pd

# Assuming your first CSV is 'first.csv' and the second one is 'second.csv'
first_csv_path = r'C:\Users\romas\Documents\Code\Telegram\russian_regions.csv'
second_csv_path = r'C:\Users\romas\Documents\Code\Telegram\russian_regions_vocabulary.csv'

# Load CSV files into pandas DataFrames
df_first = pd.read_csv(first_csv_path)
df_second = pd.read_csv(second_csv_path)

# Merge the two DataFrames based on 'region_id'
merged_df = pd.merge(df_first[['region_id', 'region_name']], df_second, on='region_id', how='left')

# Print the resulting DataFrame (for educational purposes)
print(merged_df)

# Now you can save the merged DataFrame back to a CSV file if needed
merged_df.to_csv(r'C:\Users\romas\Documents\Code\Telegram\russian_regions_2.csv', index=False)
