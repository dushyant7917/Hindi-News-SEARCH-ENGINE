import os, base64, re, logging
from elasticsearch import Elasticsearch

# Log transport details (optional):
logging.basicConfig(level=logging.INFO)

print("\n\nIndexing data...\n\n")

import pymongo
from pymongo import MongoClient

client = MongoClient('localhost:27017')
db = client.Hindi_News

l = db.News.find()

total = db.News.count()
count = 0
prv = -1

while count<total:
    try:
        # Instantiate the new Elasticsearch connection
        es = Elasticsearch("AWS Elasticsearch cluster API Endpoint")
        count = 0
        for item in xrange(0,total):
            if count > prv:
                prv = count

                es.index('hn', 'doc', {'url': l[item]['url'],
                                              'title': l[item]['title'],
                                              'summary': l[item]['summary'],
                                              'description': l[item]['description'],
                                              'keywords': l[item]['keywords'],
                                              'date_time': l[item]['date_time'],
                                              'image_url': l[item]['image_url']
                                             })

                count = count + 1
                print count, item+1
            else:
                count = count + 1

    except Exception as e:
        print(str(e))
