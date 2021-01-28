import json
from elasticsearch import Elasticsearch

def check_if_index_is_present(url):
    response = requests.request("GET", url, data="")
    json_data = json.loads(response.text)
    return json_data
	
def create_index(es, index_name):
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
    url = "http://localhost:9200/docsearch/"
    es.indices.create(index='docsearch', ignore=400)
    if (response.status_code == 200):
        return True
    else:
        return False
            
def install_plugin(client, host, plugin_name):
    payload = {
      "description" : "Extração de texto de documentos PDF",
      "processors" : [
        {
          "attachment" : {
            "field" : "base64"
          }
        }
      ]
    }
    es = Elasticsearch('http://localhost:9200')
    payload = json.dumps(payload)
    es.index(index='_ingest', doc_type='pipeline', id='attachment', body=payload)    
    url = host+"_ingest/pipeline/"+plugin_name
    response = requests.request("PUT", url, data=payload, headers=headers)
    if (response.status_code == 200):
        return True
    else:
        return False
