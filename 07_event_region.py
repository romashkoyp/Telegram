# Code gets vocabulary of regions from CSV
# searchs words from vocabulary in sentences of JSON file
# saves result in TXT file for exporting it in EXCEL

import json
import csv
import re

csv_input = r'C:\Users\romas\Documents\Code\Telegram\Data\russian_regions_vocabulary.csv'
json_events = r'C:\Users\romas\Documents\Code\Telegram\Data\all_events_sentences.json'
output_file_path = r'C:\Users\romas\Documents\Code\Telegram\Data\event_region.txt'

# Load CSV file with regions
regions_data = []

with open(csv_input, 'r', encoding='utf-8') as csv_file:
    csv_reader = csv.reader(csv_file)
    next(csv_reader)  # Skip header row
    for row in csv_reader:
        regions_data.append({
            'region_id': row[0],
            'region_name_x': row[1],
            'region_name_y': row[2]
        })

# print(f'{regions_data[:10]}\n')

# Load JSON file with events
with open(json_events, 'r', encoding='utf-8') as json_file:
    json_data_events = json.load(json_file)

# Create list of events
events = []

for entry in json_data_events:
    # Extract information from the entry
    sentence = entry.get('sentence', '')
    event_code = entry.get('event_code', '')
    word_before = entry.get('word_before', '')
    event_name = entry.get('event_name', '')
    word_before_event_name = entry.get('word_before_event_name', '')
    
    # Add extracted data to the events list
    events.append({
    "sentence": sentence,
    "event_code": event_code,
    "word_before": word_before,
    "event_name": event_name,
    "word_before_event_name": word_before_event_name
    })

# print(f'{events[:10]}\n')

# Iterate through sentences and find matches
with open(output_file_path, 'w', encoding='utf-8') as output_file:
    output_file.write("Region_ID*Region_base_name*Region_form_name*Event_base_name*Event_Name*Word_Before_and_Event_Name\n")
    order = 0
    length = len(json_data_events)
    # Iterate through sentences and find matches
    for event in events:
        event_code = event['event_code']
        word_before = event['word_before']
        event_name = event['event_name']
        word_before_event_name = event['word_before_event_name']
        event_sentence = event['sentence'].lower()

        for region_data in regions_data:
            reg = region_data['region_name_y']
            region_id = region_data['region_id']
            region_name_x = region_data['region_name_x']
            pattern = rf'\b{re.escape(reg.lower())}\b'
            if re.search(pattern, event_sentence):
                output_line = f"{region_id}*{region_name_x}*{reg}*{event_code}*{event_name}*{word_before_event_name}\n"
                output_file.write(output_line)
        
        share = (order / length) * 100
        print(f'{share:.2f}% complete ({order + 1} of {length})')
        order += 1

print("Results have been saved to", output_file_path)
