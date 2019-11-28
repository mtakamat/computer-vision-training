import cv2
import numpy as np
import os
import glob
import sys
import csv
import re
from numpy.lib.arraypad import _validate_lengths

def common_use(path1,path2):
    # 両方のディレクトリに存在する要素を決定する
    entries_in_path1 = set(os.listdir(path1))
    entries_in_path2 = set(os.listdir(path2))

    common_names = list(entries_in_path1 & entries_in_path2)

    common_files = [ f
                for f in common_names
                if os.path.isfile(os.path.join(path1, f))
                and os.path.isfile(os.path.join(path2, f))
                and re.search(r"\.(jpg$)",f)
                ]
    return common_files


def get_BoundingBox(path1,path2,output):
    if output:
        os.makedirs(output, exist_ok=True)

    common_files=common_use(path1,path2)
    for file_name in common_files:
        img1=cv2.imread(os.path.join(path1, file_name),1)
        img2=cv2.imread(os.path.join(path2, file_name),1)
        #2値化
        img1 = cv2.cvtColor(img1, cv2.COLOR_RGB2GRAY)
        #しきい値処理(大津の方法)
        retval, img_bw = cv2.threshold(img1, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)
        #エッジ検出
        edges= cv2.Canny(img_bw,100,200)
        #ターゲットのエッジ部位を特定する
        #top, bottom, left, right(コーナー情報を取得)
        results = np.where(edges==255)
        top = np.min(results[0])
        bottom = np.max(results[0]) - 1
        left = np.min(results[1])
        right = np.max(results[1]) - 1
        #バウンディングボックスを取得
        img =cv2.rectangle(img2, (left, top),(right, bottom), (0, 255, 0), cv2.LINE_4)
        output_path = file_name
        if output:
            output_path = os.path.join(output, output_path)
        cv2.imwrite(output_path,img)

"""
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
"""

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("path1", help="テストデータ1のディレクトリ")
    parser.add_argument("path2", help="テストデータ2のディレクトリ")
    parser.add_argument("-o", "--output", help="出力CSVファイル/ディレクトリ")

    command_name = sys.argv[1] if len(sys.argv) >= 2 else None
    command_action = None
    if command_name == "get_BoundingBox":
        command_action = get_BoundingBox
    elif command_name == "know_ssim":
    #    command_action = know_ssim
    #elif command_name == "know_under_3S":
    #    command_action = know_under_3S

    if not command_action:
        parser.print_help()
    else:
        args = parser.parse_args(sys.argv[2:])
        command_action(args.path1, args.path2, args.output)
