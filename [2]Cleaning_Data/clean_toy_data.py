import zipfile
import os
import json
from pprint import pprint
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import re
import collections

df = pd.read_json("/home/dk/Downloads/3-1 BITS/Acads/Resources/Information Retrieval/Assignment/our_code/[2]Cleaning_Data/articles_toy_data/2016-05-01.json" , encoding='uth-8')
count = 0
for filename in os.listdir("/home/dk/Downloads/3-1 BITS/Acads/Resources/Information Retrieval/Assignment/our_code/[2]Cleaning_Data/articles_toy_data/"):
    count+=1
    if count>2:
        file_path = "/home/dk/Downloads/3-1 BITS/Acads/Resources/Information Retrieval/Assignment/our_code/[2]Cleaning_Data/articles_toy_data/" + filename
        df_ = pd.read_json(file_path , encoding='uth-8')
        df = pd.concat(objs= [df,df_], axis=0,ignore_index=True)
        
        if count%100 ==0:
            print "This is the ",count,"th file -->"

lst = []
for i in range(df.shape[0]):
    lst.append(df.fields[i]["bodyText"])
df["bodyText"] = lst
lst_head = []
for i in range(df.shape[0]):
        lst_head.append(df.fields[i]["headline"])

df["headline"] = lst_head
df = df[df.bodyText != ""]
df.shape
df = df[(df.sectionName == 'US news') | (df.sectionName == 'Business') | (df.sectionName == 'Politics') | (df.sectionName == 'World news')]
df.info()
collections.Counter(df.sectionName)
df.head()
df.webPublicationDate.min() ,df.webPublicationDate.max()

for idx,item in enumerate(df.bodyText):
    df.bodyText[idx] = re.sub('[^\x00-\x7F]+', "", item)
    if idx%500 == 0:
        print 'Here is the ',idx,'th item'

for idx,item in enumerate(df.headline):
    df.headline[idx] = re.sub('[^\x00-\x7F]+', "", item)
    if idx%500 == 0:
        print 'Here is the ',idx,'th item'

for idx, item in enumerate(df.bodyText):
    df.bodyText[idx] = re.sub('(\\n)',"",item)
    if idx%500 == 0:
        print 'Here is the ',idx,'th item'

for idx, item in enumerate(df.headline):
    df.headline[idx] = re.sub('(\\n)',"",item)
    if idx%500 == 0:
        print 'Here is the ',idx,'th item'

print df.info()
print df[u'headline'][0]
df = df[[u'headline',u'bodyText']]
print ("-------------------------------------------")
print df.info()
print df.head()
print ("-------------------------------------------")
sLength = len(df[u'headline'])
df[u'label'] = pd.Series(['REAL' for _ in range(sLength)],index = df.index)
print ("-------------------------------------------")
print df.info()
print df.head()
print ("-------------------------------------------")

df.to_csv("/home/dk/Downloads/3-1 BITS/Acads/Resources/Information Retrieval/Assignment/our_code/[2]Cleaning_Data/clean_guadian_data/clean_data.csv",encoding='utf-8',index=False)
df_test = pd.read_csv("/home/dk/Downloads/3-1 BITS/Acads/Resources/Information Retrieval/Assignment/our_code/[2]Cleaning_Data/clean_guadian_data/clean_data.csv")
df_test.info()

sum_ = 0
max_ = 0
min_ = 9999
for item in df.bodyText:
    sum_+=len(item)
    if len(item)>max_:
        max_ = len(item)
    if len(item)<min:
        min_ = len(item)


print "Min number of word count",min_ ,"\nMax number of word count",max_,"\nTotal number of word count", sum_
