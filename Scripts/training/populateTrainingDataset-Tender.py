import requests
import csv
import json

url = 'http://localhost:8081/documents'
lista = []

with open('documents1.csv') as f:
    for linea in f:
      myobj={
            "contactEmail": "nodin55298@laklica.com",
            "dataSink": {
              "format": "SOLR_CORE",
              "url": "http://librairy-repo:8983/solr/documents"
            },
            "dataSource": {
              "name":"tbfy",
              "dataFields": {
                "id": "id",
                "name": "name_s",
                "labels": [
                  "labels_t"
                ],
                "text": [
                  "txt_t"
                ]
              },
              "filter": "id:"+linea,
              "format": "SOLR_CORE",
              "offset": 0,
              "size": -1,
              "url": "http://librairy.linkeddata.es/solr/tbfy"
            }
          }
      headers = {'content-type': 'application/json'}
      x = requests.post(url, data=json.dumps(myobj), auth = ('demo', '2019'), headers=headers)

    print(x.text)