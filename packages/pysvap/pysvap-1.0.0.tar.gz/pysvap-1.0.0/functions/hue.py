from PIL import Image
import math

def rgb_to_hsv(r, g, b):
    r = float(r)
    g = float(g)
    b = float(b)
    high = max(r, g, b)
    low = min(r, g, b)
    h, s, v = high, high, high

    d = high - low
    s = 0 if high == 0 else d / high

    if high == low:
        h = 0.0
    else:
        h = {
            r: (g - b) / d + (6 if g < b else 0),
            g: (b - r) / d + 2,
            b: (r - g) / d + 4,
        }[high]
        h /= 6

    return h, s, v


def hsv_to_rgb(h, s, v):
    i = math.floor(h * 6)
    f = h * 6 - i
    p = v * (1 - s)
    q = v * (1 - f * s)
    t = v * (1 - (1 - f) * s)

    r, g, b = [
        (v, t, p),
        (q, v, p),
        (p, v, t),
        (p, q, v),
        (t, p, v),
        (v, p, q),
    ][int(i % 6)]

    return r, g, b


def hue(img, hue):
    im = Image.open(img)
    imgcopy = Image.open(img)
    pixels2 = imgcopy.load()
    pixels = im.load()

    def helper2(colors):
        hsv = rgb_to_hsv(colors[0], colors[1], colors[2])
        ans = hsv_to_rgb(hsv[0]*(hue), hsv[1] , hsv[2])
        return int(ans[0]), int(ans[1]), int(ans[2])
        # dontMax = 0
        #         # dontMin = 300
        #         # for i in range(0, len(colors)):
        #         #     if colors[i] > dontMax:
        #         #         dontMax = colors[i]
        #         #     if colors[i] < dontMin:
        #         #         dontMin = colors[i]
        #         #
        #         # if saturation > 0:
        #         #     for i in range(0, len(colors)):
        #         #         if colors[i] == dontMax:
        #         #             if colors[i] + saturation > 255:
        #         #                 colors[i] = 255
        #         #             else:
        #         #                 colors[i] += int(saturation)
        #         #         else:
        #         #             colors[i] = colors[i] - int(saturation)
        #         #             if colors[i] < 0:
        #         #                 colors[i] = 0
        # elif saturation < 0:
        #
        #     ave = int(math.fsum(colors) / 3)
        #     difference = 300
        #     averageVala = colors[0]
        #     for itera in range(0, len(colors)):
        #         if int(math.fabs(colors[itera] - ave)) < difference:
        #             difference = int(math.fabs(colors[itera] - ave))
        #             averageVala = colors[itera]
        #
        #     for i in range(0, len(colors)):
        #         if dontMin == colors[i]:
        #             if colors[i] - saturation >= averageVala:
        #                 colors[i] = averageVala
        #             else:
        #                 colors[i] -= saturation
        #         elif dontMax == colors[i]:
        #             if colors[i] - math.fabs(saturation) <= averageVala:
        #                 colors[i] = averageVala
        #             else:
        #                 colors[i] -= int(math.fabs(saturation))
        #
        # return colors[0], colors[1], colors[2]

    def helper(i, j):
        red = pixels[i, j][0]
        green = pixels[i, j][1]
        blue = pixels[i, j][2]
        return helper2([red, green, blue])

    for i in range(im.size[0]):  # for every pixel:
        for j in range(im.size[1]):
            pixels[i, j] = helper(i, j)

    return im

