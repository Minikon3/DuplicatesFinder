# Image Duplicate Finder

This Python application helps to find and manage duplicate images in a specified folder using perceptual hashing and a graphical user interface (GUI) to compare and delete similar images.

## Features
- **Similarity Detection**: Uses perceptual hashing (`dHash`) to find images that are visually similar within a folder.
- **Interactive GUI**: Provides a GUI to compare two images side-by-side, showing their file names and resolutions.
- **User Options**: For each pair of similar images, the user can:
  - Delete one of the images.
  - Keep both images.
  - Copy the file name (without extension) to the clipboard.
- **Progress Tracking**: The console logs the total number of duplicates found and updates the user on how many remain to be processed.

## How to Use
1. Place the images to be compared in a folder (default folder is `input_folder`).
2. Run the script. The application will hash each image and look for similar ones.
3. In the GUI, you will be prompted to review each pair of similar images and decide whether to delete one or keep both.

## Customization
You can adjust the similarity threshold by modifying the value of `SIMILARITY_THRESHOLD`. The threshold can be set between `0` (very strict, only identical images) and `64` (more lenient, even loosely similar images). The default is `10`.

### Example
```python
# Adjust similarity threshold
SIMILARITY_THRESHOLD = 10  # Change this value as needed
```

## Requirements
- Python 3.x
- Required Python libraries:
  - `PIL` (from `Pillow`)
  - `imagehash`
  - `tqdm`
  - `tkinter`

You can install the necessary dependencies with:
```
pip install Pillow imagehash tqdm
```

## Running the Application
```
python your_script_name.py
```

## Folder Structure
- **input_folder/**: This is the default folder where your images should be placed.
