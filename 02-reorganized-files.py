#!/bin/python2.7
# -*- coding: UTF-8 -*-  

## 用于测试重新调整目录组织结构

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

def reorg(year):
    files = os.listdir(year)
    for i in files:
        _move_pdf("%s/%s"%(year,i), "stdata/%s"%i)


reorg("stdata4")
reorg("stdata2")
