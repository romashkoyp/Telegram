# Code gets vocabulary with words from CSV file
# to find in texts of JSON file
# sentences which contain desired phrase: word + event name in between «»
# saves result in JSON

import json
import re
import csv

json_input = r'C:\Users\romas\Documents\Code\Telegram\Data\4_channels\four_channels.json'
csv_input = r'C:\Users\romas\Documents\Code\Telegram\Data\event_vocabulary.csv'

# Load JSON file
with open(json_input, 'r', encoding='utf-8') as json_file:
    json_data = json.load(json_file)

# Extract 'post_text' field from each object in the list
texts = [item.get('post_text', '') for item in json_data]

# Join the list of strings into a single string
all_texts = ' '.join(texts)

# Split the combined string into sentences
sentences = re.split(r'(?<!\w\.\w.)(?<![A-Z][a-z]\.)(?<=\.|\?)\s', all_texts)

# Define a regular expression pattern to find text between «» symbols with optional spaces
event_pattern = re.compile(r'\s*«([^»]*)»\s*')  # Updated pattern to include optional spaces

# Read words from the CSV file into a set (case insensitive)
with open(csv_input, 'r', encoding='utf-8') as csv_file:
    csv_reader = csv.reader(csv_file)
    next(csv_reader)
    # Get word from the second column and the second row, all words are only from the second column
    words_from_csv = set(row[1].lower() for row in csv_reader)

# Create a list to store all results
all_results_json = []

for sentence in sentences:
    # Extract text between «» symbols
    matches = re.findall(event_pattern, sentence)

    for match in matches:
        # Check if the match is not empty
        if match:
            # Check if inside «» there are more than 6 words
            if len(match.split()) <= 17:
                # Find word before '«match»'
                # Use re.search to find the word before the match
                match_position = sentence.find(match)

                # Split the text and check if it's not empty before accessing elements
                words_before = sentence[:match_position].split()
                
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
                                    # Check if word_before is in the set of words from CSV (case insensitive)
                                    if word_before.lower() in words_from_csv:
                                        # Search for the event_code in the CSV file
                                        event_code = None
                                        with open(csv_input, 'r', encoding='utf-8') as csv_file:
                                            csv_reader = csv.reader(csv_file)
                                            next(csv_reader)  # Skip header
                                            for row in csv_reader:
                                                if row[1].lower() == word_before.lower():
                                                    event_code = row[0]
                                                    break

                                        # Create dictionary with additional event_code and original sentence
                                        result_dict = {
                                            'sentence': sentence,  # Include the original sentence
                                            'event_code': event_code,
                                            'word_before': word_before,
                                            'event_name': f'«{match}»',
                                            'word_before_event_name': f'{word_before} «{match}»'                                            
                                        }

                                        # Add the dictionary to the list
                                        all_results_json.append(result_dict)

# Save all results to a JSON file
json_output_file = 'all_events_sentences.json'
with open(json_output_file, 'w', encoding='utf-8') as output_file:
    json.dump(all_results_json, output_file, ensure_ascii=False, indent=2)

print(f'Results saved to {json_output_file}')
