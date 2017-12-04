# -*- coding: utf-8 -*-
import requests
from bs4 import BeautifulSoup
from urllib import FancyURLopener
from lxml import etree as ET
from lxml import html as lh
import sys
import string
import hashlib
import time
import pdb
import re
import pickle
reload(sys)
sys.setdefaultencoding("UTF8")

arrlink = []
arrtitle = []
arrcontent = []
arrbit = []

## The function below cleans an input string from all html tags
## input: "<html a= href="www.abc.com">qwerty"  output : "qwerty"
def cleanfinhtml(raw_html):
	cleanr = re.compile('<.*?>')
	cleantext = re.sub(cleanr, '', raw_html)
	return cleantext

## The function below cleans an input string from <p> tags
def cleaninihtml(raw_html):
	index = raw_html.find("<p>")
	s = ""
	while(index!=-1):
		t = raw_html.find("</p>",index)
		s = s+ raw_html[index+3:t]
		index = raw_html.find("<p>",t+1)
	return s
punctuation = '!"$%&\'()*+,-./:;=?@[\\]^_`{|}~:.'
dev_digits = u'१२३४५६७८९०'
regex = re.compile('[%s]' % re.escape(dev_digits))

FLAGS = re.MULTILINE | re.DOTALL

def hashtag(text):
    text = text.group()
    hashtag_body = text[1:]
    if hashtag_body.isupper():
        result = " <hashtag> {} <allcaps> ".format(hashtag_body)
    else:
        result = " ".join([" <hashtag> "] + re.split(r"(?=[A-Z])", hashtag_body, flags=FLAGS))
    return result

def allcaps(text):
    text = text.group()
    return text.lower() + " <allcaps> "

## The function below removes all punctuation marks from an input string
def tokenize(text):
    # Different regex parts for smiley faces
    eyes = r"[8:=;]"
    nose = r"['`\-]?"

    # function so code less repetitive
    def re_sub(pattern, repl):
        return re.sub(pattern, repl, text, flags=FLAGS)

    text = re_sub(r"https?:\/\/\S+\b|www\.(\w+\.)+\S*", " <url> ")
    text = re_sub(r"/"," / ")
    text = re_sub(r"@\w+", "<user>")
    text = re_sub(r"{}{}[)dD]+|[)dD]+{}{}".format(eyes, nose, nose, eyes), " <smile> ")
    text = re_sub(r"{}{}p+".format(eyes, nose), " <lolface> ")
    text = re_sub(r"{}{}\(+|\)+{}{}".format(eyes, nose, nose, eyes), " <sadface> ")
    text = re_sub(r"{}{}[\/|l*]".format(eyes, nose), " <neutralface> ")
    text = re_sub(r"<3","<heart>")
    text = re_sub(r"[-+]?[.\d]*[\d]+[:,.\d]*", " <number> ")
    text = re_sub(r"#\S+", hashtag)
    text = re_sub(r"([!?.]){2,}", r"\1 <repeat>")
    text = re_sub(r"\b(\S*?)(.)\2{2,}\b", r" \1\2 <elong> ")
    ## -- I just don't understand why the Ruby script adds <allcaps> to everything so I limited the selection.
    # text = re_sub(r"([^a-z0-9()<>'`\-]){2,}", allcaps)
    text = re_sub(r"([A-Z]){2,}", allcaps)
    text = regex.sub(' <devnum> ', text)
    #' '.join(text.strip(punctuation))
    return text.lower()

## The function below is the gist of the complete program. The function finds all the html links of on a url page.
## All these links are visited. From these links titles and the content of the article are stored.
## Library used here for scraping is BeautifulSoup.
def get_contentListShow(url):
	aurl = url
	html = requests.get(aurl)
	soup = BeautifulSoup(html.content,"lxml")
	article1 = soup.find("div",class_= "clear")
	article1 = (str)(article1)
	article = article1[article1.find("div class=\"clear\""):]
	contentnew = str(article)
	index = contentnew.find("href=")
	count =0
	while(index!=-1 and count < 1000):
		index2 = contentnew.find("=",index)
		s = contentnew[index2+2:contentnew.find(" ",index2+3)-1]
		z = s
		zhtml = requests.get(z)
		zsoup = BeautifulSoup(zhtml.content,"lxml")
		zarticle = zsoup.find("div",class_="entry-content")
		zp = zarticle.find_all('p')
		zp = str(zp)
		fin = cleanfinhtml(cleaninihtml(zp))
		c = tokenize(fin)		
		zarticle = zsoup.find("header",class_="entry-header")
		s = zarticle.find('h1')
		s = (str)(s)
		t = tokenize(cleanfinhtml(s))
		index = contentnew.find("href=http://www.theunrealtimes.com/",index +10)
		if(c!='none' and c!="" and z not in arrlink and z.find("http")!=-1 and z.find(">")==-1 and z.find("\"")==-1):
			arrtitle.append(t)
			arrcontent.append(c)
			arrlink.append(z)
			arrbit.append(1)
			arrdata = [arrlink,arrtitle,arrcontent,arrbit]
			filobj = open("theunrealtimes.txt",'wb')
			pickle.dump(arrdata,filobj)
			filobj.close()
			count = count +1
def main():
	url = "http://www.theunrealtimes.com/category/national/politics/page/"
	num = 1
	while(len(arrbit)<1000):
		get_contentListShow(url+(str)(num))
		num = num+1

if __name__ == '__main__':
	main()
