#coding=utf-8

#urllib模块提供了读取Web页面数据的接口
import urllib.request as urllib
#re模块主要包含了正则表达式
import re
#定义一个getHtml()函数
def getHtml(url):
    page = urllib.urlopen(url)  #urllib.urlopen()方法用于打开一个URL地址
    html = page.read() #read()方法用于读取URL上的数据
    html = html.decode('utf8')
    return html

def getImg(html,page):
    reg = r'https://.+?\.jpg'    #正则表达式，得到图片地址
    #re.findall(r'([http|https]:[^\s]*?(jpg|png|gif))'
    patten = re.compile(reg)
    imglist = patten.findall(html)      #re.findall() 方法读取html 中包含 imgre（正则表达式）的    数据
    #把筛选的图片地址通过for循环遍历并保存到本地
    #核心是urllib.urlretrieve()方法,直接将远程数据下载到本地，图片通过x依次递增命名
    removeRepeat = sorted(set(imglist),key=imglist.index)
    x = 0

    for imgurl in removeRepeat:
        print(imgurl)
        urllib.urlretrieve(imgurl,'negative/%s_%s.jpg' %(int(page), x))
        x+=1

address = 'https://image.baidu.com/search/flip?tn=baiduimage&ie=utf-8&word=%E9%AB%98%E9%80%9F%E5%9B%BE%E7%89%87&pn='
for i in range(0,10000,20):
    url = address+str(i)
    print('正在下载第%d页'%(i/20))
    html = getHtml(url)
    getImg(html,i/20)
#html = getHtml("https://image.baidu.com/search/flip?tn=baiduimage&ie=utf-8&word=%E9%AB%98%E9%80%9F%E5%9B%Bhttps://image.baidu.com/search/flip?tn=baiduimage&ie=utf-8&word=%E9%AB%98%E9%80%9F%E5%9B%BE%E7%89%87&pn=0&gsm=50&ct=&ic=0&lm=-1&width=0&height=0E%E7%89%87&ct=201326592&ic=0&lm=-1&width=&height=&v=flip")
#print(html)
#getImg(html)
#print(getImg(html))