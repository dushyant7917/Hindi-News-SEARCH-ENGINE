from flask import Flask
from flask import request
from flask import render_template, redirect, url_for
from elasticsearch import Elasticsearch
import wikiAPI

app = Flask(__name__)


@app.route('/',methods = ['GET','POST'])
def index():
    if request.method == 'GET':
        return render_template("home.html")
    else:
        query = request.form['text']
        return redirect(url_for('wikipedia', query = query))

@app.route('/search/heritage/?=<query>', methods = ['GET', 'POST'])
def wikipedia(query):
    if request.method == 'GET':
        result = {}
        result['title'], result['url'], result['images'], result['summary'] = wikiAPI.wiki(query)
        return render_template('wikiResults.html', results = result, search_text = query)
    else:
        return "Some Error Occured!"


@app.route('/search/?=<query>', methods = ['GET', 'POST'])
def search(query):
    if request.method == 'GET':
        es = Elasticsearch()
        results = es.search(index="test-index3", doc_type="doc", body={"size":18,"query":{"query_string":{"query":query}}})
        return render_template('results.html', results = results, search_text = query)
    else:
        return "Some Error Occured!"


if __name__ == '__main__':
    app.run( host='0.0.0.0', port=int('5000'), debug = True )
