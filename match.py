import cv2
import numpy as np
import matplotlib.pyplot as plt
#%matplotlib inline

hacker = cv2.imread('./TCIA_pancreas_labels⁩/⁨label0011⁩/000011-101.jpg',0)
items = cv2.imread('./Pancreas-CT⁩/PANCREAS_0011/⁩000011-101.jpg',0)

sift = cv2.xfeatures2d.SIFT_create()

kp1, des1 = sift.detectAndCompute(hacker,None)
kp2, des2 = sift.detectAndCompute(items,None)

bf = cv2.BFMatcher()
matches = bf.knnMatch(des1,des2, k=2)

good = []
for match1,match2 in matches:
    if match1.distance < 0.75*match2.distance:
        good.append([match1])

sift_matches = cv2.drawMatchesKnn(hacker,kp1,items,kp2,good,None,flags=2)

display(sift_matches)
