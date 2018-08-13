#!/usr/bin/python2.7
# -*- coding: UTF-8 -*-  

## 从目录stdata中读取所有文件，匹配文件名首的年份，执行目标年份的文件
## 其中stdata目录下文件的命名格式为：年份+ID.pdf，例如：2012+100001.pdf
## 对于匹配年份成功的文件，执行下面的操作：
##      1. 提取证券代码、年份
##      2. 遍历pdf的前十页，判断是否有重大风险提示、提取风险提示的内容
##      3. 对于存在重大风险提示的情况，过滤页眉内容
##      4. 判断重大风险提示是否单列在一页纸上（此时排除了页眉影响但未排除后面跟内容的情况）
##      5. 遍历整个文档，直到存在非标审计意见或退出文档
##      6. 将提取的内容叠加到csv文件中，并将处理过后的文件移动到stdata2中
##
## csv文档格式：证券代码(num)/年份(num)/重大风险提示(0-1)/重大风险提示内容(str)/
##              重大风险提示分类(1-7)/具体风险点(str)/风险点具体外因(str)/
##              风险点具体内因(str)/非标审计意见(0-1)/重大风险是否单列一页纸(0-1)

import os, traceback, sys, chardet
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

reload(sys)
sys.setdefaultencoding("utf8")

def _move_pdf(src, dst):
    if os.path.exists(dst): print("DST<%s> EXISTS!" % dst)
    else: os.rename(src, dst)

def _list2str(l):
    s = str()
    for i in l: s += i.replace(",", r"，") + "|"
    return (s[:-1] if len(s) > 0 else "")

def _get_header(cell1, cell2):
    header = 0
    pos = min(len(cell1), len(cell2))
    for i in range(pos):
        if cell1[i] != cell2[i]:
            header = cell1[:i]
            return i
    return 0

def _ptip_text(cell):
    ptip = False
    ptip_text = ""
    pone_page = False
    if u"重大风险提示" in cell:
        if u"........" in cell or u"······" in cell or u"目录" in cell:
            pass
        else:
            ptip = True
            ptip_text = cell
    return (ptip, ptip_text, pone_page)

def _padvise(cell):
    if u"出具了" in cell and u"意见" in cell:
        return True
    return False
        
def parse_pdf(fname, outfile):
    _pid = fname.split("/")[-1].split(".")[0].split("+")
    pid = _pid[0]
    pyear = _pid[1]
    ptip = False
    ptip_text = ""
    ptip_type = 0
    ptip_cate = []
    ptip_iner = []
    ptip_outr = []
    padvise = False
    pone_page = False

    cnt = 0
    last_page = None
    header = []

    #print "INFO: NEW PDF DOC"
    outfp = StringIO()
    fp = file(fname, 'rb')
    rsrcmgr = PDFResourceManager(caching=True)        
    device = TextConverter(rsrcmgr, outfp, codec='utf-8', laparams=LAParams(), imagewriter=None)
    interpreter = PDFPageInterpreter(rsrcmgr, device)

    for page in PDFPage.get_pages(fp, set(), maxpages=0, caching=True, check_extractable=True):
        interpreter.process_page(page)
        cell = outfp.getvalue().replace("\n","").replace("\r","").replace("\t","").replace(" ","")
        #print "INFO: PARSING CELL"
        outfp.truncate(0)
        
        ###------------------------------------###
        if cnt <= 10 and ptip == False:
            (ptip, ptip_text, pone_page) = _ptip_text(cell)
            #print "INFO: ptip=", ptip, "ptip_text=", ptip_text, "pone_page=", pone_page, "header=", header
            cnt += 1
        
        if cnt > 2 and last_page != None:
            header.append(_get_header(last_page, cell))
        last_page = cell

        if not padvise:
            padvise = _padvise(cell)
        if padvise and ptip:
            break
        ###------------------------------------###

    fp.close()
    device.close()
    outfp.close()
    
    header.sort()
    half = len(header) // 2
    lenhdr = (header[half] + header[~half]) / 2 + 2
    ptmp_text = ptip_text
    while lenhdr > 0 and len(ptip_text) > lenhdr:
        ptmp_text = ptip_text[lenhdr:]
        try:
            ret = ptmp_text.find(u"重大风险提示")
            if ret != -1 and ret < 5:
                pone_page = True
            ptip_text = ptmp_text
            break
        except:
            lenhdr -= 1

    with open(outfile, "at") as f:
        f.write(pid+",")
        f.write(pyear+",")
        ptip = "1" if ptip else "0"
        f.write(ptip+",")
        ptip_text = ptip_text.replace(",", r"，")
        f.write(ptip_text+",")
        f.write(str(ptip_type)+",")
        ptip_cate = _list2str(ptip_cate)
        f.write(ptip_cate+",")
        ptip_iner = _list2str(ptip_iner)
        f.write(ptip_iner+",")
        ptip_outr = _list2str(ptip_outr)
        f.write(ptip_outr+",")
        padvise = "1" if padvise else "0"
        f.write(padvise+",")
        pone_page = "1" if pone_page else "0"
        f.write(pone_page+"\n")    
    return

def wtf(year):
    files = os.listdir("stdata")
    cnt = 0
    for i in files:
        if i[:4] != year: continue
        try:
            parse_pdf("stdata/"+i, "result-%s.csv"%year)
            _move_pdf("stdata/"+i, "stdata2/"+i)
        except:
            #print traceback.print_exc()
            with open("error.log", "at") as f: f.write(i+"\n")
        cnt += 1
        if cnt % 100 == 0:
            print cnt
    print "Completed!"
    return


if len(sys.argv) != 2 and sys.argv not in ['2012','2013','2014','2015','2016']:
    exit()
print sys.argv[1]
wtf(sys.argv[1])

