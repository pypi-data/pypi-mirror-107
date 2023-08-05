from PIL import Image
def temperature(img, tempVal):
    im = Image.open(img)
    pixels = im.load()

    def helper2(colors):
        if tempVal > 0:
            colors[0] += tempVal
            if colors[0] > 255:
                colors[0] = 255
            colors[1] += int(tempVal/2)
            if colors[1] > 255:
                colors[1] = 255
        elif tempVal < 0:
            colors[2] -= tempVal
            if colors[2] > 255:
                colors[2] = 255
        return colors[0],colors[1],colors[2]

    def helper(i, j):
        red = pixels[i, j][0]
        green = pixels[i, j][1]
        blue = pixels[i, j][2]
        return helper2([red, green, blue])

    for i in range(im.size[0]):  # for every pixel:
        for j in range(im.size[1]):
            pixels[i, j] = helper(i, j)
    return im