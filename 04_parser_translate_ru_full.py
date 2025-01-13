# Code gets words from CSV file
# generates link for each word to create link for translate.ru
# extracts word's forms for all parts of speech from translate.ru
# saves data in new CSV file

import csv
from urllib.parse import quote
import requests
from bs4 import BeautifulSoup

CSV_INPUT = r'C:\Users\romas\Documents\Code\Telegram\Analyze_12.01.2025\eng_words.csv'
CSV_OUTPUT = r'C:\Users\romas\Documents\Code\Telegram\Analyze_12.01.2025\words_vocabulary_eng.csv'

base_url = "https://www.translate.ru/%D1%81%D0%BF%D1%80%D1%8F%D0%B6%D0%B5%D0%BD%D0%B8%D0%B5%20%D0%B8%20%D1%81%D0%BA%D0%BB%D0%BE%D0%BD%D0%B5%D0%BD%D0%B8%D0%B5/%D1%80%D1%83%D1%81%D1%81%D0%BA%D0%B8%D0%B9/{word}"

def encode_cyrillic_to_hex(input_text):
    encoded_text = quote(input_text, encoding='utf-8')
    return encoded_text

# List to keep track of unique region names
unique_words = []

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
        # writer.writerow([columns[0]])

        # Iterate through the rest of the rows
        for row in csv_reader:
            # Get the region_id from the first column
            word_id = row[0]

            # Iterate through columns starting from the second column
            for col_index in range(0, len(row)):
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

                            # Find all spans with class 'transl_form tr_f'
                            span_list = soup.find_all("span", class_='transl_form tr_f')
                            f_list = soup.find_all("f")
                            value_list = soup.find_all("value")

                            # Iterate through the span elements
                            for s in span_list:
                                if s.text:
                                    # Split the text on ' / ' and iterate through the resulting parts
                                    for part in s.text.split(' / '):
                                        # Check if the part is not already in the list
                                        if part not in unique_words:
                                            # Add the part to the list of unique words
                                            unique_words.append(part)
                                            
                                            # Write the data for the current row to the output CSV
                                            writer.writerow([word_id, part])

                            for f in f_list:
                                if f.contents:
                                    f_text = f.contents[0]
                                    if f_text not in unique_words:
                                        unique_words.append(f_text)
                                        writer.writerow([word_id, f_text])
                                    
                            # Iterate through the value elements
                            for v in value_list:
                                if v.text:
                                    # Check if the <value> tag has an <f> tag inside
                                    if not v.find("f"):
                                        v_text = v.text
                                        if v_text not in unique_words:
                                            unique_words.append(v_text)
                                            writer.writerow([word_id, v_text])

                            print(f'Ready: {cyrillic_word}')   

                    except Exception as e:
                        print(f"Error processing word '{cyrillic_word}': {e}")

# Print a message indicating the completion of the process
print(f'The result with unique word names was saved in {CSV_OUTPUT}')
