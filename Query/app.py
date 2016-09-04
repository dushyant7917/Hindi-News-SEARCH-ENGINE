from flask import Flask
from flask import request
from flask import render_template
from elasticsearch import Elasticsearch

app = Flask(__name__)

@app.route('/')
def my_form():
    return render_template("page.html")

@app.route('/', methods=['POST'])
def my_form_post():

    text = request.form['text']
    print text
    es = Elasticsearch()
    results = es.search(index="test-index3", doc_type="doc", body={"query":{"query_string":{"query":text}}})
    return render_template("results.html", res=results)


if __name__ == '__main__':
    app.run(debug='True')
