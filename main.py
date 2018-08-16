#!/bin/python2.7
# -*- coding: UTF-8 -*-  

import os, sys
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


def ListDirs(dirpath):
    files = list()
    rets = os.listdir(dirpath)
    for i in rets:
        p = dirpath + "/" + i
        if os.path.isdir(p):
            rets2 = ListDirs(p)
            files.extend(rets2)
        else:
            files.append(p)
    return files


def GetID(filepath):
    sid = filepath.split("/")[-1][:6]
    if sid.isdigit():
        return sid
    else:
        return sid[:-1]


def GetName(text):
    noise = [r'0',r'1',r'2',r'3',r'4',r'5',r'6',r'7',r'8',r'9']
    pos = 1000
    for i in noise:
        t = text.find(i)
        if t > 0:
            pos = min(pos, t)
    if pos < 5 or pos > 200:
        return ""
    return text[:pos]


def DoParse(fname):
    outfp = StringIO()
    fp = file(fname, 'rb')
    cell_text = str()
    sname = str()
    s1 = 0
    s2 = 0
    s3 = 0
    s4 = 0
    s5 = 0
    flag = True
    rsrcmgr = PDFResourceManager(caching=True)
    device = TextConverter(rsrcmgr, outfp, codec='utf-8', laparams=LAParams(), imagewriter=None)
    interpreter = PDFPageInterpreter(rsrcmgr, device)
    for page in PDFPage.get_pages(fp, set(), maxpages=0, caching=True, check_extractable=True):
        interpreter.process_page(page)
        cell = outfp.getvalue().replace("\n","").replace("\r","").replace("\t","").replace(" ","")
        outfp.truncate(0)
        cell_text += cell
        if flag:
            flag = False
            sname = GetName(cell)
    fp.close()
    device.close()
    outfp.close()
    noise = [r"`", r"~", r"!", r"@", r"#", r"$", r"%", r"^", r"&", r"*", r"(", r")", r"_", r"+", r"-", r"=", 
             r"[", r"]", r"{", r"}", r"\\", r"|", r";", r":", r"'", r"\"", r",", r".", r"/", r"<", r">", r"?", r"、",
             r"·", r"！", r"（", r"）", r"【", r"】", r"；", r"‘", r"’", r"：", r"“", r"”", r"，", r"《", r"。", r"》", r"？",
             r"0", r"1", r"2", r"3", r"4", r"5", r"6", r"7", r"8", r"9", r"a", r"b", r"c", r"d", r"e", r"f", r"g",
             r"h", r"i", r"j", r"k", r"l", r"m", r"n", r'o', r'p', r'q', r'r', r's', r't', r'u', r'v', r'w', r'x', r'y',
             r'z', r'A', r'B', r'C', r'D', r'E', r'F', r'G', r'H', r'I', r'J', r'K', r'L', r'M', r'N', r'O', r'P', r'Q',
             r'R', r'S', r'T', r'U', r'V', r'W', r'X', r'Y', r'Z']
    for i in noise:
        cell_text = cell_text.replace(i, "")
    if r"吸收合并" in cell_text:
        s1 = 1
        if r"未吸收合并" in cell_text or r"未发生吸收合并" in cell_text:
            s2 = 1
        if r"吸收合并子公司" in cell_text or r"吸收合并公司" in cell_text:
            s3 = 1
        if r"吸收合并全资子公司" in cell_text:
            s4 = 1
        if r"吸收合并控股子公司" in cell_text:
            s5 = 1
    return sname, s1, s2, s3, s4, s5


if __name__ == '__main__':
    #files = ListDirs("data")
    files = list()
    with open("filepaths-%s.txt" % sys.argv[1], "rt") as f:
        for i in f: files.append(i.strip())

    for filepath in files:
        sid = GetID(filepath)
        spath = filepath
        syear = filepath[5:9]
        sname = str()
        s1 = 0
        s2 = 0
        s3 = 0
        s4 = 0
        s5 = 0
        try:
            sname, s1, s2, s3, s4, s5 = DoParse(filepath)
            with open("result-%s.csv" % sys.argv[1], "at") as f:
                ret = "'%s,%s,%s,%s,%d,%d,%d,%d,%d\n" % (sid, syear, sname, spath, s1, s2, s3, s4, s5)
                f.write(ret)
            with open("done-%s.log" % sys.argv[1], "at") as f:
                f.write(filepath + "\n")
            if sname == "":
                with open("unname-%s.log" % sys.argv[1], "at") as f:
                    f.write(filepath + "\n")
        except Exception, e:
            #print(e)
            with open("error-%s.log" % sys.argv[1], "at") as f:
                f.write(filepath + "\n")

