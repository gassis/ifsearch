from flask import Flask, render_template, request
from elasticsearch import Elasticsearch
from elasticsearch_dsl import Search


class Config(object):
    SECRET_KEY = 'Ven@1n@2602noB0mC0nselh0emJ@t@1'


app = Flask(__name__)
app.config.from_object(Config)


def getdata(terms):
    client = Elasticsearch('http://elasticsearch:9200')
    s = Search(using=client, index="docsearch")
    term = terms.split('&')
    if len(term) > 1:
        for i in range(1, len(term)):
            s = s.filter('match_phrase', data=term[i].strip())
    s = s.query("match_phrase", data=term[0].strip())
    s = s[:100]
    es_data = s.source(['url', 'year', 'month', 'page'])
    r = s.execute(es_data)
    numres = r.hits.total.value
    results = {}
    final = {}
    for hit in r:
        page = hit.page + 1
        if hit.year not in results:
            results[hit.year] = {}
        if hit.month not in results[hit.year]:
            results[hit.year][hit.month] = {}
        if hit.url not in results[hit.year][hit.month]:
            results[hit.year][hit.month][hit.url] = []
        if page not in results[hit.year][hit.month][hit.url]:
            results[hit.year][hit.month][hit.url].append(page)
    for k in sorted(results, reverse=True):
        final[k] = results[k]
    return numres, final


@app.route('/', methods=['GET', 'POST'])
def index():
    return render_template('index.html')


@app.route('/search', methods=('GET', 'POST'))
def search():
    if request.method == 'POST':
        terms = request.form['search_term']
        n, results = getdata(terms)
        return render_template('results.html', results=results, numres=n, term=terms)


if __name__ == '__main__':
    app.run(host='0.0.0.0')
