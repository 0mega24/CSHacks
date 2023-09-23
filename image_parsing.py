"""
The backbone of the project a module to take an image input and parse it down to a
list/set of values of each pixel containing either the hue, saturation, value, and alpha value or the RGBA components.
Ignoring alpha 0 pixels while still preserving all other alpha values
"""

from PIL import Image
import colorsys
import numpy

def getImageArray(image_file):
    """
    A method that takes a image file and returns the array of all RGBA values with an x and y coordinate system
    """
    image = Image.open(image_file)
    image_pixel_array = image.load()

    return image_pixel_array

def getHSVAfromRGBA(pixel_array, x, y):
    """
    A method to take an x and y coordinate and a pixel array to return the HSVA values
    """
    pixel = pixel_array(x, y)
    hsv = colorsys.rgb_to_hsv(pixel[0], pixel[1], pixel[2])



def main():
    """
    Main
    """
    image_file_path = f"S:/Windows 10 Host OS/Minecraft/Resources/Textures/item/amethyst_shard.png"
    pixels = getImageArray(image_file_path)
    print(pixels[8, 8])

if __name__ == "__main__":
    main()