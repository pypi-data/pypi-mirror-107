from PIL import Image

dic = {
    "red":1,
    "green":2,
    "blue":3,
    "yellow":4,
    "orange":5,
    "violet":6
}

def overLay(img,value,intensity):
    num = 0
    if value in dic.keys():
        num = dic[value]
    else:
        raise Exception("FATAL! Sorry, no such overlay color exists!!")

    im = Image.open(img)
    pixels = im.load()

    def helper2(colors):
        if num==1:
            colors[0] += intensity
            if colors[0]>=255:
                colors[0]=255
        elif num==2:
            colors[1] += intensity
            if colors[1]>255:
                colors[1]=255
        elif num==3:
            colors[2] += intensity
            if colors[2]>255:
                colors[2]=255
        elif num==4:
            colors[0] += intensity
            if colors[0]>255:
                colors[0]=255
            colors[1] += intensity
            if colors[1] > 255:
                colors[1] = 255
        elif num==5:
            colors[0] += intensity
            if colors[0]>255:
                colors[0]=255
            colors[1] += int(intensity/2)
            if colors[1] > 255:
                colors[1] = 255
        elif num==6:
            colors[0] += intensity
            if colors[0]>255:
                colors[0]=255
            colors[2] += intensity
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