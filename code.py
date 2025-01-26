import time
import board
import displayio
import adafruit_imageload
import os

# Folder containing images
IMAGE_FOLDER = "/images/"

# Dynamically get all .bmp files in the /images/ folder
IMAGE_FILES = [
    f for f in os.listdir(IMAGE_FOLDER) if f.lower().endswith(".bmp")
]
IMAGE_FILES.sort()  # Sort files alphabetically for consistent order

if not IMAGE_FILES:
    raise RuntimeError("No .bmp files found in the /images/ directory!")
else:
    print(f"Found {len(IMAGE_FILES)} image(s) in the folder.")

# Display setup
display = board.DISPLAY

# Function to load and display an image
def show_image(image_file):
    try:
        display.root_group = None  # Free up memory

        # Load the BMP image
        with open(image_file, "rb") as file:
            image, palette = adafruit_imageload.load(
                file, bitmap=displayio.Bitmap, palette=displayio.Palette
            )

        # Create the TileGrid and group
        tile_grid = displayio.TileGrid(image, pixel_shader=palette)
        group = displayio.Group()
        group.append(tile_grid)

        # Show the image
        display.root_group = group

    except OSError as e:
        print(f"Error loading image {image_file}: {e}")

# Main loop for the slideshow
while True:
    for image_file in IMAGE_FILES:
        full_path = IMAGE_FOLDER + image_file  # Build the full file path
        print(f"Attempting to load image: {full_path}")
        show_image(full_path)  # Display the image
        time.sleep(3)  # Display each image for 3 seconds
