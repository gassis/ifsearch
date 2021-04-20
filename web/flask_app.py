from flask import Flask, render_template, request, g
from elasticsearch import Elasticsearch
from elasticsearch_dsl import Search
from collections import OrderedDict


class Config(object):
    SECRET_KEY = 'Ven@1n@2602noB0mC0nselh0emJ@t@1'


app = Flask(__name__)
app.config.from_object(Config)

def getindex_month(month):
    meses = ['janeiro', 'fevereiro', 'março', 'abril', 'maio', 'junho', 'julho', 'agosto', 'setembro', 'outubro', 'novembro', 'dezembro']
    idx_m = 0
    for idx, val in enumerate(meses, 1):
        if val == month.lower():
            idx_m = idx
            break
    return idx_m


def get_es():
    if 'es' not in g:
        client = Elasticsearch('http://elasticsearch:9200')
        s = Search(using=client, index="docsearch")
        g.es = s
    return g.es


def getmulti(terms):
    s = get_es()
    s = s.query("match", data=terms.strip())

    s = s[:1000]
    es_data = s.source(['url', 'year', 'month', 'page'])
    r = s.execute(es_data)
    
    numres = r.hits.total.value

    results = {}
    i = 0
    for hit in r:
        page = hit.page + 1
        results[r['hits']['hits'][i]['_score']] = [hit.year, hit.month, hit.url, page]
        i += 1
    sorted_results = OrderedDict(sorted(results.items(), reverse=True))
        
    return i, sorted_results


def getexact(terms):
    s = get_es()    
    blacklist = ['de', 'do', 'a', 'e', 'o', 'este', 'esta', 'aquele', 'aquela', 'isso', 'disso', 'aquilo', 'neste', 'nesta'] 
    term = terms.split('&')
    if len(term) > 1:
        for i in range(1, len(term)):
            if not term[i].strip() in blacklist:
                s = s.filter('match_phrase', data=term[i].strip())
        terms = term[0].strip()
    
    s = s.query("match_phrase", data=terms.strip())

    s = s[:1000]
    es_data = s.source(['url', 'year', 'month', 'page'])
    r = s.execute(es_data)
    numres = r.hits.total.value
    results = {}
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
    sorted_results = dict(OrderedDict(sorted(results.items(), reverse=True)))
    return numres, sorted_results


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
