from PIL import Image

def lighten(img, lighten):
    im = Image.open(img)
    pixels = im.load()

    def helper2(colors):
        for i in range(0, len(colors)):
            if colors[i] + lighten > 255:
                colors[i] = 255
            else:
                colors[i] += lighten
        return colors[0], colors[1], colors[2]

    def helper(i, j):
        red = pixels[i, j][0]
        green = pixels[i, j][1]
        blue = pixels[i, j][2]
        return helper2([red, green, blue])

    for i in range(im.size[0]):  # for every pixel:
        for j in range(im.size[1]):
            pixels[i, j] = helper(i, j)
    return im