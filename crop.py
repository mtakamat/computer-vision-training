import cv2
import numpy as np
import glob
import os

def crop(img_path,outout_path):
    img_path = glob.glob(os.path.join(img_path, '*'))

    for path in img_path:
        img = cv2.imread(path,1)
        h = [118,53,638,460]
        x = h[0]
        y = h[1]
        width = h[2]
        height = h[3]
        img = img[y:y + height, x:x + width]
        basename = os.path.basename(path)
        cv2.imwrite(basename,img)


if __name__=='__main__':
    img_path='.'
    crop(img_path,'./')
