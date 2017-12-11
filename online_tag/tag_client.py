#encoding=utf8
import zerorpc
import os

if __name__ == '__main__':
    c = zerorpc.Client(timeout=2)
    c.connect("tcp://0.0.0.0:10033")
    #contents = [u"带份饭", "买包烟"]
    contents = '悬赏一个键盘手会弹钢琴的，有时间组乐队的'
    tag = c.tag(contents)           
    print(tag)

