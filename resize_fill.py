#!/usr/bin/env python3
import cv2
import numpy as np

import argparse
import os
import os.path as osp

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-d', '--dir', help='Image file directory')
    parser.add_argument('-b', '--blank', help='Blank pixels to insert')

    args = parser.parse_args()
    imdir = args.dir
    blank = int(args.blank)

    files = os.listdir(imdir)
    savedir = osp.join(imdir, 'resized')
    if not osp.exists(savedir):
        os.mkdir(savedir)

    for file in files:
        _, ext = osp.splitext(file)
        if ext != '.png':
            continue
        impath = osp.join(imdir, file)
        print('Open ' + impath)
        img = cv2.imread(impath, cv2.IMREAD_UNCHANGED)
        h, w = img.shape[:2]
        if h <= w:
            hr = h - blank * 2  # resized length
            factor = hr / float(h)
            wr = int(w * factor)  # got larger blank than h
        else:
            wr = w - blank * 2
            factor = wr / float(w)
            hr = int(h * factor)

        rimg = cv2.resize(img, (wr, hr))  # resized image
        oimg = np.zeros((h, w, 4), np.uint8)  # output image, including alpha channel
        oimg[:, :, 3] = 0
        hm = (h - hr) // 2  # margin
        wm = (w - wr) // 2  # margin

        oimg[hm:hm + hr, wm:wm + wr, :] = rimg

        savepath = osp.join(savedir, file)
        print('Save ' + savepath)
        cv2.imwrite(savepath, oimg)
