#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
"""
import time
from datetime import datetime
import json
import os
import requests
import feedparser
from flask import Flask, render_template, redirect, url_for, request

application = Flask(__name__, instance_relative_config=True)

@application.route("/")
def homepage():
    return render_template("welcome.html")

@application.route('/<get_usr_txt>')
def not_homepage(get_usr_txt):
  
    return redirect(url_for('newsSpider'), code=302)


@application.route("/newsSpider", methods = ["GET", "POST"] )
def newsSpider():

    rssUrlList = {
            "topstories": { 
                "googlenews"        : "https://news.google.co.in/news?cf=all&hl=en&pz=1&ned=in&output=rss",
                "economictimes"     : "http://economictimes.indiatimes.com/rssfeedstopstories.cms"
            },

            "india" : {
                "googlenews"        : "http://news.google.co.in/news?cf=all&hl=en&pz=1&ned=in&topic=n&output=rss",
                "bbc"               : "http://feeds.bbci.co.uk/news/world/asia/india/rss.xml",
                "hindu"             : "http://www.thehindubusinessline.com/news/national/?service=rss"
            },

            "world" : {
                "googlenews"        : "https://news.google.co.in/news?cf=all&hl=en&pz=1&ned=in&topic=w&output=rss",
                "bbc"               : "http://feeds.bbci.co.uk/news/world/rss.xml",
                "hindu"             : "http://www.thehindubusinessline.com/news/national/?service=rss"
            },

            "business" : {
                "economictimes"     : "http://economictimes.indiatimes.com/markets/rssfeeds/1977021501.cms",
                "hindu"             : "http://www.thehindubusinessline.com/markets/?service=rss",
                "googlenews"        : "http://news.google.co.in/news?cf=all&hl=en&pz=1&ned=in&topic=b&output=rss"
            },

            "opinion" : {
                "hindu"             : "http://www.thehindubusinessline.com/opinion/?service=rss",
                "businessinsider"   : "http://www.businessinsider.in/rss_ptag_section_feeds.cms?query=indiainsider"
            }
    }

    selectedNewsSection = ''
    if request.method == "GET":
        error = None
        # Render just the template when method is "GET"
        return render_template ( "hotNews.html", rssUrlList = rssUrlList  )

    if request.method == "POST":

        event = { "newsSection" : request.form["newsSection"] }
        #event = { "newsSection" : "india" }
        selectedNewsSection = request.form["newsSection"]


        def recurseDict(d, newsSection=None):

            pk = newsSection
            for k, v in d.items():
                if isinstance(v, dict):
                    # If any preference is given fetch only
                    if k == pk or pk is None:
                        recurseDict( d[k], k )
                else:
                    # print( "\n{0} : {1} : {2}".format(pk, k, v) )
                    getNews( pk, k, v )

        def getNews(sectiontitle, mediagroup, url):
 
            newsFeed = {}
            articles = {}
            newsitems = []
            if 'cutOffTime' in event:

                cutOffTime = int(event['cutOffTime'])
            else:
                cutOffTime = 50000

            try:
                feed = feedparser.parse(url)
                if feed:
                    for entry in feed['entries']:

                        newsTxt = ''

                        last_updated = time.mktime( entry['published_parsed'] )
                        currLocalTime = time.mktime(time.localtime())

                        publishedTime = str( entry['published_parsed'][3] ) + " hours ago."

                        # Check if the articles are lesser than a given time period
                        if ( currLocalTime - last_updated ) < cutOffTime:
                            if ( mediagroup == "googlenews" ) or ( mediagroup == "businessinsider" ):
                                newsTxt = entry['title_detail']['value']
                            elif ( mediagroup == "economictimes" ):
                                newsTxt = entry['title']
                            else:
                                newsTxt = entry['summary_detail']['value']

                        if newsTxt:
                            newsitems.append( newsTxt + " , Reported at around " + publishedTime  )

                    if not newsitems:
                        newsitems.append( "Pfttt!! Nothing new since the last " \
                            + str( cutOffTime / 3600) + " hours."  )

                    articles[ 'newsitems' ] = newsitems
                    articles[ 'sectiontitle' ] = sectiontitle
                    articles[ 'mediagroup' ] = mediagroup

            except Exception as e:
                newsitems.append("Error : " + str(e))
                articles[ 'newsitems' ] = newsitems
                articles[ 'sectiontitle' ] = sectiontitle
                articles[ 'mediagroup' ] = mediagroup
            collateNews ( articles )
            return

        def collateNews( newsFeed ):


            tempDict = {}
            tempDict[ newsFeed['mediagroup'] ] = newsFeed[ 'newsitems' ]

            if newsFeed['sectiontitle'] in collatedNews:
                # collatedNews[ newsFeed['sectiontitle'] ][  ].update( newsFeed[ 'newsitems' ] )
                collatedNews[ newsFeed['sectiontitle'] ].update( tempDict )

            # update the section if it is not there already
            else:
                # collatedNews.update ( newsFeed )

                collatedNews[ newsFeed['sectiontitle'] ] = tempDict

        # Lets collect some news
        collatedNews = {}

        if 'newsSection' in event:
            recurseDict( rssUrlList, event['newsSection'] )
        else:
            recurseDict( rssUrlList )

        return render_template( "hotNews.html" , \
                                rssUrlList = rssUrlList, \
                                selectedNewsSection = selectedNewsSection, \
                                result = collatedNews \
                            )

if __name__ == "__main__":
    application.run(debug=True)