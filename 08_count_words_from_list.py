'''
Given: json file with text data, extract all 'post_text' fields from each object in the list
Concatenate all 'post_text' into one string, where desired word 'СВО' is present
Use regex to remove non-alphanumeric characters and split the text into words
Use Counter to count word occurrences
Return: result in txt file with word and how many times it is present in the text by descending order
'''

import json
import csv
import re

json_input = r'C:\Users\romas\Documents\Code\Telegram\Analyze_12.01.2025\four_channels.json'

# CSV file with words to count, where: word_id (first column) is unique identifier, and word_form is form of word_id to count
csv_input = r'C:\Users\romas\Documents\Code\Telegram\Analyze_12.01.2025\words_vocabulary_negative.csv'
txt_output = r'C:\Users\romas\Documents\Code\Telegram\Analyze_12.01.2025\word_quantity_negative_all.txt'

# Load JSON file
with open(json_input, 'r', encoding='utf-8') as json_file:
    json_data = json.load(json_file)

# Concatenate all 'post_text' into one string, where desired word 'СВО' is present
# texts = [item.get('post_text', '') for item in json_data if 'СВО' in item.get('post_text', '')]

# Concatenate all 'post_text' into one string
texts = [item.get('post_text', '') for item in json_data]
text_data = ' '.join(texts)

# Use regex to remove non-alphanumeric characters and split the text into words
# words = re.findall(r'\b[А-Яа-я]+\b', text_data.lower())

# Remove non-alphanumeric characters
cleaned_text = re.sub(r'[^А-Яа-яA-za-z\s]', '', text_data.lower())

# print(cleaned_text[:1000])

# Load CSV file with words to count word_form form (second column of CSV file)
with open(csv_input, 'r', encoding='utf-8') as csv_file:
    csv_reader = csv.DictReader(csv_file)
    data = list(csv_reader)

# Create a new list with counts using regular expressions
result_data = []

for row in data:
    word_id = row['word_id']
    word_form = row['word_form']

    # Use regular expression to find whole words
    # pattern = rf'\b{re.escape(word_form.lower())}\b'
    count = len(re.findall(word_form, cleaned_text))

    result_data.append({
        'word_id': word_id,
        'word_form': word_form,
        'count': count
    })

# Write result in TXT file to extract it to Excel
with open(txt_output, 'a', encoding='utf-8') as output_file:
    output_file.write("word_id*word_form*count\n")
    for result in result_data:
        output_line = f"{result['word_id']}*{result['word_form']}*{result['count']}\n"
        output_file.write(output_line)

print("Results have been saved to", txt_output)