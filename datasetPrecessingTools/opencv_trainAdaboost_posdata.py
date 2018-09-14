import os
import cv2
import argparse
import numpy as np

parser = argparse.ArgumentParser()
parser.add_argument("-folder",type=str,dest="folder")
parser.add_argument("--append",type=bool,default=False,dest="appendFlag")
args = parser.parse_args()
#print(args.folder)
#dir = os.getcwd()
#path = os.path.join(dir,args.folder)
path = args.folder
files = os.listdir(path)

description = ""
for item in files:
    print(item)
    sp = cv2.imread(os.path.join(path,item)).shape
    description += os.path.join(os.path.basename(path),item)+ " 1 0 0 "+str(sp[0])+" "+str(sp[1])+"\n"

if args.appendFlag:
    print(args.appendFlag == True)
    file = open(os.path.join(os.path.dirname(path), 'posdata.txt'), 'a')
else:
    print(args.appendFlag == True)
    file = open(os.path.join(os.path.dirname(path), 'posdata.txt'), 'w')
file.write(description)
file.close()