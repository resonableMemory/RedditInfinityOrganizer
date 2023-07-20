# This script :
#1. Delete 0 size files in current and sub folders
#2. Find and Add extension to Non extension files
#3. Create folders for files which does not have folders(for files which exists in current directory)
#4. Move all contents from duplicate folders and current Folder(only same prefix content) to the Main folder(of that duplicate folder)

import os
import shutil
import re
import magic

# Function to delete 0 size files
def delete_zero_size_files():
    for root, dirs, files in os.walk("."):
        for filename in files:
            file_path = os.path.join(root, filename)
            if os.path.getsize(file_path) == 0:
                os.remove(file_path)

# Function to find and rename files with no extension using magic
def find_and_rename_files():
    mime = magic.Magic(mime=True)
    for root, dirs, files in os.walk("."):
        for filename in files:
            file_path = os.path.join(root, filename)
            if os.path.splitext(filename)[1] == "":
                guessed_extension = mime.from_file(file_path).split("/")[-1]
                new_file_path = os.path.join(root, filename + "." + guessed_extension)
                os.rename(file_path, new_file_path)

# Function to create folders for non-similar files
def create_folders_for_non_similar_files():
    for root, dirs, files in os.walk("."):
        for filename in files:
            file_path = os.path.join(root, filename)
            if os.path.splitext(filename)[1] != "":
                prefix = re.search(r"(.*)-[a-zA-Z0-9]+", filename)
                if prefix:
                    folder_name = prefix.group(1)
                    if not os.path.exists(folder_name):
                        os.makedirs(folder_name)
                    new_file_path = os.path.join(folder_name, filename)
                    if os.path.exists(new_file_path):
                        new_file_path = os.path.join(folder_name, "copy_" + filename)
                    shutil.move(file_path, new_file_path)


def move_files():
    # Get list of directories and files in current directory
    dirs_and_files = os.listdir()

    # Create dictionary to hold folder names and corresponding prefixes
    folder_prefixes = {}

    # Loop through directories and files to find prefixes
    for item in dirs_and_files:
        if os.path.isdir(item):
            prefix = re.search(r"(.*) \(\d+\)", item)
            if prefix:
                folder_prefixes[item] = prefix.group(1)
        elif os.path.isfile(item):
            prefix = re.search(r"(.*)-[a-zA-Z0-9]+", item)
            if prefix:
                folder_prefixes[item] = prefix.group(1)

    # Loop through directories and files again to move them to their corresponding folder
    for item in dirs_and_files:
        if os.path.isdir(item):
            if item in folder_prefixes:
                # Move contents of duplicate folder to main folder
                for sub_item in os.listdir(item):
                    shutil.move(os.path.join(item, sub_item), folder_prefixes[item])
                os.rmdir(item)
            else:
                # Create new folder if it doesn't exist
                if not os.path.exists(item):
                    os.makedirs(item)
        elif os.path.isfile(item):
            if os.path.getsize(item) == 0:
                os.remove(item)
                continue

            file_ext = os.path.splitext(item)[1]
            if file_ext == '':
                # Find and rename file extension using magic module
                mime = magic.Magic(mime=True)
                file_type = mime.from_file(item)
                new_name = item + '.' + file_type.split('/')[1]
                os.rename(item, new_name)
                item = new_name

            prefix = folder_prefixes.get(item)
            if prefix:
                # Move file to corresponding folder
                new_path = os.path.join(prefix, item)
                while os.path.exists(new_path):
                    file_parts = os.path.splitext(item)
                    new_path = os.path.join(prefix, file_parts[0] + '_1' + file_parts[1])
                shutil.move(item, new_path)
            else:
                # Create new folder and move file
                prefix = re.search(r"(.*)-[a-zA-Z0-9]+", item)
                if prefix:
                    folder_name = prefix.group(1)
                    if not os.path.exists(folder_name):
                        os.makedirs(folder_name)
                    new_path = os.path.join(folder_name, item)
                    while os.path.exists(new_path):
                        file_parts = os.path.splitext(item)
                        new_path = os.path.join(folder_name, file_parts[0] + '_1' + file_parts[1])
                    shutil.move(item, new_path)

def rename_copy_files():
    # Get the current directory
    directory = os.getcwd()
    # Iterate through all files in the directory and its subdirectories
    for root, dirs, files in os.walk(directory):
        for filename in files:
            # Check if the file name starts with "copy_"
            if filename.startswith('copy_'):
                old_path = os.path.join(root, filename)
                # Check if the file is not a directory
                if not os.path.isdir(old_path):
                    new_filename = filename.replace('copy_', '', 1)
                    new_path = os.path.join(root, new_filename)
                    # If the new file name already exists, add a suffix to the file name
                    suffix = 1
                    while os.path.exists(new_path):
                        new_filename = new_filename.rsplit('.', 1)[0] + f'_{suffix}.' + new_filename.rsplit('.', 1)[1]
                        new_path = os.path.join(root, new_filename)
                        suffix += 1
                    # Rename the file
                    os.rename(old_path, new_path)
                    print(f'Renamed {filename} to {new_filename}')

delete_zero_size_files()
find_and_rename_files()
create_folders_for_non_similar_files()
move_files()
rename_copy_files()