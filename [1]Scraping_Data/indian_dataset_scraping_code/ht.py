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
def cleanhtml(raw_html):
	cleanr = re.compile('<.*?>')
	cleantext = re.sub(cleanr, '', raw_html)
	return cleantext
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
	article = soup.find("section",class_= "container")
	contentnew = str(article)
	index = contentnew.find("href=")
	count = 0
	while(index!=-1 and count < 500):
		index2 = contentnew.find("=",index)
		s = contentnew[index2+2:contentnew.find(">",index2+3)-1]
		z = s
		try:
			zhtml = requests.get(z)
		except:
			pass
		zsoup = BeautifulSoup(zhtml.content,"lxml")
		zarticle = zsoup.find("article",class_="story-article")
		t = ""
		p = ""
		try:
			t = tokenize(cleanhtml((str)(zarticle.find('h1'))))
			p = zarticle.find_all('p')
		except:
			pass				
		zarticle = str(p)
		c = tokenize(cleanhtml(zarticle))

		if(c!='none' and c!="" and z not in arrlink and z.find("http")!=-1 and z.find(">")==-1 and z.find("\"")==-1):
			arrtitle.append(t)
			arrcontent.append(c)
			arrlink.append(z)
			arrbit.append(0)
			arrdata = [arrlink,arrtitle,arrcontent,arrbit]
			filobj = open("ht.txt",'wb')
			pickle.dump(arrdata,filobj)
			filobj.close()
			count = count +1

		index = contentnew.find("href",index2+20)

def main():
	url = "http://www.hindustantimes.com/india-news/"
	get_contentListShow(url)

if __name__ == '__main__':
	main()
