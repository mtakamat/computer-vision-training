import os
import glob

path='./*.png'

#pngファイルを取得
flist=glob.glob(path)
i=866
#ファイル名を一括変換
for file in flist:
    os.rename(file, './'+ str(i) + '.png')
    i+=1

list=glob.glob(path)
