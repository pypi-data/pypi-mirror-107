from PIL import Image
from src.functions.blur import gaussianBlur
from src.functions.negative import negative
from src.functions.grayScale import grayScale
from src.functions.saturate import saturation
from src.functions.posterize import posterize
from src.functions.lighten import lighten
from src.functions.darken import darken
from src.functions.pixelate import pixelate
from src.functions.sepia import yellowsepia
from src.functions.sepia import blueSepia
from src.functions.sepia import MixedSepia
from src.functions.temp import temperature


Blur = gaussianBlur
neg = negative
gray = grayScale
sat = saturation
post = posterize
lightn = lighten
darkn = darken
pixel8 = pixelate
ysepia = yellowsepia
bsepia = blueSepia
msepia = MixedSepia
temp = temperature









