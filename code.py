import time
import board
import displayio
import adafruit_imageload
import os

# Configuration
IMAGE_FOLDER = "/images/"
SLIDE_DURATION = 3  # Seconds
FADE_DELAY = 0.2    # Seconds

# Dynamically get all .bmp files in the /images/ folder
IMAGE_FILES = [
    IMAGE_FOLDER + f for f in os.listdir(IMAGE_FOLDER) if f.lower().endswith(".bmp")
]
IMAGE_FILES.sort()  # Sort files alphabetically for consistent order

if not IMAGE_FILES:
    raise RuntimeError("No .bmp files found in the /images/ directory!")
else:
    print(f"Found {len(IMAGE_FILES)} image(s) in the folder.")

# Display setup
display = board.DISPLAY

# Transition Functions
def fade_out():
    """Gradually decrease screen brightness to create a fade-out effect."""
    for brightness in range(10, -1, -1):  # 10 to 0
        display.brightness = brightness / 10.0
        time.sleep(FADE_DELAY)
    display.brightness = 0

def fade_in():
    """Gradually increase screen brightness to create a fade-in effect."""
    for brightness in range(0, 11):  # 0 to 10
        display.brightness = brightness / 10.0
        time.sleep(FADE_DELAY)
    display.brightness = 1.0

# Function to load and display an image with fade transitions
def show_image(image_file):
    try:
        # Fade out the current screen before loading the next image
        fade_out()
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

        # Fade in the new image
        fade_in()

    except OSError as e:
        print(f"Error loading image {image_file}: {e}")

# Main loop for the slideshow
while True:
    for image_file in IMAGE_FILES:
        print(f"Attempting to load image: {image_file}")
        show_image(image_file)  # Display the image with fade transitions
        time.sleep(SLIDE_DURATION)  # Display each image for the specified duration