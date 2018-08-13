#!/bin/python2.7
# -*- coding: UTF-8 -*-  

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


def parse_pdf(fname):
    outfp = StringIO()
    fp = file(fname, 'rb')
    cell_text = str()
    rsrcmgr = PDFResourceManager(caching=True)
    device = TextConverter(rsrcmgr, outfp, codec='utf-8', laparams=LAParams(), imagewriter=None)
    interpreter = PDFPageInterpreter(rsrcmgr, device)
    for page in PDFPage.get_pages(fp, set(), maxpages=0, caching=True, check_extractable=True):
        interpreter.process_page(page)
        cell = outfp.getvalue().replace("\n","").replace("\r","").replace("\t","").replace(" ","")
        outfp.truncate(0)
        cell_text += cell
    fp.close()
    device.close()
    outfp.close()
    noise = [r"`", r"~", r"!", r"@", r"#", r"$", r"%", r"^", r"&", r"*", r"(", r")", r"_", r"+", r"-", r"=", 
             r"[", r"]", r"{", r"}", r"\\", r"|", r";", r":", r"'", r"\"", r",", r".", r"/", r"<", r">", r"?", r"、",
             r"·", r"！", r"（", r"）", r"【", r"】", r"；", r"‘", r"’", r"：", r"“", r"”", r"，", r"《", r"。", r"》", r"？",]
    for i in noise:
        cell_text = cell_text.replace(i, "")
    return cell_text



if __name__ == '__main__':
    files = ListDirs("data")
    try:
        ret = parse_pdf(files[0])
        print(ret)
    except:
        pass
#        with open("error.log", "at") as f:
#            f.write(+"\n")
