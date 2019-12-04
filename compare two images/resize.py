import os
import glob
import cv2
import numpy as np

file1='../data'
files = glob.glob(os.path.join(file1, '*.jpg'))
print(files)
#files = glob.glob('./data/*.jpg')
output='../data'
size=(384,384)
for f in files:
    img = cv2.imread(f)
    img_resize = cv2.resize(img,size)
    output_path=f
    if output:
        output_path = os.path.join(output, output_path)
        cv2.imwrite(output_path,img_resize)
