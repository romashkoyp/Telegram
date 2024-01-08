# Code detects JPG files in directory and subdirectories
# extracts Russian text from images
# cleans text from whitespaces
# save result in JSON

from PIL import Image
import pytesseract
import re
import json
import os

# Set the Tesseract executable path
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

# Specify the main folder path containing images
main_folder_path = r'C:\Users\romas\Documents\Code\Telegram\Analysis'
json_output_folder = r'C:\Users\romas\Documents\Code\Telegram\Analysis\Data'
json_output_path = os.path.join(json_output_folder, 'big_image.json')

count_image = 0
results_list = []

# Iterate through all files and subdirectories in the main folder
for folder_path, _, files in os.walk(main_folder_path):
    for filename in files:
        if filename.endswith('.jpg'):
            # Construct the full path for the image
            image_path = os.path.join(folder_path, filename)

            # Open an image file
            img = Image.open(image_path)

            # Specify the language (Russian)
            texts = pytesseract.image_to_string(img, lang='rus')
            if texts:
                count_image += 1
                print(f'Image #{count_image} was processed')
                cleaned_text = re.sub(r'\s+', ' ', texts).strip()

                # Create a dictionary to store the information
                result_dict = {
                    'global_count': count_image,
                    'image_name': filename,
                    'text_from_image': cleaned_text
                }

                results_list.append(result_dict)

# Convert the list of dictionaries to JSON format
json_result = json.dumps(results_list, ensure_ascii=False, indent=2)

# Save the JSON data to a single file in the output folder
with open(json_output_path, 'w', encoding='utf-8') as json_file:
    json_file.write(json_result)

print(f'All results saved to {json_output_path}')
