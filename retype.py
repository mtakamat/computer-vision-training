#このプログラムの目的
#目的1．tifファイルをjpgファイルにする
#目的2．pngファイルをjpgファイルにする
import os
import glob

path1='../*.tif'
path2='../*.tif'
path3='../*.jpg'
#pngファイルを取得
flist=glob.glob(path3)
i=1
#ファイル名を一括変換
for file in flist:
    os.rename(file, str(i) + '.jpg')
    i+=1

list=glob.glob(path3)
