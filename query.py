from elasticsearch import Elasticsearch
import pprint

es = Elasticsearch()

ll = []

def show_results(qrry):
    res = es.search(index="test-index3", doc_type="doc", body={"query":{"query_string":{"query":qrry}}})
    print("%d documents found" % res['hits']['total'])
    for doc in res['hits']['hits']:
        if doc['_source']['url'] not in ll:
            ll.append(doc['_source']['url'])
            pprint.pprint(doc['_source']['data']['title'])
            pprint.pprint(doc['_source']['url'])
            print("\n")
        else:
            continue


query = str(raw_input("Enter your query:"))
show_results(query)
