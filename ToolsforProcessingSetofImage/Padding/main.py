srcPath = "/media/ryan/E/DataSets/carsDataSet"
dstfolder = "padding"

import os
import cv2
import numpy as np
dstPath = os.path.join(srcPath,dstfolder)
if not os.path.exists(dstPath):
    os.mkdir(dstPath)

files = []
for root, dirs,fs in os.walk(srcPath):
    for file in fs:
        img = cv2.imread(os.path.join(root,file),0)
        if img.shape[0] != img.shape[1]:
            diff = img.shape[0]-img.shape[1]
            if diff > 0:
                img = cv2.copyMakeBorder(img,0,0,int(diff/2),diff-int(diff/2),cv2.BORDER_CONSTANT,value=[127,127,127])
            elif diff < 0:
                img = cv2.copyMakeBorder(img,int(-diff/2),-diff-int(-diff/2),0,0,cv2.BORDER_CONSTANT,value=[127,127,127])
        cv2.imwrite(os.path.join(dstPath,file),img)
