from PIL import Image

def gaussianBlur(img, radius):
    im = Image.open(img)
    imgcopy = Image.open(img)
    pixels2 = imgcopy.load()
    pixels = im.load()

    def checker(i, j):
        if (i < 0 or i >= im.size[0]) or (j < 0 or j >= im.size[1]):
            return False
        return True

    def average(xIndex, yIndex):
        # global radius
        red = 0
        blue = 0
        green = 0
        count = 0
        for i in range(xIndex - radius, xIndex + radius):
            for j in range(yIndex - radius, yIndex + radius):
                if checker(i, j):
                    red += pixels[i, j][0]
                    green += pixels[i, j][1]
                    blue += pixels[i, j][2]
                    count += 1
        red = int(red / count)
        green = int(green / count)
        blue = int(blue / count)
        return red, green, blue

    for i in range(im.size[0]):  # for every pixel:
        for j in range(im.size[1]):
            pixels2[i, j] = average(i, j);

    return imgcopy