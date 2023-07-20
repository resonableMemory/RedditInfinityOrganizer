# Issue in Infinity For Reddit: when we tap on download button multiple times it creates files like 'file.extension' and 'file.extension (1)' which makes 'file.extension (1) unusable'
# What This Script Does:
# 1. Deleted files having 0 size.
# 2. If both files are of same size then deletes the one which having '(1), etc'
# 3. if one of them size is lesser than the other, it deletes that file.
# 4. Checks if Every media file is valid and is not incomplete download file. If yes, then it deletes it.
# 5. Renames 'file.extension (1)' to a proper format file name example 'file-RandomString.extension'


import os
import re
import random
import string
import hashlib
from PIL import Image
from moviepy.editor import VideoFileClip
import json
import concurrent.futures
from functools import partial

# Function to delete files with 0 size
def delete_zero_size_files(directory):
    for root, dirs, files in os.walk(directory):
        for filename in files:
            filepath = os.path.join(root, filename)
            if os.path.getsize(filepath) == 0:
                os.remove(filepath)
                print(f"Deleted file: {filepath}")

# Function to rename files with (anyNumber) format
def rename_files(directory, checked_files):
    for root, dirs, files in os.walk(directory):
        file_contents = {}  # Dictionary to store file contents and corresponding file paths
        for filename in files:
            filepath = os.path.join(root, filename)
            if os.path.isfile(filepath) and not filepath.endswith(('.py', '.json')):
                if filepath in checked_files:
                    print(f"Skipping checked file: {filepath}")
                    continue  # Skip already checked files
                file_hash = hash_file(filepath)
                if file_hash in file_contents:
                    existing_file = file_contents[file_hash]
                    if len(filepath) > len(existing_file):
                        os.remove(filepath)
                        print(f"Deleted file: {filepath} (identical file found)")
                    else:
                        os.remove(existing_file)
                        print(f"Deleted file: {existing_file} (identical file found)")
                        file_contents[file_hash] = filepath
                else:
                    file_contents[file_hash] = filepath

        # Save the checked files for this folder
        folder_checked_files_file = os.path.join(root, 'checked_files.json')
        save_checked_files(folder_checked_files_file, list(file_contents.keys()))

# Function to calculate the hash value of a file
def hash_file(filepath):
    BLOCKSIZE = 65536
    sha256_hash = hashlib.sha256()
    with open(filepath, 'rb') as file:
        buf = file.read(BLOCKSIZE)
        while len(buf) > 0:
            sha256_hash.update(buf)
            buf = file.read(BLOCKSIZE)
    print(f"Hash calculated for: {filepath}")
    return sha256_hash.hexdigest()

# Function to validate image files
def validate_image(filepath, checked_files):
    try:
        Image.open(filepath).verify()
        print(f"Valid image: {filepath}")
        checked_files.add(filepath)
    except (IOError, SyntaxError) as e:
        print(f"Invalid image: {filepath}, Error: {str(e)}")
        os.remove(filepath)
        print(f"Deleted file: {filepath}")

# Function to validate video files
def validate_video(filepath, checked_files):
    try:
        video = VideoFileClip(filepath)
        print(f"Valid video: {filepath}")
        checked_files.add(filepath)
    except Exception as e:
        print(f"Invalid video: {filepath}, Error: {str(e)}")
        os.remove(filepath)
        print(f"Deleted file: {filepath}")

# Save checked files to a JSON file
def save_checked_files(file_path, checked_files):
    with open(file_path, 'w') as file:
        json.dump(list(checked_files), file)

# Function to close audio reader process
# Function to close audio reader process
def close_audio_reader_process(process):
    try:
        process.terminate()
    except Exception as e:
        print(f"Failed to terminate audio reader process: {str(e)}")

# Validate image file partially
def validate_image_partial(filepath, checked_files):
    validate_image(filepath, checked_files)

# Validate video file partially
def validate_video_partial(filepath, checked_files):
    validate_video(filepath, checked_files)

# Specify the directory to perform the operations
directory = '.'  # Change this to the desired directory path

# Delete files with 0 size
print("Deleting files with 0 size...")
delete_zero_size_files(directory)

# Validate image and video files, and rename files with (anyNumber) format
for root, dirs, files in os.walk(directory):
    folder_checked_files_file = os.path.join(root, 'checked_files.json')
    if os.path.isfile(folder_checked_files_file):
        with open(folder_checked_files_file, 'r') as file:
            checked_files = set(json.load(file))
        print(f"Loaded checked files from {folder_checked_files_file}: {checked_files}")
    else:
        checked_files = set()
        print(f"No checked files found. Starting fresh.")

    with concurrent.futures.ThreadPoolExecutor(max_workers=12) as executor:
        validate_image_partial = partial(validate_image_partial, checked_files=checked_files)
        validate_video_partial = partial(validate_video_partial, checked_files=checked_files)

        for filename in files:
            filepath = os.path.join(root, filename)
            if filename.lower().endswith(('.jpeg', '.jpg', '.png', '.gif')) and not filepath.endswith(('.py', '.json')):
                if filepath in checked_files:
                    print(f"Skipping checked image file: {filepath}")
                    continue  # Skip already checked files
                executor.submit(validate_image_partial, filepath)
            elif filename.lower().endswith('.mp4') and not filepath.endswith(('.py', '.json')):
                if filepath in checked_files:
                    print(f"Skipping checked video file: {filepath}")
                    continue  # Skip already checked files
                executor.submit(validate_video_partial, filepath)

    # Wait for all tasks to complete
    executor.shutdown()

    # Save the checked files for this folder
    save_checked_files(folder_checked_files_file, checked_files)
    print(f"Saved checked files to {folder_checked_files_file}: {checked_files}")
