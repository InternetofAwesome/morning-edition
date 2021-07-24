#!/usr/bin/env python3

import json
import lxml
from lxml import html
from lxml import etree
from feedgen.feed import FeedGenerator
from dateutil import parser
import pytz
import datetime
import requests

# article top level branch
articles='//*[@id="story-list"]/article[@class="rundown-segment"]/article[@class="bucketwrap resaudio"]/div[@class="audio-module"]'

#things I am interested in
title='h4[@class="audio-module-title"]'
mp3_url='div[@class="audio-module-tools"]/ul[@class="audio-module-more-tools"]/li[@class="audio-tool audio-tool-download"]/a/@href'
length='div[@class="audio-module-controls-wrap"]/div[@class="audio-module-controls"]/time'

# Get day of week
dow=datetime.datetime.now(pytz.timezone('US/Pacific')).weekday() 

# Archive URL for getting links to a given day's programs:
if(dow == 5): #saturday
	archive_url='https://www.npr.org/programs/weekend-edition-saturday/archive'
elif(dow == 6): #sunday
	archive_url='https://www.npr.org/programs/weekend-edition-sunday/archive'
else:
	archive_url='https://www.npr.org/programs/morning-edition/archive'

archive_xpath='h2/a/@href'
archive_date='//*[@id="episode-list"]/article'

def makefeed(eps):
	fg = FeedGenerator()
	fg.title('NPR Morning Edition')
	fg.author( {'name':'NPR'} )
	fg.link( href='https://www.npr.org/programs/morning-edition/', rel='alternate' )
	fg.logo('https://media.npr.org/branding/programs/morning-edition/branding_main-f9f25c3b9130b7ea5eba95da872f93cb2fd36e4f.png')
	fg.subtitle('Daily news from NPR')
	fg.link( href='https://ufr96k0yxe.execute-api.us-east-1.amazonaws.com/prod', rel='self' )
	fg.language('en')
	# Add feed episodes
	for e in eps:
		fe = fg.add_entry()
		fe.id(e['url'])
		fe.title(e['title'])
		fe.link(href=e['url'])
		fe.published(e['date'])
	return fg.rss_str(pretty=True)

def get_day_urls():
	pageContent=requests.get(archive_url)
	tree = html.fromstring(pageContent.content)
	dates=tree.xpath(archive_date)
	day_urls = []
	for d in dates:
		obj = {}
		obj['url'] = d.xpath(archive_xpath)[0]
		obj['date'] = d.xpath('@data-episode-date')[0]
		day_urls.append(obj)

	return day_urls


def lambda_handler(event, context):

	#array to keep article data in
	article_data = []
	day_urls = get_day_urls()
	for d in day_urls:
		# Get the HTML and parse it
		pageContent=requests.get(d['url'])
		tree = html.fromstring(pageContent.content)

		# eps = xd.parse(tree.xpath('//*[@id="story-list"]'))
		# print eps

		# get a top level part of the entire html tree for the episodes
		eps = tree.xpath(articles)

		for f in eps:
			a = {}
			a['title'] = f.xpath(title)[0].text
			a['url'] = f.xpath(mp3_url)[0]
			if('me_hr' in a['url']):
				a['date'] = pytz.utc.localize(parser.parse(d['date'] + " 0600"))
			else:
				a['date'] = pytz.utc.localize(parser.parse(d['date'] + " 0500"))
			article_data.append(a);
	feed = makefeed(article_data)

	return feed
