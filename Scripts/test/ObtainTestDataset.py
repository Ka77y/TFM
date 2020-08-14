import json
import requests;
import csv

DOCS = []
general_docs_list = []
general_topics_list = []

######CLASE QUE OBTIENE LOS IDS PARA EL DATASET QUE SE USARÁ EN LA FASE DE PRUEBAS

#funcion que en el caso de que no exista el tópico 2 en el documento lo añade con un valor de 0
def use_response_2(doc):
    try:
        a = doc['topics2_t']
        return doc
    except:
        doc['topics2_t'] = "0"
        return doc

#funcion que en el caso de que no exista el tópico 1 en el documento lo añade con un valor de 0
def use_response_1(doc):
    try:
        a = doc['topics1_t']
        return doc
    except:
        doc['topics1_t'] = "0"
        return doc

def gettESTDatasetIDs(lista_topicos):
    global general_docs_list
    global general_topics_list

    general_topics_list = general_topics_list + lista_topicos
    new_topic_lista = []

    for topic_aux in lista_topicos:
        if len(list(set(general_docs_list))) > 999:
            break
        else:
            query = "(topics0_t:" + topic_aux + " OR topics1_t:" + topic_aux + " OR topics1=2_t:" + topic_aux + ") AND source_s:jrc AND lang_s:en&rows=10000&start=0"
            URI_IDS = "http://librairy.linkeddata.es/solr/tbfy/select?q=" + query
            request = URI_IDS
            r = requests.get(request).json()
            DOCS[:] = r['response']['docs']
            for doc in r['response']['docs']:
                if len(list(set(general_docs_list))) > 999:
                    break
                else:
                    try:
                        print(doc['id'] + " len " + str(len(list(set(general_docs_list)))))
                        doc_d = use_response_2(doc)
                        doc_c = use_response_1(doc_d)
                        if doc_c['topics0_t'] not in general_topics_list:
                            new_topic_lista.append(doc_c['topics0_t'])
                        if doc_c['topics1_t'] not in general_topics_list:
                            new_topic_lista.append(doc_c['topics1_t'])
                        if doc_c['topics2_t'] not in general_topics_list:
                            new_topic_lista.append(doc_c['topics2_t'])
                        if len(list(set(general_docs_list))) < 1000:
                            general_docs_list.append(doc_c['id'])
                    except:
                        pass
    if len(list(set(general_docs_list))) < 1000:
        gettESTDatasetIDs(list(set(new_topic_lista)))
    else:
        file1 = open("../tr_dataset_id_correct.txt", "w")  # write mode
        file1.write(str(general_docs_list))
        file1.close()

def csv_element():
    line_count = 0
    with open('rules_tender_new_new.csv') as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        list_topics = []

        for row in csv_reader:
            if line_count == 0:
                line_count = 1
            else:
                try:
                    list_topics.append(row[3])
                    list_topics.append(row[5])
                except:
                    pass

        gettESTDatasetIDs(list(set(list_topics)))

if __name__ == '__main__':
    print(csv_element())


