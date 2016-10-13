from flask import Flask
from flask import request
from flask import render_template, redirect, url_for
from elasticsearch import Elasticsearch

app = Flask(__name__)


@app.route('/',methods=['GET'])
def my_form():
    return render_template("search.html")


@app.route('/', methods=['POST'])
def my_form_post():
    query = request.form['text']
    return redirect(url_for("api_call", text=query))


@app.route('/api/v1.0/search/<string:text>',methods=['GET'])
def api_call(text):
    es = Elasticsearch()
    results = es.search(index="test-index3", doc_type="doc", body={"size":18,"query":{"query_string":{"query":text}}})
    return render_template("results.html", res=results)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int('5000'), debug='True')
