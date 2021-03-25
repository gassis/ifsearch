import requests
import json, time
import errno
from socket import error as socket_error
from elasticsearch import Elasticsearch

def check_if_index_is_present(url):
    response = requests.request("GET", url, data="")
    json_data = json.loads(response.text)
    return json_data


if __name__ == "__main__":
    try:
        time.sleep(5)
        es = Elasticsearch('http://elasticsearch:9200')
        payload = {
            "settings": {
                "number_of_shards": 1,
                "number_of_replicas": 0
            },
            "mappings": {
                "_source": {
                    "excludes": [
                        "base64"
                    ]
                },
                "properties": {
                    "url": {
                        "type": "text",
                        "analyzer": "brazilian"
                    },
                    "page": {
                        "type": "short"
                    },
                    "year": {
                        "type": "integer"
                    },
                    "month": {
                        "type": "text",
                        "analyzer": "brazilian"
                    },
                    "data": {
                        "type": "text",
                        "analyzer": "brazilian",
                        "fields": {
                            "keyword": {
                                "type": "keyword",
                                "ignore_above": 256
                            }
                        }
                    },
                    "attachment": {
                        "type": "object",
                        "properties": {
                            "content": {
                                "type": "text",
                                "analyzer": "brazilian",
                                "copy_to": "data"
                            }
                        }
                    }
                }
            }
        }
        payload = json.dumps(payload)
        headers = {
            'Content-Type': "application/json",
            'cache-control': "no-cache"
        }
        url = "http://elasticsearch:9200/docsearch"
        json_data = check_if_index_is_present(url)
        if (not 'error' in json_data):
            print("-> Existing index: docsearch")
        else:
            response = requests.request("PUT", url, data=payload, headers=headers)
            if (response.status_code == 200):
                print("-> Created a new index: docsearch")
            else:
                print("ERROR: index not created!")
        payload = {
            "description": "Extração de texto de documentos PDF",
            "processors": [
                {
                    "attachment": {
                        "field": "base64"
                    }
                }
            ]
        }
        payload = json.dumps(payload)
        es.index(index='_ingest', doc_type='pipeline', id='attachment', body=payload)
        url = "http://elasticsearch:9200/_ingest/pipeline/docsearch-extract-pdf"
        response = requests.request("PUT", url, data=payload, headers=headers)
        if (response.status_code == 200):
            print("-> Ingestion pipeline created!")
        else:
            print("ERROR: ingestion pipeline not created!")
        es.close()
    except requests.exceptions.ConnectionError as e:
        print("## indexing ERROR 1: ##", e)
    except socket_error as e:
        print("## indexing ERROR 2: ##", e)
