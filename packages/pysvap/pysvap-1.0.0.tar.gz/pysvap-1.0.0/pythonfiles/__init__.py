from PIL import Image
import math

from functions.blur import gaussianBlur
from functions.negative import negative
from functions.grayScale import grayScale
from functions.saturate import saturation
from functions.posterize import posterize
from functions.lighten import lighten
from functions.darken import darken
from functions.pixelate import pixelate
from functions.sepia import yellowsepia
from functions.sepia import blueSepia
from functions.sepia import MixedSepia
from functions.temp import temp
from functions.colorShift import colorShift
# from functions.hue import hue
from functions.overlay import overLay

Image.open("./sampleImages/cool.jpeg").show()
overLay("./sampleImages/cool.jpeg","orange",100).show()










