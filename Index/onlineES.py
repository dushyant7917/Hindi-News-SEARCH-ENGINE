import os, base64, re, logging
from elasticsearch import Elasticsearch

# Log transport details (optional):
logging.basicConfig(level=logging.INFO)

# Parse the auth and host from env:
bonsai = "https://t9hmi71e5i:knf4qmzmyx@hsse-458039054.ap-southeast-2.bonsaisearch.net"
auth = re.search('https\:\/\/(.*)\@', bonsai).group(1).split(':')
host = bonsai.replace('https://%s:%s@' % (auth[0], auth[1]), '')

# Connect to cluster over SSL using auth for best security:
es_header = [{
  'host': host,
  'port': 443,
  'use_ssl': True,
  'http_auth': (auth[0],auth[1])
}]

# Instantiate the new Elasticsearch connection:
es = Elasticsearch(es_header)

# Verify that Python can talk to Bonsai (optional):
es.ping()

################################################################################################
print("\n\nIndexing data...\n\n")

import pymongo
from pymongo import MongoClient

client = MongoClient('localhost:27017')
db = client.Hindi_News

l = db.News.find()

count = 0
for item in l:
    if count > 2942:
        es.index('hsse', 'doc', {'url': item['url'],
                                      'title': item['title'],
                                      'summary': item['summary'],
                                      'description': item['description'],
                                      'keywords': item['keywords'],
                                      'date_time': item['date_time'],
                                      'image_url': item['image_url']
                                     })
    count = count + 1
    print count
