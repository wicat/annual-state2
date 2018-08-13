#!/usr/bin/python2.7
# -*- coding: UTF-8 -*-

import os, sys, logging
import jieba
from gensim import corpora, models, similarities

#logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)

#reload(sys)
#sys.setdefaultencoding("utf-8")

# return string
def _merge_after_remove_header_and_footer(l_pages):
    footerbet = u"1234567890-=+<>/"
    l_segs = list()
    s_ret = str()
    nr_pages = len(l_pages)
    cnt = 0
    if nr_pages > 1:
        x1 = l_pages[0].replace(" ", "")
        x2 = l_pages[1].replace(" ", "")
        minlen = min(len(x1), len(x2))
        for i in range(minlen):
            if x1[i] != x2[i]:
                break
            cnt += 1
    ## remove header
    for i in l_pages:
        l_segs.append(i.replace(" ", "")[cnt:])
    ## remove footer and merge
    for i in l_segs:
        if len(i) == 0:
            continue
        while i[-1] in footerbet:
            i = i[:-1]
            if len(i) == 0:
                break
        s_ret += i
    return s_ret

def _split_by_tab_and_filte_english(l_origin):
    alphabet = u"QWERTYUIOPASDFGHJKLZXCVBNMqwertyuiopasdfghjklzxcvbnm"
    l_later = list()
    for i in l_origin:
        tmp = i.replace(" ","")
        tmp_cnt = 0
        for j in tmp:
            if j in alphabet:
                tmp_cnt += 1
        if float(tmp_cnt) / len(tmp) > 0.1:
            continue
        l_later.append(i.split("\t"))
    return l_later

def _merge_and_split_by_keyword(l_origin):
    l_middle = list()
    l_later = list()
    for i in l_origin:
        if len(i) == 2:
            continue
        cnt = 0
        for j in i:
            if u"重要提示" in j or u"第一节" in j:
                if cnt < 8:
                    l_middle.append(i)
                break
            cnt += 1
    for i in l_middle:
        segment = _merge_after_remove_header_and_footer(i[2:])
        segments = segment.split(u"重要提示")
        if len(segments) == 2:
            l_later.append([i[0], i[1], segments[1]])
    return l_later

def __remove_dup_v1(lines_list):
    dictionaries = list()
    lsis = list()
    indexes = list()
    cnts =[0 for i in range(len(lines_list))]
    print "PRE"
    for item in lines_list:
        words = [[word for word in jieba.lcut(line)] for line in item]
        dictionary = corpora.Dictionary(words)
        corpus = [dictionary.doc2bow(word) for word in words]
        lsi = models.LsiModel(corpus, id2word=dictionary, num_topics=20)
        index = similarities.MatrixSimilarity(lsi[corpus])
        dictionaries.append(dictionary)
        lsis.append(lsi)
        indexes.append(index)
    print "DO"
    for n in range(len(lines_list)):
        for line in lines_list[n]:
            compare_text = dictionaries[n].doc2bow(jieba.lcut(line))
            query_lsi = lsis[n][compare_text]
            sims = indexes[n][query_lsi]
            for key, val in enumerate(sims):
                if val > 0.9:
                    cnts[n] += 1
    print cnts
    print "DONE"

def __remove_dup_v2(lines):
    candidate = list()
    candidate.append(lines[0])
    print "PRE"
    words = None
    dictionary = None
    corpus = None
    lsi = None
    index = None
    rebuild = True
    for line in lines:
        if rebuild:
            words = [[word for word in jieba.lcut(item)] for item in candidate]
            dictionary = corpora.Dictionary(words)
            corpus = [dictionary.doc2bow(word) for word in words]
            lsi = models.LsiModel(corpus, id2word=dictionary, num_topics=20)
            index = similarities.MatrixSimilarity(lsi[corpus])

        compare_text = dictionary.doc2bow(jieba.lcut(line))
        query_lsi = lsi[compare_text]
        sims = index[query_lsi]
        flag = True
        for m,elem in enumerate(sims):
            if elem > 0.9:
                flag = False
                break
        if flag:
            candidate.append(line)
            rebuild = True
        else:
            rebuild = False
    with open("result-1516-tmp1.csv", "at") as f:
        for i in candidate:
            f.write(i.encode("utf-8")+"\n")
    print "DONE"

def __remove_dup_v3(lines):
    cnts =[0 for i in range(len(lines))]
    print "PRE"
    words = [[word for word in jieba.lcut(line)] for line in lines]
    dictionary = corpora.Dictionary(words)
    corpus = [dictionary.doc2bow(word) for word in words]
    lsi = models.LsiModel(corpus, id2word=dictionary, num_topics=20)
    index = similarities.MatrixSimilarity(lsi[corpus])
    print "DO"
    for n in range(0, len(lines)):
        compare_text = dictionary.doc2bow(jieba.lcut(lines[n]))
        query_lsi = lsi[compare_text]
        sims = index[query_lsi]
        for m,elem in enumerate(sims):
            if elem > 0.9:
                cnts[n] += 1
    with open("result-1516-tmp2.csv", "at") as f:
        for i in range(len(cnts)):
            if cnts[i] > 30:
                f.write(lines[i].encode("utf-8")+"\n")
    print "DONE"

def _remove_duplicate(l_origin):
    lines = list()
    lines_list = list()
    for i in l_origin:
        tmp = i[2].split(u"。")
        while "" in tmp:
            tmp.remove("")
        lines.extend(tmp)
        lines_list.append(tmp)
    #__remove_dup_v1(lines_list)
    #__remove_dup_v2(lines)
    #__remove_dup_v3(lines)

def _split_segs_by_kw(l_origin):
    cntsucc = 0
    cntfail = 0
    l_later = list()
    for i in l_origin:
        tmp = i[2].split(u"。")
        while "" in tmp:
            tmp.remove("")
        flag = True
        cnt = 0
        for j in tmp:
            if u"风险" in j or u"風險" in j:
                flag = False
                break
            cnt += 1
        if flag:
            cntfail += 1
            l_later.append([i[0], i[1], "0", ""])
        else:
            cntsucc += 1
            tmp = tmp[cnt:]
            tmpstr = str()
            for k in tmp:
                if u"√适用□不适用" in k:
                    k = k.replace(u"√适用□不适用", "")
                if u"□适用√不适用" in k:
                    k = k.replace(u"□适用√不适用", "")
                if u"其他" in k and len(k) < 20:
                    continue
                if u"不派发现金红利" in k:
                    continue
                if u"通过的利润分配" in k:
                    continue
                tmpstr += k + u"。"
            l_later.append([i[0], i[1], "1", tmpstr[:-1].replace(u",", u"，")])

    with open("result-1516-ver2.csv", "at") as f:
        for i in l_later:
            f.write("%s, %s, %s, %s\n" % (i[0].encode("utf-8"),i[1].encode("utf-8"),i[2].encode("utf-8"), i[3].encode("utf-8")))
    print "SUCCESS=%d, FAILED=%d" % (cntsucc, cntfail)
    print "Completed!"

def main_first_half():
    l_origin = list()
    l_later = list()
    with open("result-1516.csv", "rt") as f:
        for i in f:
            l_origin.append(unicode(i.replace("\n","").replace("\r",""), "utf-8"))
    print len(l_origin)
    l_later = _split_by_tab_and_filte_english(l_origin)
    print len(l_later)
    l_later = _merge_and_split_by_keyword(l_later)
    print len(l_later)
    with open("result-1516-ver1.csv", "at") as f:
        for i in l_later:
            f.write("%s\t%s\t%s\n" % (i[0].encode("utf-8"),i[1].encode("utf-8"),i[2].encode("utf-8")))
    print "Completed!"
    return

def main_last_half():
    l_origin = list()
    l_later = list()
    with open("result-1516-ver1.csv", "rt") as f:
        for i in f:
            l_origin.append(unicode(i.strip(), "utf-8"))
    for i in l_origin:
        l_later.append(i.split("\t"))
    print len(l_later)
    _split_segs_by_kw(l_later)
    #_remove_duplicate(l_later)
    print "Completed!"
    return


if __name__ == '__main__':
    #main_first_half()
    main_last_half()
