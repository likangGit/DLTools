#encoding:utf-8
#author：likang
#email：749900261@qq.com
from scipy.misc import imsave
import numpy as np

# 解压缩，返回解压后的字典
def unpickle(file):
    fo = open(file, 'rb')
    data = fo.read()
    dict = np.array(bytearray(data)).reshape((10000,-1))
    fo.close()
    return dict
# 生成训练集图片，如果需要png格式，只需要改图片后缀名即可。
for j in range(1, 6):
    dataName = "data_batch_" + str(j)+".bin"  # 读取当前目录下的data_batch12345文件，dataName其实也是data_batch文件的路径，本文和脚本文件在同一目录下。
    Xtr = unpickle(dataName)
    print(dataName + " is loading...")

    for i in range(0, 10000):
        if Xtr[i, 0] == 1:
            img = np.reshape(Xtr[i,1:], (3, 32, 32))  # Xtr['data']为图片二进制数据
            img = img.transpose((1, 2, 0))  # 读取image
            picName = 'train/' + str(Xtr[i,0]) + '_' + str(i + (j - 1)*10000) + '.bmp'  # Xtr['labels']为图片的标签，值范围0-9，本文中，train文件夹需要存在，并与脚本文件在同一目录下。
            imsave(picName, img)
    print(dataName + " loaded.")

print("test_batch is loading...")

# 生成测试集图片
testXtr = unpickle("test_batch.bin")
for i in range(0, 10000):
    if testXtr[i,0] == 1:
        img = np.reshape(testXtr[i,1:], (3, 32, 32))
        img = img.transpose((1, 2, 0))
        picName = 'test/' + str(testXtr[i,0]) + '_' + str(i) + '.bmp'
        imsave(picName, img)
print("test_batch loaded.")