#!/bin/python2
# Pixel sorts in an interesting way: looks at all pixels with R, G, and B values
# above specified thresholds, and sorts them across the entire image.

# You can imagine it pulls them into a separate list, sorts them, then inserts
# elements (in order) from the list into the spots from which the pixels came.


import os
import sys

from PIL import Image

import config


def main():
    if len(sys.argv) is not 5:
        usage()

    fnamepath = sys.argv[1]
    fname = os.path.split(fnamepath)[1]
    try:
        r = int(sys.argv[2])
        g = int(sys.argv[3])
        b = int(sys.argv[4])
    except:
        usage()

    try:
        im = Image.open(fnamepath)
    except:
        print "Could not find image"
        sys.exit(3)

    if im.getbands() != ("R", "G", "B"):
        rgb_complaint()

    rmax, gmax, bmax = im.getextrema()
    newim = sort_range(im, (r, rmax[1]), (g, gmax[1]), (b, bmax[1]))

    newim.save(config.save_loc + fname)


def sort_range(im, rrange, grange, brange):
    """
    Sort pixels of an image which fall into the specified R, G, B ranges.
    First arg should be a PIL Image object, ranges should be twoples.

    Returns the new Image object.
    """
    if im.getbands() != ("R", "G", "B"):
        rgb_complaint()

    locs = []
    pix_to_sort = []
    pix = list(im.getdata())

    for i, p in enumerate(pix):
        r, g, b = p
        if rrange[0] <= r and r < rrange[1] and \
            grange[0] <= g and g < grange[1] and \
            brange[0] <= b and b < brange[1]:

            locs.append(i)
            pix_to_sort.append(p)

    pix_to_sort.sort(key=lambda p: p[0]*(256**2) + p[1]*256 + p[2])

    for np in zip(pix_to_sort, locs):
        pix[np[1]] = np[0]

    im2 = Image.new(im.mode, im.size)
    im2.putdata(pix)

    return im2


def usage():
    print "Put the shit in the shit, you shit"
    sys.exit(1)


def rgb_complaint():
    print "File must be RGB"
    sys.exit(2)


if __name__ == "__main__":
    main()
