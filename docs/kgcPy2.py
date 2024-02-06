'''Accelerated version of the functions in the kgcPy package.'''
from PIL import Image
Image.MAX_IMAGE_PIXELS = None

import pandas as pd
from importlib import resources

with resources.open_binary('kgcPy', 'kmz_int_reshape.png') as fp:
    kg_img = Image.open(fp)
    kg_img.load()

with resources.open_binary('kgcPy', 'kg_zoneNum.csv') as fp:
    kg_df = pd.read_csv(fp)

def lookupCZ(lat, lon):
    x = round((lon+180)*(kg_img.size[0])/360 - 0.5)
    y = round(-(lat-90)*(kg_img.size[1])/180 - 0.5)
    num = kg_img.getpixel((x, y))
    res = kg_df['kg_zone'].loc[kg_df['zoneNum'] == num]
    return res.values[0]
