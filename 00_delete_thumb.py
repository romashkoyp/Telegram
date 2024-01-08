# Code detects files in folder, which contains thumb in their name and
# transfers these files into desired folder

import os
import shutil

def transfer_files(source_folder, destination_folder):
    # Ensure the source folder exists
    if not os.path.exists(source_folder):
        print(f"Source folder '{source_folder}' does not exist.")
        return

    # Ensure the destination folder exists, or create it
    if not os.path.exists(destination_folder):
        os.makedirs(destination_folder)

    # List all files in the source folder
    files = os.listdir(source_folder)

    # Filter files with 'thumb' in their name
    thumb_files = []

    for file in files:
        if 'thumb' in file:
            thumb_files.append(file)

    count_thumb = 0

    # Move each thumb file to the destination folder
    for thumb_file in thumb_files:
        source_path = os.path.join(source_folder, thumb_file)
        destination_path = os.path.join(destination_folder, thumb_file)
        shutil.move(source_path, destination_path)
        count_thumb += 1
    
    print(f'\nFrom {source_folder}\nto {destination_folder}\ntransfered {count_thumb} thumb files\n')

# Example usage
source_folder = r'C:\Users\romas\Documents\Code\Telegram\Analysis\06_mypervie_2023-12-27\photos'
destination_folder = r'C:\Users\romas\Documents\Code\Telegram\Analysis\06_mypervie_2023-12-27\thumb'
transfer_files(source_folder, destination_folder)
