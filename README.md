# PyPortalPictureParade
# PyPortal Picture Parade

**PyPortal Picture Parade** is a dynamic image slideshow designed for the Adafruit PyPortal. It automatically detects `.bmp` files in the `/images` directory and displays them on the PyPortal screen. Perfect for creating digital photo frames, art displays, or IoT dashboards!

## Features
- **Dynamic File Detection**: Automatically displays any `.bmp` files added to the `/images/` folder.
- **Error Handling**: Skips problematic images and continues the slideshow.
- **Memory Management**: Ensures smooth performance on the PyPortal.

## Getting Started

1. **Install CircuitPython** on your PyPortal.
   - Download from [CircuitPython.org](https://circuitpython.org/board/pyportal/).
2. **Add Required Libraries**:
   - Download the CircuitPython library bundle from [Adafruit](https://circuitpython.org/libraries).
   - Copy `adafruit_imageload` to the `lib/` folder on the PyPortal.
3. **Set Up the Project**:
   - Copy `code.py` to the root of your PyPortal's `CIRCUITPY` drive.
   - Create an `images/` folder and add `.bmp` files (320x240, RGB565 format).
4. **Run the Slideshow**:
   - The PyPortal will automatically start displaying the images in alphabetical order.

## Resizing and Converting Images

To ensure compatibility with PyPortal, all images must be resized to **320x240 pixels** and converted to the **BMP** format with the correct color depth.

### Steps to Resize and Convert:

1. **Resize the Image**:
   - You can use any image editor (e.g., Photoshop, GIMP, or Microsoft Paint) to resize the image to **320x240 pixels**.
   - Alternatively, online tools like [ResizePixel](https://www.resizepixel.com/) can be used.

2. **Convert to BMP Format**:
   - Go to [Online BMP Converter](https://online-converting.com/image/convert2bmp/).
   - Upload your resized image.
   - In the **Color** section, select **"16 (5:5:5:1, RGB Hi Color)"**.
   - Leave all other settings as default.
   - Click **Convert** and download the `.bmp` file.

3. **Transfer the Image**:
   - Move the `.bmp` file to the `CIRCUITPY/images/` folder on your PyPortal.

Once the images are correctly formatted and placed in the `/images/` directory, they will be automatically displayed in the slideshow.

## Example Images
Add example `.bmp` files to the `images/` folder for easy testing.

## Contributing
Contributions are welcome! Feel free to open issues or submit pull requests.

## License
This project is licensed under the [MIT License](LICENSE).
