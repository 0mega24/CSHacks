"""
The backbone of the project a module to take an image input and parse it down to a
list/set of values of each pixel containing either the hue, saturation, value, and alpha value or the RGBA components.
Ignoring alpha 0 pixels while still preserving all other alpha values

The second major portion is the 4 layers of sorting and clustering
Sean Lidy
"""

from PIL import Image, ImageDraw
import colorsys
import math

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

def clumpByKey(input_list, key_index):
    """
    A more universal method that clumps a list based on a specific key
    """
    input_list.sort(key=lambda x: x[key_index])
    clumped_data = []
    current_group = []    
    for item in input_list:
        if not current_group or item[key_index] == current_group[0][key_index]:
            current_group.append(item)
        else:
            if len(current_group) > 1:
                clumped_data.append(current_group.copy())
            else:
                clumped_data.append(current_group[0])
            current_group = [item]
    if current_group:
        if len(current_group) > 1:
            clumped_data.append(current_group.copy())
        else:
            clumped_data.append(current_group[0])

    return clumped_data

def clumpByHue(unique_color_list):
    """
    A helper function to clump and sort by hue
    """

    return clumpByKey(unique_color_list, 0)

def clumpByValue(unique_color_list):
    """
    A helper function to clump and sort the hue clumps by value
    """
    temp_list = []
    for sublist in unique_color_list:
        if len(sublist) == 1 or type(sublist) == tuple:
            temp_list.append(sublist)
        elif len(sublist) == 2:
            temp = sublist
            temp.sort(key=lambda x: x[2])
            temp_list.append(temp)
        else:
            temp = clumpByKey(sublist, 2)
            temp_list.append(temp)
    unique_color_list = temp_list

    return temp_list

def clumpBySaturation(unique_color_list):
    """
    A helper function to clump and sort the value clumps
    """
    temp_list = []
    for sublist in unique_color_list:
        if len(sublist) == 1 or type(sublist) == tuple:
            temp_list.append(sublist)
        elif len(sublist) == 2 and len(sublist[0]) == 0 and len(sublist[1] == 0):
            temp = sublist
            temp.sort(key=lambda x: x[2])
            temp_list.append(temp)
        else:
            for suberlist in sublist:
                if len (suberlist) == 1 or type(suberlist) == tuple:
                    temp_list.append(suberlist)
                elif len(suberlist) == 2 and len(suberlist[0]) == 0 and len(suberlist[1] == 0):
                    temp = suberlist
                    temp.sort(key=lambda x: x[2])
                    temp_list.append(temp)
                else:
                    temp = clumpByKey(suberlist, 1)
                    temp_list.append(temp)
    unique_color_list = temp_list

    return temp_list

def clumpByAlpha(unique_color_list):
    """
    A Helper function to clump and sort the saturation clumps
    """
    temp_list = []
    for sublist in unique_color_list:
        if len(sublist) == 1 or type(sublist) == tuple:
            temp_list.append(sublist)
        elif len(sublist) == 2 and len(sublist[0]) == 0 and len(sublist[1] == 0):
            temp = sublist
            temp.sort(key=lambda x: x[2])
            temp_list.append(temp)
        else:
            for suberlist in sublist:
                if len (suberlist) == 1 or type(suberlist) == tuple:
                    temp_list.append(suberlist)
                elif len(suberlist) == 2 and len(suberlist[0]) == 0 and len(suberlist[1] == 0):
                    temp = suberlist
                    temp.sort(key=lambda x: x[2])
                    temp_list.append(temp)
                else:
                    for subestlist in suberlist:
                        if len (subestlist) == 1 or type(subestlist) == tuple:
                            temp_list.append(subestlist)
                        elif len(subestlist) == 2 and len(subestlist[0]) == 0 and len(subestlist[1] == 0):
                            temp = subestlist
                            temp.sort(key=lambda x: x[3])
                            temp_list.append(temp)
                        else:
                            temp = clumpByKey(subestlist, 3)
                            temp_list.append(temp)
    unique_color_list = temp_list

    return temp_list

def unifiedSort(open_image, color_list):
    """
    The cascading implementation of image processing and clump sorting
    """
    return clumpByAlpha(clumpBySaturation(clumpByValue(clumpByHue(processImage(open_image, color_list)))))

def createImage(color_list):
    """
    A method to take a array of HSVA pixels and return image
    """
    for i in range(0,len(color_list)):
        color_list[i] = getRGBAfromHSVA(color_list[i])

    width, height = len(color_list) * 10, 10
    image = Image.new("RGB", (width, height))
    draw = ImageDraw.Draw(image)

    x_position = 0
    for color in color_list:
        draw.rectangle([x_position, 0, x_position + 10, height], fill=color)
        x_position += 10

    return image

def saveImage(image, image_save_path):
    """
    A method to take a pillow image and a save path and save the image
    """
    image.save(image_save_path)


def visualImageOpen(image):
    """
    A method to take a pillow image and open it with your default system image viewer
    """
    image.show()

def main():
    """
    Main
    """
    image_file_path = f"S:/Windows 10 Host OS/Minecraft/Resources/Textures/item/experience_bottle.png"
    image_save_path = f"S:/Windows 10 Host OS/Minecraft/CSHacks/test.png"

    open_image = openImage(image_file_path)
    color_list = []
    color_list = unifiedSort(open_image, color_list)

    image = createImage(color_list)
    saveImage(image, image_save_path)
    visualImageOpen(image)

if __name__ == "__main__":
    main()