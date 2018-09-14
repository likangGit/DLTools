#!/usr/bin/python3.5
import cv2
import numpy as np
import os
import argparse
import re
import random
from xml.dom.minidom import Document


def CheckArg(value):
    backgroundPath = Check_Image(value.backgroundImage)
    foregroundPath = Check_Image(value.foregroundImage)
    outputPath = Check_Path(value.outputPath)
    r = Check_R_S(value.r)
    s = Check_R_S(value.s)
    n = Check_N(value.n)
    return backgroundPath, foregroundPath, outputPath, r, s, n


def Check_Image(value):
    if not os.path.exists(value):
        print('%s does\'t exist' % value)
        exit(1)
    return value



def Check_R_S(value):
    search_obj = re.match(r'(\d+\.?\d*):(\d+\.?\d*)(?::(\d+\.?\d*))?$', value)
    if search_obj:
        temp = list(search_obj.groups())
        if temp[2] == None:  # 说明是start:stop,未指定step，设置默认值step=1
            temp[2] = 1
        temp = list(map(float, temp))
        return temp
    else:
        parser.print_help()
        exit(1)


def Check_N(value):
    search_obj = re.match(r'\d+', value)
    if not search_obj:
        parser.print_help()
        exit(1)
    return int(value)


def Check_Path(value):
    if not os.path.isdir(value):
        print('Error: %s is not a directory' % value)
        parser.print_help()
        exit(1)
    return value


def ListGenerator(value, default=0):
    if value[0] >= value[1]:
        temp = [default, ]
    else:
        temp = np.arange(value[0], value[1], value[2])
    return temp

def InsertNode(doc, parent, subNodeName, text=None):
    subNode = doc.createElement(subNodeName)
    if text is not None:
        subNode.appendChild(doc.createTextNode(text))
    parent.appendChild(subNode)
    return subNode

def WriteXml(backgroundImage, path, label, i, x, y, w, h):
    dir = os.path.dirname(os.path.join(os.path.abspath(path),".."))
    folder = os.path.basename(dir)
    filename = str(i)+'.jpg'
    filepath = 'imgs/'+filename
    heigh, width, depth = backgroundImage.shape
    name = label
    xmin = x
    xmax = xmin + w
    ymin = y
    ymax = ymin + h

    doc = Document()
    storage = doc.createElement('opencv_storage')
    doc.appendChild(storage)

    InsertNode(doc,storage,'folder',folder)
    InsertNode(doc,storage,'filename',filename)
    InsertNode(doc,storage,'path',filepath)

    sizeNode = InsertNode(doc,storage,'size')
    InsertNode(doc,sizeNode,'width',str(width))
    InsertNode(doc,sizeNode,'heigh',str(heigh))
    InsertNode(doc,sizeNode,'depth',str(depth))

    objectNode = InsertNode(doc,storage,'objects')
    InsertNode(doc,objectNode,'name',name)
    bndboxNode = InsertNode(doc,objectNode,'bndbox')
    InsertNode(doc,bndboxNode,'xmin',str(xmin))
    InsertNode(doc,bndboxNode,'xmax',str(xmax))
    InsertNode(doc,bndboxNode,'ymin',str(ymin))
    InsertNode(doc,bndboxNode,'ymax',str(ymax))

    #写入文件
    f = open(outputPath+'xmls/'+str(i)+'.xml','w')
    f.write(doc.toprettyxml(indent='  '))
    f.close()
    return
if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('backgroundImage', type=str, help='background image')
    parser.add_argument('foregroundImage', type=str, help='foreground image')
    parser.add_argument('name', type=str, help='label of object')
    parser.add_argument('outputPath', type=str, help='the path of output,if it does\'t exits,it will be created')
    parser.add_argument('-r', type=str, default='0:0:0', help='use like -r start:stop:step or start:stop(step=1)')
    parser.add_argument('-s', type=str, default='0:0:0', help='use like -s start:stop:step or start:stop(step=1)')
    parser.add_argument('-n', type=str, default='1', help='the total number of training samples generated')

    args = parser.parse_args()
    # 检查参数
    backgroundPath, foregroundPath, outputPath, r, s, n = CheckArg(args)
    # 准备数据列表
    label = args.name
    backgroundImage = cv2.imread(backgroundPath)
    foregroundImage = cv2.imread(foregroundPath)
    angles = ListGenerator(r)
    scales = ListGenerator(s, 1)
    (h, w) = foregroundImage.shape[:2]
    xStop = backgroundImage.shape[1] - w
    yStop = backgroundImage.shape[0] - h
    xs = ListGenerator([0, xStop, 1])
    ys = ListGenerator([0, yStop, 1])

    center = (w / 2, h / 2)
    imagePath = outputPath + 'imgs'
    xmlPath = outputPath + 'xmls'
    if not os.path.exists(imagePath):
        os.mkdir(imagePath)
    if not os.path.exists(xmlPath):
        os.mkdir(xmlPath)
    # 开始随机生成
    print('start')
    for i in range(n):
        temp = backgroundImage.copy()
        angle = angles[random.randint(0, len(angles) - 1)]
        scale = scales[random.randint(0, len(scales) - 1)]
        x = xs[random.randint(0, len(xs) - 1)]
        y = ys[random.randint(0, len(ys) - 1)]
        M = cv2.getRotationMatrix2D(center, angle, scale)
        transformed = cv2.warpAffine(foregroundImage, M, (w, h))
        oneChannel = cv2.cvtColor(transformed,cv2.COLOR_BGR2GRAY)
        mask = cv2.merge([oneChannel, oneChannel, oneChannel])
        np.copyto(temp[y:y + h, x:x + w], transformed, where=mask.astype(bool))
        cv2.imwrite(imagePath+'/'+str(i)+'.jpg',temp)
        #生成xml
        WriteXml(temp, outputPath, label, i, x, y, w, h)
    # cv2.imshow('back',backgroundImage)
    # cv2.imshow('fore',foregroundImage)
    # cv2.waitKey(0)
    # print(backgroundPath, foregroundPath, outputPath)
    # print(r, s, n)
    #print(angles, scales, xs, ys)
    print('\ndone!')
