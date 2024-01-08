# This Python script utilizes the spaCy library to perform lemmatization on a CSV file
# containing Russian words and their corresponding counts. The script reads the input CSV, 
# processes each word using spaCy, extracts the lemma of the first token, and saves the results 
# (lemma, original word, count) in a new CSV file. The user can customize input and output file paths, 
# making it adaptable for various datasets.

import csv
import spacy

csv_input = r'C:\Users\romas\Documents\Code\Telegram\Data\word_quantity_full.csv'
csv_output = r'C:\Users\romas\Documents\Code\Telegram\Data\word_quantity_full_lemma.csv'

# Set the language to Russian, large model
nlp = spacy.load("ru_core_news_lg")

# Create a list of Russian words
words = []
# Read words from CSV file
with open(csv_input, 'r', encoding='utf-8') as csv_file:
    word_reader = csv.reader(csv_file)
    next(word_reader)  # Skip the header row
    for row in word_reader:
        words.append((row[0], row[1]))

# Use Spacy to process the words
results = []
for word, count_post in words:
    doc = nlp(word)
    # Take the lemma of the first token (assuming single word input)
    lemma = doc[0].lemma_
    # Add lemma to results
    results.append([lemma, word, count_post])
    print(f'SpaCy: {lemma}, {word}, {count_post}')

# Save results in CSV file with headers 
with open(csv_output, 'w', encoding='utf-8', newline='') as csv_file:
    csv_writer = csv.writer(csv_file)
    # Write the header row to the output CSV
    csv_writer.writerow(['lemma','word', 'count_post'])
    csv_writer.writerows(results)
