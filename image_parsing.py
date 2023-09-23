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

def getImageDim(image_file):
    image = Image.open(image_file)
    width, height = image.size
    return width, height

def getHSVAfromRGBA(pixel_array, x, y):
    """
    A method to take an x and y coordinate and a pixel array to return the HSVA values
    """
    R, G, B, A = pixel_array[x, y]

    return list(colorsys.rgb_to_hsv(R/255, G/255, B/255)) + [A]

def nonVectorizedAlphaCheckerAndSetCreator(pixel_array, x, y, unique_value_set):
    """
    Takes a list containing HSVA and checks to see if the alpha value is not 0 and then adds it to a set if it is not equal to 0
    """
    HSVA = getHSVAfromRGBA(pixel_array, x, y)
    if int(HSVA[3]) != 0:
        unique_value_set.add(HSVA)
        return unique_value_set


def main():
    """
    Main
    """
    image_file_path = f"S:/Windows 10 Host OS/Minecraft/Resources/Textures/item/amethyst_shard.png"
    
    
    # pixels = getImageArray(image_file_path)
    # H, S, V, A = getHSVAfromRGBA(pixels, 8, 8)
    # H *= 360
    # print(round(H, -1), round(S, 2), round(V, 2), A)
    # print(pixels[8, 8])

if __name__ == "__main__":
    main()