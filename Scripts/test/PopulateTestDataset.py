import requests
import csv
import json

url = 'http://localhost:8081/documents'
lista = []

f = open('C:/Users/Katherine Vivanco/PycharmProjects/untitled2/tr_dataset_id_correct.txt').readlines()
lista = f[0].split(" ")

for row in lista:

  myobj={
        "contactEmail": "iqiwicep-7962@yopmail.com",
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
          "filter": "id:"+row+" && source_s:jrc && lang_s:en" ,
          "format": "SOLR_CORE",
          "offset": 0,
          "size": -1,
          "url": "http://librairy.linkeddata.es/solr/tbfy"
        }
      }
  headers = {'content-type': 'application/json'}
  x = requests.post(url, data=json.dumps(myobj), auth = ('demo', '2019'), headers=headers)

print(x.text)