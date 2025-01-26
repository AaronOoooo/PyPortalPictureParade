import time
import board
import displayio
import adafruit_imageload
import os
import random

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

# Transition Functions
def fade_out():
    for i in range(255, -1, -10):  # Gradually decrease brightness
        display.brightness = i / 255.0
        time.sleep(0.02)
    display.brightness = 0

def fade_in():
    for i in range(0, 256, 10):  # Gradually increase brightness
        display.brightness = i / 255.0
        time.sleep(0.02)
    display.brightness = 1.0

def slide_in(tile_grid, direction="left"):
    steps = 20
    for step in range(steps + 1):
        if direction == "left":
            tile_grid.x = -320 + (320 * step // steps)
        elif direction == "right":
            tile_grid.x = 320 - (320 * step // steps)
        elif direction == "up":
            tile_grid.y = -240 + (240 * step // steps)
        elif direction == "down":
            tile_grid.y = 240 - (240 * step // steps)
        time.sleep(0.02)
    tile_grid.x, tile_grid.y = 0, 0

def wipe_transition(tile_grid, direction="left"):
    steps = 20
    for step in range(steps + 1):
        if direction == "left":
            tile_grid.x = -320 * step // steps
        elif direction == "right":
            tile_grid.x = 320 * step // steps
        elif direction == "up":
            tile_grid.y = -240 * step // steps
        elif direction == "down":
            tile_grid.y = 240 * step // steps
        time.sleep(0.02)

def zoom_in(image, palette):
    steps = 10
    for step in range(steps + 1):
        scale = 1 + step / steps  # Gradual zoom in
        new_tile_grid = displayio.TileGrid(
            image,
            pixel_shader=palette,
            x=int((320 - (320 * scale)) // 2),  # Center horizontally
            y=int((240 - (240 * scale)) // 2),  # Center vertically
        )
        group = displayio.Group()
        group.append(new_tile_grid)
        display.root_group = group
        time.sleep(0.05)

def zoom_out(image, palette):
    steps = 10
    for step in range(steps + 1):
        scale = 2 - step / steps  # Gradual zoom out
        new_tile_grid = displayio.TileGrid(
            image,
            pixel_shader=palette,
            x=int((320 - (320 * scale)) // 2),  # Center horizontally
            y=int((240 - (240 * scale)) // 2),  # Center vertically
        )
        group = displayio.Group()
        group.append(new_tile_grid)
        display.root_group = group
        time.sleep(0.05)

def random_transition(tile_grid, image, palette):
    transitions = ["fade", "slide", "wipe", "zoom"]
    choice = random.choice(transitions)

    if choice == "fade":
        fade_out()
        fade_in()
    elif choice == "slide":
        slide_in(tile_grid, random.choice(["left", "right", "up", "down"]))
    elif choice == "wipe":
        wipe_transition(tile_grid, random.choice(["left", "right", "up", "down"]))
    elif choice == "zoom":
        if random.choice([True, False]):
            zoom_in(image, palette)
        else:
            zoom_out(image, palette)

# Function to load and display an image with a random transition
def show_image(image_file):
    try:
        display.root_group = None  # Free up memory

        # Load the BMP image
        with open(image_file, "rb") as file:
            image, palette = adafruit_imageload.load(
                file, bitmap=displayio.Bitmap, palette=displayio.Palette
            )

        # Create the initial TileGrid and group
        tile_grid = displayio.TileGrid(image, pixel_shader=palette)
        group = displayio.Group()
        group.append(tile_grid)

        # Add the initial group to the display
        display.root_group = group

        # Perform a random transition
        random_transition(tile_grid, image, palette)

    except OSError as e:
        print(f"Error loading image {image_file}: {e}")

# Main loop for the slideshow
while True:
    for image_file in IMAGE_FILES:
        full_path = IMAGE_FOLDER + image_file  # Build the full file path
        print(f"Attempting to load image: {full_path}")
        show_image(full_path)  # Attempt to show the image
        time.sleep(3)  # Display each image for 3 seconds
