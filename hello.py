
# -*- coding: utf-8 -*-
#!/usr/bin/env python
import sys  

reload(sys)  
sys.setdefaultencoding('utf8')
from flask import Flask, abort, request, render_template
from uuid import uuid4
import requests
import requests.auth
import urllib
import json
import os
import wolframalpha
import wikipedia
from gtts import gTTS
import pyglet
import speech_recognition as sr
import feedparser 
import notify2 
import os 
import time
from newsapi import NewsApiClient
try:
    from urllib.parse import urlparse
except ImportError:
     from urlparse import urlparse

try:
    from urllib.request import urlopen
except ImportError:
    from urllib2 import urlopen

appId ="V9TXYX-QTVQKH7E9V"
client = wolframalpha.Client(appId)
filename='audio.mp3'
global img
google_api='b5728e66922a4a628d57a9b5f0037e93'

app = Flask(__name__)
@app.route('/')
def index():
   return render_template('index.html')

def primaryImage(title=''):
    url = 'http://en.wikipedia.org/w/api.php'
    data = {'action':'query', 'prop':'pageimages','format':'json','piprop':'original','titles':title}
    try:
        res = requests.get(url, params=data)
        key = res.json()['query']['pages'].keys()[0]
        imageUrl = res.json()['query']['pages'][key]['original']['source']

    except Exception, err:
        imageUrl=('Exception while finding image:= '+str(err))
    return imageUrl

def removeBrackets(variable):
  return variable.split('(')[0]

def resolveListOrDict(variable):
  if isinstance(variable, list):
    return variable[0]['plaintext']
  else:
    return variable['plaintext']

@app.route('/addRegion', methods=['POST'])
def addRegion():
	
	# value=request.form['search']
	# newsapi = NewsApiClient(api_key='b5728e66922a4a628d57a9b5f0037e93')
	# top_headlines = newsapi.get_top_headlines(q='bitcoin',sources='bbc-news,the-verge',category='business',language='en',country='us')
	# top_headlines=newsapi.get_top_headlines(q=str(value),sources='bbc-news')
	# all_articles = newsapi.get_everything(q='bitcoin',sources='bbc-news,the-verge',domains='bbc.co.uk,techcrunch.com',from_param='2017-12-01',to='2017-12-12',language='en',sort_by='relevancy',page=2)
	# sources = newsapi.get_sources()
	# print (top_headlines)
	# print ("hiiiiiiiiiiiiii")
	# print (all_articles)
	# print ("hiiiiiiiiiii")
	# print (sources)
	

	final=[]
	final_image=[]

	value=request.form['search']
	print ("hii")
	try:
		result= client.query(value) 
	except:
		keyword=request.form['search']
		searchResults = wikipedia.search(keyword)
  		if not searchResults:
			print("No result from Wikipedia")
  		try:
			page = wikipedia.page(searchResults[0])
  		except wikipedia.DisambiguationError, err:
			page = wikipedia.page(err.options[0])
		wikiTitle = str(page.title.encode('utf-8'))
		wikiSummary = str(page.summary.encode('utf-8'))
		image1=primaryImage(keyword)
		return render_template('index.html',result =final,image=image1,wikiSummary=wikiSummary)

	if result['@success'] == 'false':
		return render_template('404.html')
	pod0 = result['pod'][0]
	question = resolveListOrDict(pod0['subpod'])
	question = removeBrackets(question)
	image1=primaryImage(question)
	if result is None:
		return None
	total_result=result['@numpods']
	for pod in result.pods:
		for subpod in pod.subpods:
			if (subpod.plaintext) != None:
				a=subpod.plaintext.upper()
				null = None
				p=eval(json.dumps(subpod))
				final.append(a)
	final.pop()
	
	file = gTTS(text=str(a))
	filename='audio.mp3'
	file.save(filename)
	return render_template('index.html',result =final,para=a,image=image1)

@app.route('/addRegion1')
def addRegion1():
	f = feedparser.parse("http://feeds.bbci.co.uk/news/rss.xml") 
	ICON_PATH = os.getcwd() + "/icon.ico"
	notify2.init('News Notify') 
	for newsitem in f['items']: 
		n = notify2.Notification(newsitem['title'], 
								newsitem['summary'], 
								icon=ICON_PATH 
								) 
	n.set_urgency(notify2.URGENCY_NORMAL) 
	n.show() 
	n.set_timeout(15) 
	time.sleep(20)
	return ("Starting Notifier")

@app.route('/addRegion2')
def addRegion2():
	pyglet.have_avbin=True
	music=pyglet.media.load(filename,streaming=False)
	music.play()
	pyglet.app.run()
	return ("Audio Playing")

# @app.route('/news', methods=['GET'])
# def news():
# 	dic={}
# 	des=[]
# 	con=[]
# 	image=[]
# 	newsapi = NewsApiClient(api_key='b5728e66922a4a628d57a9b5f0037e93')
# 	top_headlines=requests.get("https://newsapi.org/v2/top-headlines?country=us&apiKey=b5728e66922a4a628d57a9b5f0037e93")
# 	data = top_headlines.json() 
# 	null=None
# 	data=eval(json.dumps(data))
# 	n=data['totalResults']
# 	data=data['articles']
# 	for i in range(n):
# 		if data[i]['description'] is not None:
# 			des.append(data[i]['description'])
# 			con.append(data[i]['content'])
# 			image.append(data[i]['urlToImage'])
# 	dic['des']=des
# 	dic['image']=image
# 	dic['con']=con
# 	print (dic)
# 	return render_template('raghav.html',dic=dic)

	

if __name__ == '__main__':
    app.run(debug=True, port=5000)


