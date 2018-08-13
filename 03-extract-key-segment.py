#!/bin/python2.7
# -*- coding: UTF-8 -*-  

## 用于测试内容的提取和关键字的比较

import os
from cStringIO import StringIO
from pdfminer.pdfparser import PDFParser
from pdfminer.pdfdocument import PDFDocument
from pdfminer.pdfpage import PDFPage, PDFTextExtractionNotAllowed
from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
from pdfminer.pdfdevice import PDFDevice, TagExtractor
from pdfminer.converter import XMLConverter, HTMLConverter, TextConverter
from pdfminer.cmapdb import CMapDB
from pdfminer.layout import LAParams
from pdfminer.image import ImageWriter

DIRS = ["2010", "2011", "2012", "2013", "2014", "2015", "2016"]
TOPDIR = "stdata/"
RESDIR = "resdir"

def parse_pdf(fname, outfile, pdst):
    cnt = 1
    fid = fname.split("/")[-1].split(".")[0]
    outlist = list()
    outfp = StringIO()
    fp = file(fname, 'rb')
    
    rsrcmgr = PDFResourceManager(caching=True)        
    device = TextConverter(rsrcmgr, outfp, codec='utf-8', laparams=LAParams(), imagewriter=None)
    interpreter = PDFPageInterpreter(rsrcmgr, device)

    for page in PDFPage.get_pages(fp, set(), maxpages=0, caching=True, check_extractable=True):
        interpreter.process_page(page)
        cell = outfp.getvalue().replace("\n","").replace("\r","").rstrip()
        outfp.truncate(0)
        
        #outlist.append(cell)
        if r"重大风险提示" in cell:
            with open(outfile, "at") as f:
                f.write(fid+"\n")
                f.write("%d\n" % cnt)
                f.write(cell+"\n")
            if os.path.exists(pdst): print("DST <%s> EXISTS!" % pdst)
            else: os.rename(fname, pdst)

        if cnt == 10: break
        cnt += 1

    fp.close()
    device.close()
    outfp.close()
    return

def do_parse(fdate):
    psrc = "stdata/" + fdate
    pdst = "stdata2/" + fdate
    if not os.path.isdir(pdst): os.mkdir(pdst)

    files = os.listdir(psrc)
    for i in files:
        try:
            x = parse_pdf(psrc+i, "result-%s.txt" % fdate[:-1], pdst+i)
        except:
            with open("error.log", "at") as f:
                f.write(i+"\n")


do_parse("2012/")
do_parse("2013/")
do_parse("2014/")
do_parse("2015/")
do_parse("2016/")

