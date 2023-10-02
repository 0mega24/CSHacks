# CSHacks
## Image Parsing and Color Palette Generator  

Based on the idea of cluster sorting I take an image and sort its unique colors based on a custom algorithm.  
  
Due to the ability to near losslessly convert from the RGB color space to the HSV color space I am able to  
take the image and sort it by clustering pixels based on their hue making subsets of the unique list so they can be sorted again. 

The way that I used this was to allow for a four tiered sorting system making smaller and smaller more specific  
sub-lists for each aspect the hue, saturation, value, and alpha.  

## Algorithmic Theory
The project description above allows me to jump into how the algorithm is intended to work.

For this algorithm I took a staged clustering approach. As seen in the code below.

```py
def unifiedSort(open_image, color_list):
    """
    The cascading implementation of image processing and clump sorting
    """
    return clumpByAlpha(clumpBySaturation(clumpByValue(clumpByHue(processImage(open_image, color_list)))))
```

Each stage of the sorting algorithm is represented by a object that gets passed down.  
To get the sorting algorithm to work I take a set (exclusive list/no repetition) to limit myself to dealing with unique values only. Based on the naming in my head I thought of the code as a clumping sort meaning that it takes subsets of the list and opportunities on them one by one without resorting the entire list. 

```py
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
```
This is the final stage of the algorithm where it checks for any lists that have the same H, S, and V values before sorting that subset by the Alpha value.

## Examples
Textures that had a limited color palette and were mostly shades of one color lead to very pleasing results.  
## ![](README/bamboo_singleleaf.png) ![ ](README/amethyst_shard.png) ![](README/carrot.png)
## ![](README/axolotl_bucket.png)
## ![](README/emerald_ore.png) ![](README/emerald.png) ![](README/emerald_block.png)
## ![](README/beacon.png) ![](README/dark_oak_sapling.png) ![](README/heart_of_the_sea.png) 
## ![](README/honeycomb.png) ![](README/medium_amethyst_bud.png) ![](README/milk_bucket.png)
## ![](README/debug.png)
## ![](README/comparator_on.png) ![](README/bowl.png)
## ![](README/birch_chest_boat.png) 