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
# es.ping()

##################################################################################################################################
from flask import Flask
from flask import request
from flask import render_template, redirect, url_for
from elasticsearch import Elasticsearch


app = Flask(__name__)


@app.route('/',methods = ['GET','POST'])
def index():
    if request.method == 'GET':
        return render_template("home.html")
    else:
        query = request.form['text']
        return redirect(url_for('search', query = query))


@app.route('/search/?=<query>', methods = ['GET', 'POST'])
def search(query):
    if request.method == 'GET':
        results = es.search(index="hsse", doc_type="doc", body={"size":18,"query":{"query_string":{"query":query}}})
        return render_template('search_results.html', results = results, search_text = query)
    else:
        return "Some Error Occured!"


if __name__ == '__main__':
    app.run( host='0.0.0.0', port=int('5000'), debug = True )
