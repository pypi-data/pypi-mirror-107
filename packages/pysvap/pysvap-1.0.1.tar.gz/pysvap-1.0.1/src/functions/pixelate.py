from PIL import Image
def pixelate(img, radius):
    im = Image.open(img)
    imgcopy = Image.open(img)
    pixels2 = imgcopy.load()
    pixels = im.load()

    def checker(i, j):
        if (i < 0 or i >= im.size[0]) or (j < 0 or j >= im.size[1]):
            return False
        return True

    for i in range(0, im.size[0] - radius, 2 * radius):  # for every pixel:
        for j in range(0, im.size[1] - radius, 2 * radius):
            for t in range(i - radius, i + radius):
                for k in range(j - radius, j + radius):
                    if checker(i, j):
                        pixels2[t, k] = pixels[i, j]

    return imgcopy