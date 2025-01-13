# Code searches matching of words/phrases from CSV file
# in JSON file and count each matching for each word/phrase
# result is saved to TXT file to export it directly in Excel

import json
import csv
import re

json_input = r'C:\Users\romas\Documents\Code\Telegram\Data\4_channels\four_channels.json'
csv_input = r'C:\Users\romas\Documents\Code\Telegram\Data\russian_regions_vocabulary.csv'
txt_output = r'C:\Users\romas\Documents\Code\Telegram\Analyze_12.01.2025\region_quantity.txt'

# Read the CSV file
with open(csv_input, 'r', encoding='utf-8') as csv_file:
    csv_reader = csv.DictReader(csv_file)
    data = list(csv_reader)

# Read the JSON file
with open(json_input, 'r', encoding='utf-8') as json_file:
    word_count_data = json.load(json_file)

texts = [item.get('post_text', '') for item in word_count_data]

text_data = ' '.join(texts).lower()

# Create a new list with counts using regular expressions
result_data = []
order = 0
length = len(data)
for row in data:
    region_id = row['region_id']
    region_name_x = row['region_name_x']
    region_name_y = row['region_name_y']

    # Use regular expression to find whole words
    pattern = rf'\b{re.escape(region_name_y.lower())}\b'
    count = len(re.findall(pattern, text_data))

    result_data.append({
        'region_id': region_id,
        'region_name': region_name_x,
        'region_form': region_name_y,
        'count': count
    })

    share = (order / length) * 100
    print(f'{share:.2f}% complete ({order + 1} of {length}): {result_data[order]}')
    order += 1

# Write result in TXT file to extract it to Excel
with open(txt_output, 'w', encoding='utf-8') as output_file:
    output_file.write("region_id*region_name*region_form*count\n")
    for result in result_data:
        output_line = f"{result['region_id']}*{result['region_name']}*{result['region_form']}*{result['count']}\n"
        output_file.write(output_line)

print("Results have been saved to", txt_output)
