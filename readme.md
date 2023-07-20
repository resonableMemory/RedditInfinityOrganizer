# File Organizer and Cleaner for Infinity for Reddit

This project consists of three Python scripts: `duplicateFolderSorter.py`, `ExtensionfileOrganizer.py`, and `redundantAndInvalidRemover.py`. Each script serves a specific purpose to help you organize and clean up files downloaded from Infinity for Reddit app.

Please note that these issues were encountered while running the Infinity for Reddit app on Android 8. The provided scripts aim to address these issues and streamline the organization and cleanup of downloaded files.

Additionally, please note that this project was created for personal use to organize files before making a backup. You are welcome to use, modify, and distribute the scripts as per the terms of the [MIT License](LICENSE). Feel free to adapt the code to suit your needs and use it in your own projects.


## duplicateFolderSorter.py

### Functionality:

This script specifically addresses an issue caused by the Infinity for Reddit app, where it generates multiple duplicate folders for the same subreddit. For example: `Aww`, `Aww(1)`.

The script performs the following tasks:

1. Merges all files from duplicate folders (e.g., `Aww(1)`) into the main folder (e.g., `Aww`).
2. Deletes the duplicate folders once the files have been merged.

## ExtensionfileOrganizer.py

### Functionality:

This script organizes files based on their extensions. Files that are scattered around without a folder will be grouped into a common extension folder.

## redundantAndInvalidRemover.py

### Functionality:

This script addresses an issue in Infinity for Reddit where tapping on the download button multiple times creates files like `file.extension` and `file.extension (1)`, making `file.extension (1)` unusable. The script performs the following tasks:

1. Deletes files with 0 size.
2. If two files have the same size, it deletes the one with the `(1)` suffix, and so on.
3. If one file's size is lesser than the other, it deletes that file.
4. Checks if every media file is valid and not an incomplete download file. If it's invalid, it will be deleted.
5. Renames `file.extension (1)` to a properly formatted file name, for example, `file-RandomString.extension`.

Additionally, for efficiency purposes, each folder also maintains a `checked_file.json` to keep track of validated files. If a file has been validated before, it won't be validated again to save time, especially when dealing with a large number of files.



## How to Use

1. Ensure you have Python installed on your system (compatible version: Python 3.x).
2. Download the three Python scripts: `duplicateFolderSorter.py`, `ExtensionfileOrganizer.py`, and `redundantAndInvalidRemover.py`.
3. Place the scripts in the directory where you want to organize and clean up your files.
4. Open a terminal or command prompt and navigate to the directory where the scripts are located.
5. Run each script by executing the following commands:
```bash
python duplicateFolderSorter.py
python ExtensionfileOrganizer.py
python redundantAndInvalidRemover.py
```
6. Follow the on-screen prompts to proceed with the organization and cleanup process.

**Note:** Before running the scripts, it's advisable to create a backup of your files, as the operations performed by the scripts are irreversible.

## License

This project is licensed under the [MIT License](LICENSE).
