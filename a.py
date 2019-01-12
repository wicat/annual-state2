import codecs

ret = []
with codecs.open("result.csv", "r", encoding="utf-8") as f: 
    for i in f:
        ret.append(i.split(","))


qwe = []
for i in ret:
    if len(i) > 9:
        x = i[2:-5]
        y = ""
        for j in x:
            y += j
        z = [i[0], i[1], y, i[-6],i[-5],i[-4],i[-3],i[-2],i[-1]]
        qwe.append(z)
    else:
        qwe.append(i)

with codecs.open("ret.csv", "a", encoding="utf-8") as f:
    for i in qwe:
        s = ''
        for j in i:
            s += j + ","
        f.write(s[:-1])
