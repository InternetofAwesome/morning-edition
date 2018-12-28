import json
from botocore.vendored import requests
import lxml
from lxml import html
from lxml import etree
from feedgen.feed import FeedGenerator

# article top level branch
articles='//*[@id="story-list"]/article[@class="rundown-segment"]/article[@class="bucketwrap resaudio"]/div[@class="audio-module"]'

#things I am interested in
title='h4[@class="audio-module-title"]'
mp3_url='div[@class="audio-module-tools"]/ul[@class="audio-module-more-tools"]/li[@class="audio-tool audio-tool-download"]/a/@href'
length='div[@class="audio-module-controls-wrap"]/div[@class="audio-module-controls"]/time'

# Main article URL, will be replaced
article_list_url="https://www.npr.org/programs/morning-edition/2018/12/17/677285137?showDate=2018-12-17"

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
	return fg.rss_str(pretty=True)


def lambda_handler(event, context):

	# Get the HTML and parse it
	pageContent=requests.get(article_list_url)
	tree = html.fromstring(pageContent.content)

	# eps = xd.parse(tree.xpath('//*[@id="story-list"]'))
	# print eps

	# get a top level part of the entire html tree for the episodes
	eps = tree.xpath(articles)

	#array to keep article data in
	article_data = []

	for f in eps:
		a = {}
		a['title'] = f.xpath(title)[0].text
		a['url'] = f.xpath(mp3_url)[0]
		if('hr1' in a['url']):
			article_data.insert(0, a)
		else:
			article_data.append(a);
	feed = makefeed(article_data)
	# print "**************************************************************************"
	# print "FEED", feed
	return feed
	# return {
 #        'statusCode': 200,
 #        # 'body': json.dumps(article_data)
 #        'body': feed
 #    }