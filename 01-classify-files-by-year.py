#!/bin/python2.7
# -*- coding: UTF-8 -*-  

## 将原始目录的组织结构进行调整，按照年份将文件放置到对应年份的目录中

import os

DIRS = ["2010", "2011", "2012", "2013", "2014", "2015", "2016"]
TOPDIR = "stdata/"
RESDIR = "resdir"

def _check_dir(path):
    if not os.path.isdir(path):
        os.mkdir(path)

def check_dir():
    for i in DIRS:
        _check_dir(TOPDIR+i)
    _check_dir(RESDIR)

def _rename_id(id1, lls, c=1):
    id2 = "%s-%d" % (id1, c)
    if id2 in lls:
        id2 = _rename_id(id1, lls, c+1)
    return id2

def _move_pdf(src, dst):
    if os.path.exists(dst):
        print("DST<%s> EXISTS!" % dst)
    else:
        os.rename(src, dst)

def classify_1516():
    lls = []
    files = os.listdir("2015")
    for i in files:
        x = i.split(".")
        t = x[0][:6]

        if t in lls:
            t = _rename_id(t, lls)
        lls.append(t)
        dst = TOPDIR + "2015/" + t + ".pdf"
        _move_pdf("2015/"+i, dst)

def _classify_1214(i, t, lls, d):
    if t in lls:
        t = _rename_id(t, lls)
    lls.append(t)
    dst = TOPDIR + d + t + ".pdf"
    _move_pdf("2012-2014/"+i, dst)
    return lls

def classify_1214():
    lls = []
    lls13 = os.listdir("stdata/2013/")
    for i in lls13:
        lls.append(i.split(".")[0])

    files = os.listdir("2013")
    for i in files:
        x = i.split(".")
        t = x[0][:6]
        u = x[0][6:]

        if t in lls:
            t = _rename_id(t, lls)
        lls.append(t)
        dst = TOPDIR + "2013/" + t + ".pdf"
        _move_pdf("2013/"+i, dst)


