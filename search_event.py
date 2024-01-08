# This Python script extracts event-related information from a JSON file, 
# specifically the text enclosed in «» symbols. It checks for specific criteria, 
# including word count and formatting, and cross-references the extracted information with a CSV file. 
# The results, containing the event code, word before the event, and event name, are saved in a JSON file. 
# Users can configure input file paths and customize the script for different datasets.

import json
import re
import csv

json_input = r'C:\Users\romas\Documents\Code\Telegram\Data\big_json.json'
csv_input = r'C:\Users\romas\Documents\Code\Telegram\Data\event_vocabulary.csv'

# Load JSON file
with open(json_input, 'r', encoding='utf-8') as json_file:
    json_data = json.load(json_file)

# Extract 'post_text' field from each object in the list
texts = [item.get('post_text', '') for item in json_data]

# Define a regular expression pattern to find text between «» symbols with optional spaces
event_pattern = re.compile(r'\s*«([^»]*)»\s*')  # Updated pattern to include optional spaces

# Create a set to store unique results (case insensitive)
unique_results_lowercase = set()

# Read words from the CSV file into a set (case insensitive)
with open(csv_input, 'r', encoding='utf-8') as csv_file:
    csv_reader = csv.reader(csv_file)
    next(csv_reader)
    # Get word from the second column and the second row, all words are only from the second column
    words_from_csv = set(row[1].lower() for row in csv_reader)

for text in texts:
    # Extract text between «» symbols
    matches = re.findall(event_pattern, text)

    for match in matches:
        # Check if the match is not empty
        if match:
            # Check if inside «» there are more than 6 words
            if len(match.split()) <= 17:
                # Find word before '«match»'
                # Use re.search to find the word before the match
                match_position = text.find(match)

                # Split the text and check if it's not empty before accessing elements
                words_before = text[:match_position].split()
                
                if len(words_before) >= 2:
                    word_before = words_before[-2]

                    # Check if word before exists
                    if word_before:
                        # Check if word before contains only Cyrillic characters
                        if all(char.isalpha() and char.isalpha() for char in word_before):
                            # Check if word before length is more than 3 characters
                            if len(word_before) > 3:
                                # Check if not all characters in word before are in upper case
                                if not all(char.isupper() for char in word_before):
                                    # Convert result to lowercase for case-insensitive comparison
                                    result_lowercase = (word_before.lower(), match.lower())

                                    # Check if the lowercase result is not already in the set
                                    if result_lowercase not in unique_results_lowercase:
                                        # Check if word_before is in the set of words from CSV (case insensitive)
                                        if word_before.lower() in words_from_csv:
                                            # Print and add to the set
                                            # print(f'{word_before} «{match}»')
                                            unique_results_lowercase.add(result_lowercase)

# Create a list of dictionaries from the unique results set
unique_results_json = []

for result in unique_results_lowercase:
    word_before = result[0]
    event_name = result[1]

    # Search for the event_code in the CSV file
    event_code = None
    with open(csv_input, 'r', encoding='utf-8') as csv_file:
        csv_reader = csv.reader(csv_file)
        next(csv_reader)  # Skip header
        for row in csv_reader:
            if row[1].lower() == word_before.lower():
                event_code = row[0]
                break

    # Create dictionary with additional event_code
    result_dict = {
        'event_code': event_code,
        'word_before': word_before,
        'event_name': f'«{event_name}»'
    }

    # Add the dictionary to the list
    unique_results_json.append(result_dict)

# Save unique results to a JSON file
json_output_file = 'unique_events.json'
with open(json_output_file, 'w', encoding='utf-8') as output_file:
    json.dump(unique_results_json, output_file, ensure_ascii=False, indent=2)

print(f'Results saved to {json_output_file}')
