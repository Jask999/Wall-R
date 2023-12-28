from PIL import Image
import numpy as np


def get_RGB_dominant_color_1(pil_img):
    img = pil_img.copy()
    # copy is made for orginal image to keep highest quality.

    img.thumbnail((100, 100))
    #resizes into smaller image for faster processing

    paletted = img.convert('P', palette=Image.ADAPTIVE, colors=16)
    # Reduces the image to only 16 colors
    # k-means clustering is used to do this.
    # The 16 colors are the 16 clusters internally created
    # The largest cluster is the most domanint color

    # Find the color that occurs most often
    palette = paletted.getpalette()
    #an array of the 16 rgb values from the reduced image
    color_counts = sorted(paletted.getcolors(), reverse=True)
    # Above sorts the palette array into pairs of two numbers.
    # The first number is for how many times the color is found in the image.
    # The second number describes the color by giving the colors index in the above array.
    palette_index = color_counts[0][1]
    # color_counts[] is in order of most appearences of a color
    # the second number tells the index of the most domanint color in palette[]
    dominant_color1 = palette[palette_index * 3:palette_index * 3 + 3]
    # This just retreives all 3 RBG values from the index of the most domaniant color

    palette_index = color_counts[1][1]
    dominant_color2 = palette[palette_index * 3:palette_index * 3 + 3]

    palette_index = color_counts[2][1]
    dominant_color3 = palette[palette_index * 3:palette_index * 3 + 3]


    return dominant_color1, dominant_color2, dominant_color3





def get_RGB_dominant_color_2(pil_img):
    img = pil_img.copy() # copy is made cause the orginal is somehow altered and this way orginal keeps highest quality

    img.thumbnail((100, 100)) #resizes into smaller image for faster processing, probably keep cause it

    # Reduce colors (uses k-means internally)
    paletted = img.convert('P', palette=Image.ADAPTIVE, colors=16) #converts the image somehow. Info: https://pillow.readthedocs.io/en/stable/reference/Image.html#PIL.Image.Image.convert

    # Find the color that occurs most often
    palette = paletted.getpalette() #an array of the rgb of x (colors = palette_SIZE) colors from the image
    color_counts = sorted(paletted.getcolors(), reverse=True)
    # Above sorts the palette array into pairs of two numbers.
    # The first number is for how many times the color is found in the image.
    # The second number describes the color by giving the colors index in the above array.
    palette_index = color_counts[1][1] # since color_counts[] is in order of most number of appearences of a color, the second number of the first pair tells us the index of the most domanint color in palette[]
    dominant_color2 = palette[palette_index * 3:palette_index * 3 + 3] # This just retreives all 3 RBG values from the index of the most domaniant color
    return dominant_color2


def get_RGB_dominant_color_3(pil_img):
    img = pil_img.copy() # copy is made cause the orginal is somehow altered and this way orginal keeps highest quality

    img.thumbnail((100, 100)) #resizes into smaller image for faster processing, probably keep cause it

    # Reduce colors (uses k-means internally)
    paletted = img.convert('P', palette=Image.ADAPTIVE, colors=16) #converts the image somehow. Info: https://pillow.readthedocs.io/en/stable/reference/Image.html#PIL.Image.Image.convert

    # Find the color that occurs most often
    palette = paletted.getpalette() #an array of the rgb of x (colors = palette_SIZE) colors from the image
    color_counts = sorted(paletted.getcolors(), reverse=True)
    # Above sorts the palette array into pairs of two numbers.
    # The first number is for how many times the color is found in the image.
    # The second number describes the color by giving the colors index in the above array.
    palette_index = color_counts[2][1] # since color_counts[] is in order of most number of appearences of a color, the second number of any pair tells us the index of the most domanint color in palette[]
    dominant_color3 = palette[palette_index * 3:palette_index * 3 + 3] # This just retreives all 3 RBG values from the index of the most domaniant color
    return dominant_color3





def get_light_to_dark_ratio(pil_img):

    img = pil_img.copy()
    img.thumbnail((100, 100))

    paletted = img.convert('P', palette=Image.ADAPTIVE,colors=128)
    RGB_array = paletted.getpalette()

    sorted_array = sorted(paletted.getcolors(), reverse=True)

    light_count = 0
    dark_count = 0
    avg_RGB = []

    for x in range(126):
        #print(RGB_array)
        temp = RGB_array[x * 3:x * 3 + 3]
        try:
            avg = temp[0] / 3 + temp[1] / 3 + temp[2] / 3
        except:
            avg = 0
        avg = round(avg)
        avg_RGB.append(avg)

        if avg_RGB[x] > 100:
            try:
                num = sorted_array[x][0]
            except:
                num = 0
            light_count = light_count + num
        if avg_RGB[x] <= 100:
            try:
                num = sorted_array[x][0]
            except:
                num = 0
            dark_count = dark_count + num

    lightToDarkRatio = light_count / (dark_count + 1) #Prevents divide by zero
    lightToDarkRatio = round(lightToDarkRatio, ndigits=3)

    return lightToDarkRatio

#pil_img = Image.open('SpiderManTesting.jpg')
#LTD = get_light_to_dark_ratio(pil_img)
#print(LTD)

#color1 = get_RGB_dominant_color_1(pil_img)
#color2 = get_RGB_dominant_color_2(pil_img)
#color3 = get_RGB_dominant_color_3(pil_img)

#print(color1)
#print(color2)
#print(color3)

