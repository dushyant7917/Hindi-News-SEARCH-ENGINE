import pprint

import pymongo
from pymongo import MongoClient

from pyelasticsearch import ElasticSearch
es = ElasticSearch('http://localhost:9200/')

client = MongoClient('localhost:27017')
db = client.Hindi_News

l = db.News.find()

for item in l:
    es.index('test-index', 'doc', {'url': item['url'],
                                  'title': item['title'],
                                  'summary': item['summary'],
                                  'description': item['description'],
                                  'keywords': item['keywords'],
                                  'date_time': item['date_time'], 
                                  'image_url': item['image_url']
                                 })
                                  




