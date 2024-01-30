# Code detects JSON files in folder and subfolders
# extracts data from these JSON files and
# cleans text data from emojies, whitespaces and unusual characters
# create only one JSON file with all data

import json
import os
import re

# Specify the root directory containing JSON files
root_directory = r'C:\Users\romas\Documents\Code\Telegram\Analysis'

# Ensure the output directory exists
output_directory = os.path.join(root_directory, 'Data')
os.makedirs(output_directory, exist_ok=True)

file_name = 'big_json'

# Function to reset word count and create a new output file
def create_new_file(directory, extension):
    return os.path.join(directory, f'{file_name}.{extension}')

# Extracted data list for all JSON files
all_extracted_data = []

# Counter for global post ID
global_post_id_counter = 1

# Iterate through each subdirectory in the root directory
for subdir, _, files in os.walk(root_directory):
    for file in files:
        # Check if the file is a JSON file
        if file.endswith('.json'):
            json_input = os.path.join(subdir, file)

            # Load JSON data from file
            with open(json_input, 'r', encoding='utf-8') as file:
                data = json.load(file)

                # Extracted data list for each JSON file
                extracted_data = []

                for message in data.get('messages', []):
                    # Extract information from the message
                    channel = message.get('from', '')
                    post_id = message.get('id', '')
                    post_date = message.get('date', '')
                    post_text = message.get('text', '')

                    if post_text:
                        full_text = ''.join(item.get('text', '') if isinstance(item, dict) else item for item in post_text)
                        lines = [line for line in full_text.splitlines() if line.strip()]
                        cleaned_text = ' '.join(lines)

                        # Define a list of allowed symbols
                        allowed_symbols = ['«', '»', '.', ',', '!', '?', ':', ';', '(', ')', '[', ']', '{', '}', '&', '@', '#', '$', '%', '^', '*', '+', '-', '=', '_', '<', '>', '|', '/', '\\']

                        # Remove emojis and unwanted symbols using regex
                        cleaned_text = re.sub(r'[^\w\s{}]+'.format(''.join(re.escape(symbol) for symbol in allowed_symbols)), '', cleaned_text)
                        cleaned_text = re.sub(r'\s+', ' ', cleaned_text)
                        
                        # Add extracted data to the list
                        extracted_data.append({
                            "channel": channel,
                            "post_id": post_id,
                            "global_post_id": global_post_id_counter,
                            "post_date": post_date,
                            "post_text": cleaned_text
                        })

                        # Increment the global post ID counter
                        global_post_id_counter += 1

                # Append the extracted data for the current file to the overall list
                all_extracted_data.extend(extracted_data)

# Save all extracted information to a single JSON file in the output directory
output_json_path = create_new_file(output_directory, 'json')

with open(output_json_path, 'w', encoding='utf-8') as output_json_file:
    json.dump(all_extracted_data, output_json_file, ensure_ascii=False, indent=2)

print(f"All data has been extracted and saved to {output_json_path}.")
