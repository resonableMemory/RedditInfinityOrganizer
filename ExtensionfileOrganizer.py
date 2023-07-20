# This Script Organises files according to its extension i.e files which are scattered around without a folder will have a common extension folder

import os
import shutil

# Get the current working directory
current_dir = os.getcwd()

# Loop through all the files in the directory
for filename in os.listdir(current_dir):
    # Get the file extension
    extension = os.path.splitext(filename)[1]

    # Exclude the Python script itself from being moved
    if extension == '.py':
        continue

    # Create a folder for the extension if it doesn't exist
    folder_name = extension.upper()[1:] # Remove the '.' from the extension and capitalize it
    folder_path = os.path.join(current_dir, folder_name)
    if not os.path.exists(folder_path):
        os.makedirs(folder_path)

    # Move the file to the corresponding folder
    file_path = os.path.join(current_dir, filename)
    destination_path = os.path.join(folder_path, filename)
    shutil.move(file_path, destination_path)
