import os
import time
import board
import displayio
import adafruit_imageload
from adafruit_touchscreen import Touchscreen

# Folder containing images
IMAGE_FOLDER = "/images/"

# Dynamically get all .bmp files in the /images/ folder
IMAGE_FILES = [
    f for f in os.listdir(IMAGE_FOLDER) if f.lower().endswith(".bmp")
]
IMAGE_FILES.sort()

if not IMAGE_FILES:
    raise RuntimeError("No .bmp files found in the /images/ directory!")
else:
    print(f"Found {len(IMAGE_FILES)} image(s) in the folder.")

# Display and Touchscreen setup
display = board.DISPLAY
touch = Touchscreen(
    board.TOUCH_XL, board.TOUCH_XR, board.TOUCH_YD, board.TOUCH_YU,
    calibration=None, size=(320, 240)
)

# Button Definitions
BUTTON_WIDTH = 80
BUTTON_HEIGHT = 40
BUTTON_Y = 200  # Position near the bottom of the screen

buttons = {
    "previous": {"x": 20, "y": BUTTON_Y, "color": 0xFF0000},
    "pause": {"x": 120, "y": BUTTON_Y, "color": 0x00FF00},
    "next": {"x": 220, "y": BUTTON_Y, "color": 0x0000FF},
}

def create_button_group():
    """Create a new button group."""
    button_group = displayio.Group()
    for label, props in buttons.items():
        # Create a colored button rectangle
        button = displayio.TileGrid(
            displayio.Bitmap(BUTTON_WIDTH, BUTTON_HEIGHT, 1),
            pixel_shader=displayio.Palette(1),
            x=props["x"],
            y=props["y"]
        )
        button.pixel_shader[0] = props["color"]  # Set button color
        button_group.append(button)
    return button_group


def show_image(index):
    """Load and display an image based on the index."""
    try:
        # Reset the display root group to free memory
        display.root_group = None

        # Load the BMP image
        image_file = IMAGE_FOLDER + IMAGE_FILES[index]
        with open(image_file, "rb") as file:
            image, palette = adafruit_imageload.load(
                file, bitmap=displayio.Bitmap, palette=displayio.Palette
            )

        # Create a new TileGrid and Group for the image
        tile_grid = displayio.TileGrid(image, pixel_shader=palette)
        group = displayio.Group()
        group.append(tile_grid)

        # Create a fresh button group and add to the group
        fresh_button_group = create_button_group()
        group.append(fresh_button_group)

        # Assign the new group to the display
        display.root_group = group

    except OSError as e:
        print(f"Error loading image: {e}")

def handle_touch():
    """Handle touchscreen presses and map them to button actions."""
    global current_image_index, paused
    touch_point = touch.touch_point
    if touch_point:
        x, y, z = touch_point  # Extract touch coordinates
        if buttons["previous"]["x"] <= x <= buttons["previous"]["x"] + BUTTON_WIDTH and \
           buttons["previous"]["y"] <= y <= buttons["previous"]["y"] + BUTTON_HEIGHT:
            print("Previous button pressed")
            current_image_index = (current_image_index - 1) % len(IMAGE_FILES)
            show_image(current_image_index)
        elif buttons["next"]["x"] <= x <= buttons["next"]["x"] + BUTTON_WIDTH and \
             buttons["next"]["y"] <= y <= buttons["next"]["y"] + BUTTON_HEIGHT:
            print("Next button pressed")
            current_image_index = (current_image_index + 1) % len(IMAGE_FILES)
            show_image(current_image_index)
        elif buttons["pause"]["x"] <= x <= buttons["pause"]["x"] + BUTTON_WIDTH and \
             buttons["pause"]["y"] <= y <= buttons["pause"]["y"] + BUTTON_HEIGHT:
            print("Pause/Resume button pressed")
            paused = not paused  # Toggle paused state

# Display state variables
current_image_index = 0
paused = False

# Main loop for the slideshow
show_image(current_image_index)  # Show the first image
while True:
    handle_touch()  # Check for button presses
    if not paused:
        time.sleep(3)  # Wait before showing the next image
        current_image_index = (current_image_index + 1) % len(IMAGE_FILES)
        show_image(current_image_index)
