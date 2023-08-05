from PIL import Image
def negative(img):
    im = Image.open(img)
    imgcopy = Image.open(img)
    pixels2 = imgcopy.load()
    pixels = im.load()

    def helper(i, j):
        red = 255 - pixels[i, j][0]
        green = 255 - pixels[i, j][1]
        blue = 255 - pixels[i, j][2]
        return red, green, blue

    for i in range(im.size[0]):  # for every pixel:
        for j in range(im.size[1]):
            pixels2[i, j] = helper(i, j)

    return imgcopy