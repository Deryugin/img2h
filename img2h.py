#!/usr/bin/python3
from PIL import Image

import random
import argparse
import os
import sys

format_rgb888 = [0, 0, 0,  0, 8, 16]
format_rgb565 = [3, 2, 3,  0, 5, 11]
format_bgr565 = [3, 2, 3, 11, 5,  0]

def main():
    parser = argparse.ArgumentParser(description='Convert image to C-style header')
    parser.add_argument('-i','--input', help='Input file name', required=True)
    parser.add_argument('-f','--format', default="RGB888", required=False)
    parser.add_argument('-n','--name', default="image", required=False)

    args = vars(parser.parse_args())

    im = Image.open(args["input"]) # Can be many different formats.
    pix = im.load()

    print("uint16_t " + args["name"] + "[] = {")

    fmt = []
    if args["format"] == "RGB888":
        fmt = format_rgb888
    elif args["format"] == "RGB565":
        fmt = format_rgb565
    elif args["format"] == "BGR565":
        fmt = format_bgr565

    sys.stdout.write('\t')
    for y in range(im.size[1]):
        for x in range(im.size[0]):
            if x % 16 == 0 and x != 0:
                print("")
                sys.stdout.write('\t')

            r = pix[x,y][0]
            g = pix[x,y][1]
            b = pix[x,y][2]

            r = r >> fmt[0]
            g = g >> fmt[1]
            b = b >> fmt[2]

            val = (r << fmt[3]) | (g << fmt[4]) | (b << fmt[5])

            sys.stdout.write(hex(val) + ", ")

        print("")
        sys.stdout.write('\t')

    print("};")

    pix[x,y] = (255, 255, 255)  # Set the RGBA Value of the image (tuple)
    im.save('arch2.png')  # Save the modified pixels as .png

if __name__ == '__main__':
    main()