# script divide json file into desired quantity json files

import json
import os

def split_json_file(input_file, output_directory, num_files=10):
    with open(input_file, 'r', encoding='utf-8') as file:
        data = json.load(file)

    # Calculate the number of items per chunk
    items_per_chunk = len(data) // num_files
    remainder = len(data) % num_files

    # Create the output directory if it doesn't exist
    os.makedirs(output_directory, exist_ok=True)

    # Split the data into chunks and save each chunk to a separate file
    start_idx = 0
    for i in range(num_files):
        end_idx = start_idx + items_per_chunk + (1 if i < remainder else 0)
        chunk_data = data[start_idx:end_idx]

        output_file = os.path.join(output_directory, f'output_{i + 1}.json')
        with open(output_file, 'w', encoding='utf-8') as out_file:
            json.dump(chunk_data, out_file, ensure_ascii=False, indent=2)

        start_idx = end_idx

# Example usage:
input_file_path = r'Data\big_json.json'
output_directory_path = r'Data\Json'

split_json_file(input_file_path, output_directory_path, num_files=10)
