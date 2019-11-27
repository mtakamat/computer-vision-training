import cv2
import numpy as np
import os
import glob
import sys
import csv
from skimage.measure import compare_ssim
#import numpy as np
#import matplotlib.pyplot as plt
#img1='../task/PONBAFRC8'
#img2='../task/PONBAFRC8_to_PONBAFRC9_V2_AllUR'
#img3='../task/PONBAFRC9_V2'

#path1 = sorted(glob.glob(os.path.join(img1, '*')))
#path2 = sorted(glob.glob(os.path.join(img2, '*')))
#path3 = sorted(glob.glob(os.path.join(img3, '*')))

def abs_diff(path1,path2,output):
    path1 = sorted(glob.glob(os.path.join(path1, '*')), reverse=True)
    path2 = sorted(glob.glob(os.path.join(path2, '*')), reverse=True)

    if output:
        os.makedirs(output, exist_ok=True)

    for path_1, path_2 in zip(path1, path2):
        img1 = cv2.imread(path_1,1)
        img2 = cv2.imread(path_2,1)
        img=cv2.absdiff(img1,img2)
        basename = os.path.basename(path_1)
        if output:
            basename = os.path.join(output, basename)
        cv2.imwrite(basename,img)

def know_ssim(path1,path2,output):
    path1 = sorted(glob.glob(os.path.join(path1, '*')), reverse=True)
    path2 = sorted(glob.glob(os.path.join(path2, '*')), reverse=True)

    f = open(output, 'w', newline='') if output else sys.stdout
    csvw = csv.writer(f)

    for path_1, path_2 in zip(path1, path2):
        img1 = cv2.imread(path_1,0)
        img2 = cv2.imread(path_2,0)
        ssim=compare_ssim(img1,img2)
        csvw.writerow([os.path.basename(path_1), ssim])

    if output:
        f.close()

def know_under_3S(path1,path2,output):
    path1 = sorted(glob.glob(os.path.join(path1, '*')), reverse=True)
    path2 = sorted(glob.glob(os.path.join(path2, '*')), reverse=True)

    f = open(output, 'w', newline='') if output else sys.stdout
    csvw = csv.writer(f)

    for path_1, path_2 in zip(path1, path2):
        img1 = cv2.imread(path_1,0)
        img2 = cv2.imread(path_2,0)
        ssim=compare_ssim(img1,img2)
        #SSIM値が0.95以下のものをリストアップ
        if  ssim < 0.95:
            csvw.writerow([os.path.basename(path_1), ssim])

    if output:
        f.close()

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("path1", help="テストデータ1のディレクトリ")
    parser.add_argument("path2", help="テストデータ2のディレクトリ")
    parser.add_argument("-o", "--output", help="出力CSVファイル/ディレクトリ")

    command_name = sys.argv[1] if len(sys.argv) >= 2 else None
    command_action = None
    if command_name == "abs_diff":
        command_action = abs_diff
    elif command_name == "know_ssim":
        command_action = know_ssim
    elif command_name == "know_under_3S":
        command_action = know_under_3S

    if not command_action:
        parser.print_help()
    else:
        args = parser.parse_args(sys.argv[2:])
        command_action(args.path1, args.path2, args.output)
