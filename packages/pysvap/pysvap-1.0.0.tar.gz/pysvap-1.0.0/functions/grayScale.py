from PIL import Image

def grayScale(img):
    im = Image.open(img)
    imgcopy = Image.open(img)
    pixels2 = imgcopy.load()
    pixels = im.load()

    def helper(i, j):
        red = pixels[i, j][0]
        green = pixels[i, j][1]
        blue = pixels[i, j][2]
        grey = int((red * 0.299) + (green * 0.587) + (blue * 0.114))
        return grey, grey, grey

    for i in range(im.size[0]):  # for every pixel:
        for j in range(im.size[1]):
            pixels2[i, j] = helper(i, j)

    return imgcopy