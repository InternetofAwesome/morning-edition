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
import xmltodict
#                                                       ** (refer to id=episode-core)
# full_show = '/html/body/main/div[2]/section/div[2]/div/div[2]/b/@data-play-all'
full_show = '//*[@id="full-show"]/b/@data-play-all'

# Get day of week
dow=datetime.datetime.now(pytz.timezone('US/Pacific')).weekday() 

# Archive URL for getting links to a given day's programs:
if(dow == 5): #saturday
	archive_url='https://www.npr.org/programs/weekend-edition-saturday'
elif(dow == 6): #sunday
	archive_url='https://www.npr.org/programs/weekend-edition-sunday'
else:
	archive_url='https://www.npr.org/programs/morning-edition'
	# archive_url='https://www.npr.org/programs/morning-edition/2023/01/13/1148968551/morning-edition-for-january-13-2023?showDate=2023-01-13'

def makefeed(eps):
	fg = FeedGenerator()
	fg.title('NPR Morning Edition')
	fg.author( {'name':'NPR'} )
	fg.link( href='https://www.npr.org/programs/morning-edition/', rel='alternate' )
	fg.logo('https://cdn.shopify.com/s/files/1/0877/5762/products/Podcast_Stickers_ME_1024x1024.jpg')
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

def lambda_handler(event, context):

	article_data = []
	pageContent=requests.get(archive_url)
	# print(pageContent.content)
	tree = html.fromstring(pageContent.content)
	eps = tree.xpath(full_show)[0]
	# print(etree.tostring(eps))
	eps_json = json.loads(eps)
	# parsed = xmltodict.parse(etree.tostring(eps))
	# eps_json = json.loads(json.dumps(parsed))

	print(eps_json)

	for e in eps_json['audioData']:
			a = {}
			a['title'] = e['title']
			a['url'] = e['audioUrl']
			if('me_hr' in a['url']):
				a['date'] = pytz.utc.localize(parser.parse("06:00"))
			else:
				a['date'] = pytz.utc.localize(parser.parse("05:00"))
			article_data.append(a);
	feed = makefeed(article_data)

	return feed
