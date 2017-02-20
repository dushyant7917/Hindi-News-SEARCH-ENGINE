import os, base64, re, logging
from elasticsearch import Elasticsearch
import pymongo
from pymongo import MongoClient

client = MongoClient('localhost:27017')
db = client.Hindi_News

l = db.News.find()

ll = []

for item in l:
    ll.append({'url': item['url'],
               'title': item['title'],
               'summary': item['summary'],
               'description': item['description'],
               'keywords': item['keywords'],
               'date_time': item['date_time'],
               'image_url': item['image_url']
              })

# Log transport details (optional):
logging.basicConfig(level=logging.INFO)

tracer = logging.getLogger('elasticsearch.trace')
tracer.setLevel(logging.INFO)
tracer.addHandler(logging.FileHandler('es_trace.log'))


# Parse the auth and host from env:
bonsai = 'https://2n9hqiyq9q:24xxaxc26w@sandbox-cluster-8120769645.ap-southeast-2.bonsaisearch.net'
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

es.indices.create(index='test-index', ignore=400)
#es.indices.delete(index='test-index', ignore=[400, 404])

num=1
for doc in ll:
    res = es.index(index="test-index", doc_type='text', id=num, body=doc)
    num = num + 1
