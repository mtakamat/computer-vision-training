import os
import glob
import numpy as np
import cv2

from_dir = './Pancreas-CT/PANCREAS_0056'
to_dir = './high_pass_56/'

#os.makedirs(to_dir, exist_ok=True)
for path in glob.glob(os.path.join(from_dir, '*')):
    img=cv2.imread(path,1)
    # グレースケール変換
    gray = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)

    dst = cv2.Laplacian(gray, cv2.CV_32F, ksize=3)
    output_path = path

    output_path = (os.path.join(to_dir, output_path))

    cv2.imwrite(output_path,dst)
