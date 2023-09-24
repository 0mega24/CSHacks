# CSHacks
## Image Parsing and Color Palette Generator  

Based on the idea of cluster sorting I take an image and sort its unique colors based on a custom algorithm.  
  
Due to the ability to near losslessly convert from the RGB color space to the HSV color space I am able to  
take the image and sort it by clustering pixels based on their hue making subsets of the unique list so they can be sorted again. 

The way that I used this was to allow for a four tiered sorting system making smaller and smaller more specific  
sub-lists for each aspect the hue, saturation, value, and alpha.  

## Algorithmic Theory
The project description above allows me to jump into how the algorithm is intended to work.