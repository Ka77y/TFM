import requests;
import csv

import sys
sys.path.append('../')

from training import obtainTopics


#SCRIPT que actualiza los niveles de tópicos en los documentos con los tópicos asociados
from training.GeneralFunctions import obtainArrayDocTopics, URI_SEND_NEW_DOCUMENT_TOPICS, postRequestApi

uri_docs_specific_topic = "http://localhost:8983/solr/documents/select?q="
id_usados = []

def topicAsociation(topico_base,topico_asociado,current_topic):
    global id_usados
    request = uri_docs_specific_topic + "" + current_topic + ":" + topico_base + "&rows=1000"
    r = requests.get(request).json()
    json_string = r['response']['docs']
    for doc in json_string:
        #if doc['id'] == 'jrc32004D0768-en':
        if doc['id'] not in id_usados:
            doc_topics = obtainArrayDocTopics(doc)
            try:
                # verifica si el tópico asociado también se encuentra en el documento
                i_doc_topic = doc_topics.index(str(topico_asociado))
                doc[current_topic] = doc[current_topic] + " " + str(topico_asociado)
                # recupera todos los tópicos del documento en un array
                all_doc_topics = obtainTopics.obtainDocumentTopics(doc['txt_t'], 0)
                x = i_doc_topic
                while x < len(doc_topics):
                    doc_topics[x] = all_doc_topics[x + 1];
                    topic_aux = "topics" + str(x) + "_t"
                    doc[topic_aux] = str(doc_topics[x])
                    x = x + 1
                    doc
            except:
                doc[current_topic] = doc[current_topic] + " " + str(topico_asociado)
            postRequestApi(URI_SEND_NEW_DOCUMENT_TOPICS, [doc])
            # postRequestApi(URI_SEND_NEW_DOCUMENT_TOPICS, [doc_backup])
            id_usados.append(doc['id'])

def readCSVFile():
    global id_usados
    DOCS = []
    line_count = 0
    a=0
    with open('rules_tender_new_new.csv') as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        for row in csv_reader:
            if line_count == 0:
                line_count = 1
            else:
                while a <=2:
                    id_usados = []
                    current_topic = "topics"+str(a)+"_t"
                    # asocia el primer tópico con el segundo, de la regla
                    topicAsociation(row[3],row[5],current_topic)
                    # asocia el segundo tópico con el primero, de la regla
                    topicAsociation(row[5], row[3], current_topic)
                    a = a+1
                a = 0

if __name__ == '__main__':
    print(readCSVFile())