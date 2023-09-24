"""
The backbone of the project a module to take an image input and parse it down to a
list/set of values of each pixel containing either the hue, saturation, value, and alpha value or the RGBA components.
Ignoring alpha 0 pixels while still preserving all other alpha values

The second major portion is the 4 layers of sorting and clustering
Sean Lidy
"""

from PIL import Image
import colorsys
import numpy

def openImage(image_file):
    """
    - A method to open the image file to be used in other functions to avoid having multiple instances of it in memory
    - Format the method to match the naming convention that I have been using
    """
    return Image.open(image_file)

def getImageArray(image):
    """
    - A method to load the image into an array that can be iterated over
    - Format the method to match the naming convention that I have been using
    """
    return image.load()

def getImageDim(image):
    """
    - Take an open pillow image and return the width and height of the open file
    - Wrap the size function to return 2 values and not a list
    """
    width, height = image.size
    return width, height

def getHSVAfromRGBA(pixel):
    """
    - A method to take a pixel object that contains the R, G, B, A values and convert it into the HSVA color space for sorting reasons
    - Return a tuple containing the H, S, V values as 2 decimal point floats and an int representing the alpha value
    """
    R, G, B, A = pixel
    H, S, V, A = list(colorsys.rgb_to_hsv(R/255, G/255, B/255)) + [A]

    return (round(H, 2), round(S, 2), round(V, 2), A)

def getRGBAfromHSVA(pixel):
    """
    - A method to take a pixel object that contains the H, S, V, A values and convert it into the RGBA color space for image generation reasons
    - Return a tuple containing the R, G, B, A values as ints
    """
    H, S, V, A = pixel
    R, G, B, A = list(colorsys.hsv_to_rgb(H, S, V)) + [A]

    return (int(R * 255), int(G * 255), int(B * 255), A)

def checkAlphaAndAddToList(HSVA, value_list):
    """
    - Takes a list containing HSVA and checks to see if the alpha value is not 0 and then adds it to a list if it is not equal to 0
    - Ignores wether or not it is a unique color or not
    """
    if int(HSVA[3]) != 0:
        value_list.append(HSVA)

        return value_list

def processImage(image, color_list):
    """
    - Takes a pillow image and a color list object and returns a list of all the unique colors within the image
    """
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