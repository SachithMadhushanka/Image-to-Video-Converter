import os
import imageio
from PIL import Image, ImageDraw  # Import ImageDraw module
import numpy as np
import tkinter as tk
from tkinter import filedialog, messagebox

# Function to select folder containing images
def browse_folder():
    folder_path = filedialog.askdirectory()
    if folder_path:
        path_entry.delete(0, tk.END)
        path_entry.insert(0, folder_path)

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

# Video Generating function
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

    # Sort the images based on their numbers
    images = sorted(images, key=lambda x: int(x.split('.')[0]))

    mean_height = 0
    mean_width = 0
    num_of_images = len(images)

    # calculate the mean height and width of all the images
    for file in images:
        im = Image.open(os.path.join(folder_path, file))
        width, height = im.size
        mean_width += width
        mean_height += height

    mean_width = int(mean_width / num_of_images)
    mean_height = int(mean_height / num_of_images)

    # Make dimensions divisible by 16
    mean_width += 16 - (mean_width % 16)
    mean_height += 16 - (mean_height % 16)

    video_name = os.path.join(folder_path, "output.mp4")
    print("Video will be saved as:", video_name)

    # Create an imageio VideoWriter object
    writer = imageio.get_writer(video_name, fps=5)  # Explicitly set frame rate to 5 fps

    # Number of frames to display each image
    num_frames_per_image = 40  # Adjust this value to change the duration of each image

    # Add numbers to each image and write to the video
    for i in range(num_of_images):
        current_image = Image.open(os.path.join(folder_path, images[i])).resize((mean_width, mean_height))
        if i < num_of_images - 1:
            next_image = Image.open(os.path.join(folder_path, images[i + 1])).resize((mean_width, mean_height))
        else:
            next_image = current_image.copy()

        for _ in range(num_frames_per_image):
            # Create a blank canvas to draw the image and fading effect
            frame = Image.new('RGB', (mean_width, mean_height), color='black')

            # Paste the current image onto the canvas
            frame.paste(current_image, (0, -(_*mean_height//num_frames_per_image)))
            
            # Paste the next image onto the canvas
            frame.paste(next_image, (0, mean_height - (_*mean_height//num_frames_per_image)))
            
            writer.append_data(np.array(frame))

    # Close the writer
    writer.close()

    messagebox.showinfo("Success", "Video generated successfully.")


# Button to generate video
generate_button = tk.Button(root, text="Generate Video", command=generate_video)
generate_button.grid(row=1, column=1, padx=5, pady=5)

# Run the main event loop
root.mainloop()
