# Code detects all html files in input folder and
# creates only one html file with whole content from html files

import os
from bs4 import BeautifulSoup

def combine_html_files(output_file, input_folder):
    # Create a new combined HTML file
    with open(output_file, 'w', encoding='utf-8-sig') as combined_file:
        # Write the HTML structure
        combined_file.write('<html>\n<head>\n</head>\n<body>\n')

        # Iterate through HTML files in the input folder
        for filename in os.listdir(input_folder):
            if filename.endswith('.html'):
                file_path = os.path.join(input_folder, filename)

                # Read the content of each HTML file
                with open(file_path, 'r', encoding='utf-8-sig') as file:
                    content = file.read()

                # Parse the content using BeautifulSoup
                soup = BeautifulSoup(content, 'html.parser')

                # Extract the body content and write it to the combined file
                body_content = soup.body.prettify()
                combined_file.write(body_content)

        # Close the HTML structure
        combined_file.write('\n</body>\n</html>')

if __name__ == "__main__":
    # Specify input folder and output file
    input_folder = r'C:\Users\romas\Documents\Code\Telegram\Analysis\06_mypervie_2023-12-27'
    output_file = r'C:\Users\romas\Documents\Code\Telegram\Analysis\06_mypervie_2023-12-27\combined.html'

    # Call the function to combine HTML files
    combine_html_files(output_file, input_folder)

    print(f'HTML files from {input_folder} combined successfully. Check {output_file}.')
