import os
from PIL import Image
from __future__ import print_function

files = os.listdir('.')
for file_name in files:
    im = Image.open(file_name)
    print(im.format, im.size, im.mode)
    im2 = im.resize([256, 256], Image.BILINEAR)
    gim = im2.convert("L")
    filename, file_extension = os.path.splitext(file_name)
    gim.save(filename + '.png')