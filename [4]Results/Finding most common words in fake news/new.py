import pandas as pd

d = dict()

df = pd.read_csv("clean_indian_dataset.csv")

df.columns = ['title','text','label']
df.title = df.title.str.lower()
df.text = df.text.str.lower()
df.title = df.title.str.replace(r'http[\w:/\.]+','<URL>') # remove urls
df.text = df.text.str.replace(r'http[\w:/\.]+','<URL>') # remove urls
df.title = df.title.str.replace(r'[^\.\w\s]','') #remove everything but characters and punctuation
df.text = df.text.str.replace(r'[^\.\w\s]','') #remove everything but characters and punctuation
df.title = df.title.str.replace(r'\.\.+','.') #replace multple periods with a single one
df.text = df.text.str.replace(r'\.\.+','.') #replace multple periods with a single one
df.title = df.title.str.replace(r'\.',' . ') #replace periods with a single one
df.text = df.text.str.replace(r'\.',' . ') #replace multple periods with a single one
df.title = df.title.str.replace(r'\s\s+',' ') #replace multple white space with a single one
df.text = df.text.str.replace(r'\s\s+',' ') #replace multple white space with a single one
df.title = df.title.str.strip() 
df.text = df.text.str.strip() 


for li1 in range(len(df)):
	if df.iloc[li1].label == 1:
		words = df.iloc[li1].text.split()
		temp_dict = set()
		for word in words:
			if word in temp_dict:
				continue
			word = word.lower()
			if word in d:
				d[word] = d[word] + 1
			else:
				d[word] = 1
			temp_dict.add(word)

count = 0
for key,value in sorted(d.iteritems(),key=lambda (k,v): (v,k),reverse=True):
	print "Word = ",key,"-",value
	count += 1
	if count > 500:
		break
