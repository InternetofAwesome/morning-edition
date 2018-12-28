import json
from botocore.vendored import requests
import lxml
from lxml import html
from lxml import etree
from dateutil import parser
import datetime

# article top level branch
articles='//*[@id="story-list"]/article[@class="rundown-segment"]/article[@class="bucketwrap resaudio"]/div[@class="audio-module"]'

#things I am interested in
title='h4[@class="audio-module-title"]'
mp3_url='div[@class="audio-module-tools"]/ul[@class="audio-module-more-tools"]/li[@class="audio-tool audio-tool-download"]/a/@href'
length='div[@class="audio-module-controls-wrap"]/div[@class="audio-module-controls"]/time'

# Want to sort the funny bits at the beginning to the top. Normally less than 40s
funny_tdiff=parser.parse("00:00:40")

# Main article URL, will be replaced
article_list_url="https://www.npr.org/programs/morning-edition/2018/12/17/677285137?showDate=2018-12-17"

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
		a['time'] = f.xpath(length)[0].text
		dt = parser.parse("00:" + a['time'])
		if(dt < funny_tdiff):
			article_data.insert(0, a)
		else:
			article_data.append(a);
	return {
        'statusCode': 200,
        'body': json.dumps(article_data)
    }