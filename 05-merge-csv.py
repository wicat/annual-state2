#!/bin/python2.7
# -*- coding: UTF-8 -*-  

## 用于合并所有csv文件内容
## 并将“重大风险提示内容”进行过滤
## 剔除“重大风险提示”关键字前面的内容
## 同时剔除最后一个句号后面的内容

import os, sys

reload(sys)
sys.setdefaultencoding("utf8")

def do_merge(src, dst):
    itemlist = list()
    for csvf in src:
        with open(csvf, "rt") as f:
            for i in f:
                itemlist.append(i)
    with open(dst, "at") as f:
        for i in itemlist:
            f.write(i)
    print ("Compeletd!")

def find_last(s, ss):
    last_pos = -1
    while True:
        pos = s.find(ss, last_pos+1)
        if pos == -1:
            return last_pos
        last_pos = pos

def do_strip(src):
    itemlist = list()
    with open(src, "rt") as f:
        for i in f:
            x = i.split(',')
            if x[3] != '':
                p1 = x[3].find(u'重大风险提示')
                p2 = find_last(x[3], u'。')
                if p1 == -1: p1 = 0
                x[3] = x[3].decode('utf-8')[p1:p2+1].encode('utf-8')
            itemlist.append(x)
        print ("Read Completed!")
    with open(src+'-2', "at") as f:
        for i in itemlist:
            x = str()
            for j in i:
                x += j + ','
            f.write(x[:-1])
    print ("Write Completed!")


if __name__ == '__main__':
    do_strip("result.csv")
