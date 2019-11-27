import cv2
import numpy as np
import os
import glob
import sys
import csv
import re
from numpy.lib.arraypad import _validate_lengths
#import numpy as np
#import matplotlib.pyplot as plt
#img1='../task/PONBAFRC8'
#img2='../task/PONBAFRC8_to_PONBAFRC9_V2_AllUR'
#img3='../task/PONBAFRC9_V2'

#path1 = sorted(glob.glob(os.path.join(img1, '*')))
#path2 = sorted(glob.glob(os.path.join(img2, '*')))
#path3 = sorted(glob.glob(os.path.join(img3, '*')))
def common_use(path1,path2):
    # 両方のディレクトリに存在する要素を決定する
    entries_in_path1 = set(os.listdir(path1))
    entries_in_path2 = set(os.listdir(path2))

    common_names = list(entries_in_path1 & entries_in_path2)

    common_files = [ f
                for f in common_names
                if os.path.isfile(os.path.join(path1, f))
                and os.path.isfile(os.path.join(path2, f))
                and re.search(r"\.(png$)",f)
                ]
    return common_files


def abs_diff(path1,path2,output):
    if output:
        os.makedirs(output, exist_ok=True)

    common_files=common_use(path1,path2)

    for file_name in common_files:
        img1=cv2.imread(os.path.join(path1, file_name),1)
        img2=cv2.imread(os.path.join(path2, file_name),1)
        img=cv2.absdiff(img1,img2)
        output_path = file_name
        if output:
            output_path = os.path.join(output, output_path)
        cv2.imwrite(output_path,img)

def normalize(x,min=-1,max=1):
    xmax=x.max()
    xmin=x.min()
    if xmin==xmax:
        return np.ones_like(x)
    return (xmax-xmin)*(x-xmin)/(xmax-xmin)+xmin

def crop(ar, crop_width, copy=False, order='K'):
    '''Crop numpy array at the borders by crop_width.
    Source: www.github.com/scikit-image.'''

    ar = np.array(ar, copy=False)
    crops = _validate_lengths(ar, crop_width)
    slices = [slice(a, ar.shape[i] - b) for i, (a, b) in enumerate(crops)]

    if copy:
        cropped = np.array(ar[slices], order=order, copy=True)
    else:
        cropped = ar[slices]
    return cropped

def compute_ssim(img1,img2,win_size=11,L=255,K1=0.01,K2=0.03):
    #img1: SSIMを計算する画像
    #img2: 参照画像
    #K1,K2: 補正項
    C1=(K1*L)**2
    C2=(K2*L)**2

    #compute weighted means
    ux=np.mean(img1, axis=(0, 1))
    uy=np.mean(img2, axis=(0, 1))

    #compute variances
    uxx=np.var(img1*img1, axis=(0, 1))
    uyy=np.var(img2*img2, axis=(0, 1))
    uxy=np.cov(img1,img2)

    #compute covariances
    vx=uxx-ux*ux
    vy=uyy-uy*uy
    vxy=uxy-ux*uy

    #compute SSIM
    ssim=((2*ux*uy+C1)*(2*vxy+C2))/((ux**2+uy**2+C1)*(vx+vy+C2))
    mssim=ssim.mean()

    pad=(win_size-1)//2
    mssim=crop(ssim,pad).mean()
    mssim=normalize(mssim,min=-1,max=1)
    #print(mssim)
    return mssim


def know_ssim(path1,path2,output):
    common_files=common_use(path1,path2)
    f = open(output, 'w', newline='') if output else sys.stdout
    csvw = csv.writer(f)

    for file_name in common_files:
        img1=cv2.imread(os.path.join(path1, file_name),0)
        img2=cv2.imread(os.path.join(path2, file_name),0)
        #To do:SSIMをnumpyで表現する
        ssim=compute_ssim(img1,img2)
        #ssim=compare_ssim(img1,img2)
        csvw.writerow([os.path.basename(file_name), ssim])

    if output:
        f.close()

def know_under_3S(path1,path2,output):
    common_files=common_use(path1,path2)
    g = open(output, 'w', newline='') if output else sys.stdout
    csvw = csv.writer(g)

    for file_name in common_files:
        img1=cv2.imread(os.path.join(path1, file_name),0)
        img2=cv2.imread(os.path.join(path2, file_name),0)
        ssim=compute_ssim(img1,img2)
        #SSIM値が0.95以下のものをリストアップ
        if  ssim < 0.95:
            csvw.writerow([os.path.basename(file_name), ssim])
    if output:
        g.close()

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
