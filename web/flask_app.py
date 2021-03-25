from flask import Flask, render_template, request, g
from elasticsearch import Elasticsearch
from elasticsearch_dsl import Search


class Config(object):
    SECRET_KEY = 'Ven@1n@2602noB0mC0nselh0emJ@t@1'


app = Flask(__name__)
app.config.from_object(Config)

def get_es():
    if 'es' not in g:
        client = Elasticsearch('http://elasticsearch:9200')
        s = Search(using=client, index="docsearch")
        g.es = s
    return g.es


def getmulti(terms):
    s = get_es()
    s = s.query("match", data=terms.strip())

    s = s[:500]
    es_data = s.source(['url', 'year', 'month', 'page'])
    r = s.execute(es_data)
    numres = r.hits.total.value
    
    results = []
    i = 0
    for hit in r:
        page = hit.page + 1
        results.append([hit.url, hit.year, hit.month, page])
        i += 1
    
    return numres, results


def getexact(terms):
    s = get_es()
    s = s.query("match_phrase", data=terms.strip())

    s = s[:500]
    es_data = s.source(['url', 'year', 'month', 'page'])
    r = s.execute(es_data)
    numres = r.hits.total.value
    
    results = {}
    final = {}
    i = 0
    for hit in r:
        page = hit.page + 1
        if hit.year not in results:
            results[hit.year] = {}
        if hit.month not in results[hit.year]:
            results[hit.year][hit.month] = {}
        if hit.url not in results[hit.year][hit.month]:
            results[hit.year][hit.month][hit.url] = {}
        if page not in results[hit.year][hit.month][hit.url].keys():
            results[hit.year][hit.month][hit.url][page] = r['hits']['hits'][i]['_score']
        i += 1
            
    for hit in r:
        results[hit.year][hit.month][hit.url] = {k: v for k, v in sorted(results[hit.year][hit.month][hit.url].items(), key=lambda item: item[1], reverse=True)}
    
    for k in sorted(results, reverse=True):
        final[k] = results[k]
    return numres, final


@app.route('/', methods=['GET', 'POST'])
def index():
    return render_template('index.html')


@app.route('/search', methods=('GET', 'POST'))
def searche():
    if request.method == 'POST':
        radio = request.form['radio']
        terms = request.form['search_term']
        if not radio or radio == 'radio1':
            n, results = getexact(terms)
            return render_template('resultse.html', results=results, numres=n, term=terms)            
        elif radio == 'radio2':
            n, results = getmulti(terms)
            return render_template('resultsm.html', results=results, numres=n, term=terms)

        
if __name__ == '__main__':
    app.run(host='0.0.0.0')
