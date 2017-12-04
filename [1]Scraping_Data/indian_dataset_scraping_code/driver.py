import pickle
import numpy
import re
from cleaner import tokenize
import io

#removes the html tags from the title and the content
def clean(raw_html):
    cleanr = re.compile('<.*?>')
    cleantext = re.sub(cleanr,'',raw_html)
    return cleantext

pickle_off = open("ix_final.txt","rb")
ix = pickle.load(pickle_off,encoding='Unicode')

pickle_off = open("toi.txt","rb")
toi = pickle.load(pickle_off,encoding='UTF8')

pickle_off = open("theunrealtimes.txt","rb")
ut = pickle.load(pickle_off,encoding='UTF8')

pickle_off = open("farzinews.txt","rb")
fz = pickle.load(pickle_off,encoding='UTF8')

pickle_off = open("newsnotmatter.txt","rb")
new = pickle.load(pickle_off,encoding='UTF8')

pickle_off = open("teekhimirchi.txt","rb")
tm = pickle.load(pickle_off,encoding='UTF8')

pickle_off = open("ht.txt","rb")
ht = pickle.load(pickle_off,encoding='UTF8')

a = []
z = []
for i in range(0,len(ix[0])):
    link = ix[0][i]
    t = tokenize(clean(ix[1][i]))
    t = t[22:]
    s = tokenize(clean(ix[2][i]))
    c = ix[3][i]
    a.append(link)
    a.append(t)
    a.append(s)
    a.append(c)
    z.append(a)
    a = []


for i in range(0,len(ut[0])):
    link = ut[0][i]
    t = tokenize(clean(ut[1][i]))
    s = tokenize(clean(ut[2][i]))
    c = ut[3][i]
    a.append(link)
    a.append(t)
    a.append(s)
    a.append(c)
    z.append(a)
    a = []

for i in range(0,len(fz[0])):
    link = fz[0][i]
    t = tokenize(clean(fz[1][i]))
    s = tokenize(clean(fz[2][i]))
    c = fz[3][i]
    a.append(link)
    a.append(t)
    a.append(s)
    a.append(c)
    z.append(a)
    a = []

for i in range(0,len(new[0])):
    link = new[0][i]
    t = tokenize(clean(new[1][i]))
    s = tokenize(clean(new[2][i]))
    c = new[3][i]
    a.append(link)
    a.append(t)
    a.append(s)
    a.append(c)
    z.append(a)
    a = []

for i in range(0,len(tm[0])):
    link = tm[0][i]
    t = tokenize(clean(tm[1][i]))
    s = tokenize(clean(tm[2][i]))
    c = tm[3][i]
    a.append(link)
    a.append(t)
    a.append(s)
    a.append(c)
    z.append(a)
    a = []

for i in range(0,len(ht[0])):
    link = ht[0][i]
    t = tokenize(clean(ht[1][i]))
    s = tokenize(clean(ht[2][i]))
    c = ht[3][i]
    a.append(link)
    a.append(t)
    a.append(s)
    a.append(c)
    z.append(a)
    a = []

with io.open("data_1.csv", 'w', encoding="utf-8") as fh:
    for row in z:
        strin = str(row[1])+","+str(row[2])+","+str(row[3])+"\n"
        fh.write(strin)
