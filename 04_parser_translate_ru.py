# Code gets words from CSV file
# generates link for each word to create link for translate.ru
# extracts word's forms from translate.ru
# saves data in new CSV file

import csv
from urllib.parse import quote
import requests
from bs4 import BeautifulSoup

CSV_INPUT = r'C:\Users\romas\Documents\Code\Telegram\Data\russian_regions.csv'
CSV_OUTPUT = r'C:\Users\romas\Documents\Code\Telegram\russian_regions_translate.csv'

base_url = "https://www.translate.ru/%D1%81%D0%BF%D1%80%D1%8F%D0%B6%D0%B5%D0%BD%D0%B8%D0%B5%20%D0%B8%20%D1%81%D0%BA%D0%BB%D0%BE%D0%BD%D0%B5%D0%BD%D0%B8%D0%B5/%D1%80%D1%83%D1%81%D1%81%D0%BA%D0%B8%D0%B9/{word}"

def encode_cyrillic_to_hex(input_text):
    encoded_text = quote(input_text, encoding='utf-8')
    return encoded_text

# List to keep track of unique region names
unique_region_names = []

# Set a user agent to avoid blocking
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
}

# Open input csv
with open(CSV_INPUT, 'r', encoding='utf-8') as file:
    csv_reader = csv.reader(file)

    # Read the first row to get column names
    columns = next(csv_reader)

    # Open the output CSV file for unique region names
    with open(CSV_OUTPUT, 'w', newline='', encoding='utf-8') as csvfile:
        writer = csv.writer(csvfile)

        # Write the header row to the output CSV
        writer.writerow([columns[0], columns[1]])

        # Iterate through the rest of the rows
        for row in csv_reader:
            # Get the region_id from the first column
            region_id = row[0]

            # Iterate through columns starting from the second column
            for col_index in range(1, len(row)):
                # Get the Cyrillic word from the current column
                cyrillic_word = row[col_index]

                # Check if the column is not empty
                if cyrillic_word:
                    try:
                        # Translate Cyrillic words to hex
                        word = encode_cyrillic_to_hex(cyrillic_word)

                        # Put hex word into the URL
                        search_link = base_url.format(word=word)

                        # Go to the URL
                        response = requests.get(search_link)

                        # Check if the response status code is 200
                        if response.status_code == 200:
                            # Start parser
                            soup = BeautifulSoup(response.text, 'html.parser')
                            cases = ["Именительный", "Родительный", "Дательный", "Винительный", "Творительный", "Предложный"]

                            # Find word in different cases
                            for case in cases:
                                td = soup.find("div", {"class": "td", "data-label": case})
                                if td:
                                    span = td.find('span', class_='transl_form tr_f')
                                    if span.text:
                                        # Check if the region name is not already in the list
                                        if span.text not in unique_region_names:
                                            unique_region_names.append(span.text)
                                            # Write the data for the current row to the output CSV
                                            writer.writerow([region_id, span.text])

                            print(f'Ready: {cyrillic_word}')

                    except Exception as e:
                        print(f"Error processing word '{cyrillic_word}': {e}")

# Print a message indicating the completion of the process
print(f'The result with unique region names was saved in {CSV_OUTPUT}')
