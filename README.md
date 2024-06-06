# Image to Video Converter

## Overview

Image to Video Converter is a Python-based desktop application that converts a sequence of images into a video. The application allows users to select a folder containing images, and it generates a video where each image is displayed for a specified duration. Additionally, the application adds a transition effect between images.

## Features

- Select a folder containing images (supports `.jpg`, `.jpeg`, and `.png` formats).
- Automatically calculates the mean width and height of the images to maintain consistent video dimensions.
- Generates a video with a transition effect between images.
- Saves the generated video in the selected folder.

## Requirements

- Python 3.x
- tkinter
- imageio
- Pillow (PIL)
- numpy

## Installation

1. **Clone the repository:**
   ```bash
   git clone https://github.com/yourusername/image-to-video-converter.git
   cd image-to-video-converter
   ```

2. **Install the required Python packages:**
   ```bash
   pip install imageio pillow numpy
   ```

## Usage

1. **Run the application:**
   ```bash
   python image_to_video_converter.py
   ```

2. **Use the application:**
   - Click the "Browse" button to select a folder containing images.
   - Click the "Generate Video" button to start the video generation process.
   - The generated video will be saved in the selected folder as `output.mp4`.

## Script Explanation

### Importing Libraries
```python
import os
import imageio
from PIL import Image, ImageDraw
import numpy as np
import tkinter as tk
from tkinter import filedialog, messagebox
```
- **os**: For file and directory operations.
- **imageio**: For creating the video.
- **Pillow (PIL)**: For handling image processing.
- **numpy**: For numerical operations.
- **tkinter**: For creating the graphical user interface.

### Browsing for Folder
```python
def browse_folder():
    folder_path = filedialog.askdirectory()
    if folder_path:
        path_entry.delete(0, tk.END)
        path_entry.insert(0, folder_path)
```
- Allows the user to select a folder containing images.

### Video Generation
```python
def generate_video():
    folder_path = path_entry.get()
    if not folder_path:
        messagebox.showerror("Error", "Please select a folder containing images.")
        return

    if not os.path.exists(folder_path):
        messagebox.showerror("Error", "Folder does not exist.")
        return

    os.chdir(folder_path)

    images = [img for img in os.listdir(folder_path)
              if img.endswith(".jpg") or
              img.endswith(".jpeg") or
              img.endswith("png")]

    if not images:
        messagebox.showerror("Error", "No images found in the selected folder.")
        return

    images = sorted(images, key=lambda x: int(x.split('.')[0]))

    mean_height = 0
    mean_width = 0
    num_of_images = len(images)

    for file in images:
        im = Image.open(os.path.join(folder_path, file))
        width, height = im.size
        mean_width += width
        mean_height += height

    mean_width = int(mean_width / num_of_images)
    mean_height = int(mean_height / num_of_images)

    mean_width += 16 - (mean_width % 16)
    mean_height += 16 - (mean_height % 16)

    video_name = os.path.join(folder_path, "output.mp4")
    print("Video will be saved as:", video_name)

    writer = imageio.get_writer(video_name, fps=5)

    num_frames_per_image = 40

    for i in range(num_of_images):
        current_image = Image.open(os.path.join(folder_path, images[i])).resize((mean_width, mean_height))
        if i < num_of_images - 1:
            next_image = Image.open(os.path.join(folder_path, images[i + 1])).resize((mean_width, mean_height))
        else:
            next_image = current_image.copy()

        for _ in range(num_frames_per_image):
            frame = Image.new('RGB', (mean_width, mean_height), color='black')
            frame.paste(current_image, (0, -(_*mean_height//num_frames_per_image)))
            frame.paste(next_image, (0, mean_height - (_*mean_height//num_frames_per_image)))
            writer.append_data(np.array(frame))

    writer.close()

    messagebox.showinfo("Success", "Video generated successfully.")
```
- This function generates the video by:
  - Checking the folder and images.
  - Calculating the mean dimensions of the images.
  - Creating the video with the specified frame rate and transition effect.

### Main Window
```python
# Create main window
root = tk.Tk()
root.title("Image to Video Converter")

# Label and Entry for folder path
path_label = tk.Label(root, text="Select Folder:")
path_label.grid(row=0, column=0, padx=5, pady=5, sticky="w")

path_entry = tk.Entry(root, width=50)
path_entry.grid(row=0, column=1, padx=5, pady=5)

browse_button = tk.Button(root, text="Browse", command=browse_folder)
browse_button.grid(row=0, column=2, padx=5, pady=5)

# Button to generate video
generate_button = tk.Button(root, text="Generate Video", command=generate_video)
generate_button.grid(row=1, column=1, padx=5, pady=5)

# Run the main event loop
root.mainloop()
```
- Sets up the graphical user interface for selecting the folder and generating the video.

## License

This project is licensed under the MIT License.
