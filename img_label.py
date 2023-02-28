'''
Author: Andrey Stroganov (savthe@gmail.com)

No rights reserved. This script is available for public domain. Have fun with it!
'''

#!/bin/env python3

import argparse 
import warnings

from PIL import Image, ImageFilter, ImageDraw, ImageFont

warnings.simplefilter(action='ignore', category=DeprecationWarning)

HEIGHT_PERCENT = 7 # Percent of image height
LABEL_HEIGHT_PERCENT = 80 # Percent of box height
BLUR_RADIUS = 2
BOX_FILL_COLOR = (0, 0, 0, 100)

def get_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('image_name', type=str, help='Original image name')
    parser.add_argument('output_name', type=str, help='Output image name')
    parser.add_argument('label', type=str, help='Label')
    parser.add_argument('font', type=str, help='Font file name')

    return parser.parse_args()

def select_font(label, font_name, height):
    font_size = 1
    font = ImageFont.truetype(font_name, size=font_size, encoding='UTF-8')
    while font.getsize(label)[1] < height: 
        font_size += 1
        font = ImageFont.truetype(font_name, size=font_size, encoding='UTF-8')

    return font

args = get_args()

img = Image.open(args.image_name)
width, height = img.size

# Making bottom box.
box_height = height * HEIGHT_PERCENT // 100;
box_y = height - box_height
box = (0, box_y, width, height)

orig_box = img.crop(box)
blurred_box = orig_box.filter(ImageFilter.GaussianBlur(radius=BLUR_RADIUS))
draw = ImageDraw.Draw(blurred_box, 'RGBA')
draw.rectangle(((0, 0), (width, box_height)), fill=BOX_FILL_COLOR)

# Making label.
font = select_font(args.label, args.font, box_height * LABEL_HEIGHT_PERCENT // 100)
label_width, label_height = font.getsize(args.label)
label_top = (box_height - label_height) // 2
label_left = width // 2 - label_width // 2
draw.text((label_left, label_top), args.label, font=font )

# Finilizing the image.
img.paste(blurred_box, box)
img.save(args.output_name)
