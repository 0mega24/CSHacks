"""
The backbone of the project a module to take an image input and parse it down to a
list/set of values of each pixel containing either the hue, saturation, value, and alpha value or the RGBA components.
Ignoring alpha 0 pixels while still preserving all other alpha values
Sean Lidy
"""

from PIL import Image
import colorsys
import numpy
import time

def openImage(image_file):
    """
    Open the image file to be used in other functions to avoid having multiple instances of it in memory
    """
    return Image.open(image_file)

def getImageArray(image):
    """
    A method that takes a image file and returns the array of all RGBA values with an x and y coordinate system
    """
    image_pixel_array = image.load()

    return image_pixel_array

def getImageDim(image):
    """
    Take an open pillow image and return the width and height of the open file
    """
    width, height = image.size
    return width, height

def getHSVAfromRGBA(RGBA):
    """
    A method to take an x and y coordinate and a pixel array to return the HSVA values
    """
    R, G, B, A = RGBA

    H, S, V, A = list(colorsys.rgb_to_hsv(R/255, G/255, B/255)) + [A]

    return (round(H, 2), round(S, 2), round(V, 2), A)

def checkAlphaAndAddToList(HSVA, value_list):
    """
    Takes a list containing HSVA and checks to see if the alpha value is not 0 and then adds it to a set if it is not equal to 0
    """
    if int(HSVA[3]) != 0:
        value_list.append(HSVA)

        return value_list

def processImage(image, color_list):
    pixels = getImageArray(image)
    width, height = getImageDim(image)
    for x in range(width):
        for y in range(height):
            HSVA = getHSVAfromRGBA(pixels[x, y])
            checkAlphaAndAddToList(HSVA, color_list)
    return list(set(color_list))

def main():
    """
    Main
    """
    image_file_path = f"S:/Windows 10 Host OS/Minecraft/Resources/Textures/item/amethyst_shard.png"

    open_image = openImage(image_file_path)

    color_list = []
    color_list = processImage(open_image, color_list)

    print(color_list)

if __name__ == "__main__":
    main()