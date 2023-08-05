from PIL import Image
from src.functions.grayScale import grayScale
def yellowsepia(img, quantity):
    im = grayScale(img)
    pixels = im.load()

    def helper(i, j):
        red = pixels[i, j][0]
        green = pixels[i, j][1]
        blue = pixels[i, j][2]

        if red + quantity > 255:
            red = 255
        else:
            red += quantity
        if green + quantity > 255:
            green = 255
        else:
            green += quantity

        return red, green, blue

    for i in range(im.size[0]):  # for every pixel:
        for j in range(im.size[1]):
            pixels[i, j] = helper(i, j)
    return im



def blueSepia(img, quantity):
    im = grayScale(img)
    pixels = im.load()

    def helper(i, j):
        red = pixels[i, j][0]
        green = pixels[i, j][1]
        blue = pixels[i, j][2]

        if blue + quantity > 255:
            blue = 255
        else:
            blue += quantity
        if green + quantity > 255:
            green = 255
        else:
            green += quantity

        return red, green, blue

    for i in range(im.size[0]):  # for every pixel:
        for j in range(im.size[1]):
            pixels[i, j] = helper(i, j)
    return im



def MixedSepia(img):
    im = Image.open(img)
    imgcopy = Image.open(img)
    pixels2 = imgcopy.load()
    pixels = im.load()

    def helper2(colors):
        colors[0] = int((0.393 * colors[0]) + (0.769 * colors[1]) + (0.189 * colors[2]))
        colors[1] = int((0.349 * colors[0]) + (0.686 * colors[1]) + (0.168 * colors[2]))
        colors[2] = int((0.272 * colors[0]) + (0.534 * colors[1]) + (0.131 * colors[2]))
        return colors[0], colors[1], colors[2]

    def helper(i, j):
        red = pixels[i, j][0]
        green = pixels[i, j][1]
        blue = pixels[i, j][2]
        return helper2([red, green, blue])

    for i in range(im.size[0]):  # for every pixel:
        for j in range(im.size[1]):
            pixels2[i, j] = helper(i, j)

    return imgcopy
