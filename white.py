import cv2
import numpy as np

width = 256
height = 256

# uint8で0埋めの配列を作る。
# 幅16、高さ24のサイズ
# zeros(shape, type) shapeは配列の大きさ
# 配列の（行数、列数）になっている
# 画像はwidth,heightの慣習があるが、ココは逆なので気をつけること
imageArray = np.zeros((height, width, 3), np.uint8)
imageArray+=255
# これでサイズを確認できます

size = imageArray.shape[:2]
print(size)


# 0で埋められた配列を画像として保存します
cv2.imwrite("white.png", imageArray);
