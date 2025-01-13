# This script reads a JSON file, groups its contents by the 'channel' key,
# sanitizes the channel names to ensure they are valid file names,
# and writes each group's data to a separate JSON file in the specified output directory

import json
import os
import re

def sanitize_filename(filename):
    # Replace invalid characters with underscores
    return re.sub(r'[\\/*?:"<>|]', '_', filename)

def split_json_file_by_channel(input_file, output_directory):
    with open(input_file, 'r', encoding='utf-8') as file:
        data = json.load(file)

    # Create the output directory if it doesn't exist
    os.makedirs(output_directory, exist_ok=True)

    # Dictionary to hold data for each channel
    channel_data = {}

    # Iterate through the data and group by channel
    for item in data:
        channel = item['channel']
        if channel not in channel_data:
            channel_data[channel] = []
        channel_data[channel].append(item)

    # Write each channel's data to a separate file
    for channel, items in channel_data.items():
        sanitized_channel = sanitize_filename(channel)
        output_file = os.path.join(output_directory, f'{sanitized_channel}.json')
        with open(output_file, 'w', encoding='utf-8') as out_file:
            json.dump(items, out_file, ensure_ascii=False, indent=2)

# Example usage:
input_file_path = r'C:\Users\romas\Documents\Code\Telegram\Data\big_json.json'
output_directory_path = r'C:\Users\romas\Documents\Code\Telegram\Data\Channels'

split_json_file_by_channel(input_file_path, output_directory_path)
