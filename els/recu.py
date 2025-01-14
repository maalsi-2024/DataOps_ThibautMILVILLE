#! /usr/bin/python
from elasticsearch import Elasticsearch
import json
import warnings

warnings.filterwarnings("ignore")
# Connexion au cluster
client = Elasticsearch(hosts = "http://@localhost:9200")

query = {
 "query": {
 "match_all": {}
 }
}
response = client.search(index="bitcoin-price", body=query)
# Sauvegarde de la requête et la réponse dans un fichier json
with open("./{}.json".format("_response"), "w") as f:
 json.dump(dict(response), f, indent=2)
with open("./{}.json".format("_request"), "w") as f:
 json.dump(query, f, indent=2)
