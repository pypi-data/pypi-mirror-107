from PIL import Image
def colorShift(img,num):
    im = Image.open(img)
    pixels = im.load()

    def helper2(colors):
        if num == 1:
            temp = colors[0]
            colors[0]=colors[1]
            colors[1] = colors[2]
            colors[2]=temp
        elif num == 2:
            temp = colors[0]
            colors[0] = colors[2]
            colors[2] = colors[1]
            colors[1] = temp
        elif num == 3:
            temp = colors[1]
            colors[1] = colors[2]
            colors[2] = colors[0]
            colors[0] = temp
        elif num==4:
            temp = colors[1]
            colors[1] = colors[0]
            colors[2] = colors[1]
            colors[0] = temp
        elif num == 5:
            temp = colors[2]
            colors[2] = colors[1]
            colors[1] = colors[0]
            colors[0] = temp

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