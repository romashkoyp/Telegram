# Code gets vocabulary of words
# counts how many times each word of phrase is in JSON file's text
# return result in CSV file

import json
import csv
import re
from collections import Counter

json_input = r'C:\Users\romas\Documents\Code\Telegram\Data\big_json.json'
csv_input = r'C:\Users\romas\Documents\Code\Telegram\Data\words_vocabulary.csv'
csv_output = r'C:\Users\romas\Documents\Code\Telegram\Data\word_quantity.csv'

# Load JSON file
with open(json_input, 'r', encoding='utf-8') as json_file:
    json_data = json.load(json_file)

# Read words from CSV file
words = []
with open(csv_input, 'r', encoding='utf-8') as csv_file:
    word_reader = csv.reader(csv_file)
    next(word_reader)  # Skip the header row
    for row in word_reader:
        words.append((row[0], row[1]))  # Assuming the word_id is in the first column

# Extract 'post_text' field from each object in the list
texts = [item.get('post_text', '') for item in json_data]

# Concatenate all 'post_text' into one string
text_data = ' '.join(texts)
if not text_data:
    print('no text data')
else:
    # Use Counter to count word occurrences
    word_count = Counter(re.findall(r'\b\w+\b', text_data.lower(), flags=re.IGNORECASE))

    # Prepare results as a list of lists
    results = []
    for word_id, word_form in words:
        # Count variations of the word
        count_post = sum(word_count[variant] for variant in re.findall(r'\b\w+\b', word_form.lower(), flags=re.IGNORECASE))
        results.append([word_id, word_form, count_post])

    # Save results to CSV
    with open(csv_output, 'w', encoding='utf-8', newline='') as result_file:
        csv_writer = csv.writer(result_file)
        # Write header
        csv_writer.writerow(['word_id', 'word_form', 'count_post'])
        # Write data
        csv_writer.writerows(results)

    print(f'Results saved to {csv_output}')
