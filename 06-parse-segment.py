#!/usr/bin/python2.7
# -*- coding: UTF-8 -*-  

## 用于测试内容的提取和关键字的匹配

import os
from cStringIO import StringIO

DIRS = ["2012", "2013", "2014", "2015", "2016"]

def load_data(path):
    data = []
    asid = str()
    line = str()
    text = str()
    cnt = 1
    with open(path, "rt") as f:
        for i in f:
            if cnt == 1:
                asid = i.strip()
            elif cnt == 2:
                line = i.strip()
            else:
                text = i.strip()
                data.append([asid, line, text])
                cnt = 0
            cnt += 1
    return data

def write_io(text, idd):
    with open("res.txt", "at") as f:
        f.write("%d %s\n" % (idd, text))

def parse_data(path):
    y = []
    data = load_data(path)
    for cell in data:
        x = cell[2].replace(" ","").find(r"重大风险提示")
        y.append([x, cell[2]])

#        if x < 100:
#            print cell[0]
#            print cell[2]
    return y


abc =[]
for i in ["2012","2013","2014","2015","2016"]:
    y = parse_data("result-%s.txt" % i) 
    abc.extend(y)
abc.sort()
for i in abc:
    write_io(i[1], i[0])

