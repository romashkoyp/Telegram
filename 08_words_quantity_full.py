# Code counts how many times each word is in JSON file's text
# return result in CSV file

import json
import csv
import re
from collections import Counter

json_input = r'C:\Users\romas\Documents\Code\Telegram\Data\big_json.json'
csv_output = r'C:\Users\romas\Documents\Code\Telegram\Data\word_quantity_full.csv'

# Load JSON file
with open(json_input, 'r', encoding='utf-8') as json_file:
    json_data = json.load(json_file)

# Extract 'post_text' field from each object in the list
texts = [item.get('post_text', '') for item in json_data]

# Concatenate all 'post_text' into one string
text_data = ' '.join(texts)
if not text_data:
    print('no text data')
else:
    # Use regex to remove non-alphanumeric characters and split the text into words
    words = re.findall(r'\b[А-Яа-я]+\b', text_data.lower())

    # Use Counter to count word occurrences
    word_count = Counter(words)

    # Prepare results as a list of dictionaries
    results = [{'word': word, 'count_post': count} for word, count in word_count.items()]

    # Sort results by 'count_post' in descending order
    sorted_results = sorted(results, key=lambda x: x['word'], reverse=False)

    # Save sorted results to CSV using DictWriter
    with open(csv_output, 'w', encoding='utf-8', newline='') as result_file:
        fieldnames = ['word', 'count_post']
        csv_writer = csv.DictWriter(result_file, fieldnames=fieldnames)
        
        # Write header
        csv_writer.writeheader()
        
        # Write data
        csv_writer.writerows(sorted_results)

    print(f'Sorted results saved to {csv_output}')
