import pprint

import pymongo
from pymongo import MongoClient

from pyelasticsearch import ElasticSearch
#es = ElasticSearch('http://localhost:9200/')
es = ElasticSearch("Elasticsearch URI")


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

es.bulk((es.index_op(doc) for doc in ll), index='test-index2', doc_type='doc')
