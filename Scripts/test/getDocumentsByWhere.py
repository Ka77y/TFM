import requests

url = 'http://localhost:8081/documents'
DOCS = []

def use_response(doc):
    try:
        a = doc['topics2_t']
        return doc
    except:
        doc['topics2_t'] = "0"
        return doc

# función que obtiene los documentos que contengan dichos tópicos
def getDocuments(row):

    try:
        query = "topics0_t:" + row[3] + " OR topics1_t:" + row[3] + " OR topics1=2_t:" + row[
            3] + " OR topics0_t:" + row[5] + " OR topics1_t:" + row[5] + " OR topics2_t:" + row[
                    5]+"&rows=1000"
        URI_IDS = "http://localhost:8983/solr/documents/select?q=" + query
        request = URI_IDS
        csv_to_save = ""
        r = requests.get(request).json()
        DOCS[:] = r['response']['docs']
        return DOCS
        # for doc in r['response']['docs']:
        #     doc_c = use_response(doc)
            # csv_to_save = doc_c['id'] + "," + doc_c['topics0_t'] + "," + doc_c[
            #     'topics1_t'] + "," + doc_c['topics2_t']
            # file = open('tr_dataset_id.csv', 'a')
            # file.write(csv_to_save + '\n')
            # file.close()
    except:
        pass
