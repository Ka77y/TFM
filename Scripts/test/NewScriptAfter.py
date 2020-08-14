import json
import requests;
import csv
from test.ObtainTestDataset import use_response_2, use_response_1
from test.getDocumentsByWhere import getDocuments

rank_body_template = "rank_template.json"
URI_DOCUMENT_RANK = 'http://localhost:8081/ranks'
URI_OBTAIN_DOCUMENT_INFORMATION = 'http://localhost:8983/solr/documents/select?q=id:'

def getDocumentInformationApi(id):
    id_aux = id.replace("#","%23")
    request = URI_OBTAIN_DOCUMENT_INFORMATION + "\""+id_aux+"\""
    r = requests.get(request).json()
    json_string = r['response']['docs']

    return json_string


def readJsonFile(jsonFileName):
    with open(jsonFileName, 'r') as json_file:
        aux = json_file.read()
        data = json.loads(aux)
        return data

# envía una petición post
def postRequestApi(uri, body):
    headers = {'content-type': 'application/json'}
    r = requests.post(uri, data=json.dumps(body), auth=('demo', '2019'), headers=headers)
    return r

def getDocumentRank(body):
    new_rank_docs_id = []
    r = postRequestApi(URI_DOCUMENT_RANK, body).content
    if r != b'':
        new_rank_docs = json.loads(r.decode('ISO-8859-1'))['response']['docs']
        for doc in new_rank_docs:
            new_rank_docs_id.append(doc['id'])

    return new_rank_docs_id

def readCSVFile():
    DOCS = []
    line_count = 0
    with open('rules_tender_new_new.csv') as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        for row in csv_reader:
            if line_count == 0:
                line_count = 1
            else:
                DOCS[:] = getDocuments(row)
                ifPutRule(DOCS, row)

def ifPutRule():
    global precision_after
    global precision_before
    precision_after = 0
    precision_before = 0
    line_count = 0
    used_ids = []
    try:
        with open('log_precision_results_before_v1.csv') as csv_file:
            csv_reader = csv.reader(csv_file, delimiter=',')
            for row in csv_reader:
                if line_count == 0:
                    line_count = 1
                else:
                    doc = getDocumentInformationApi(row[0])[0]
                    rule = row[3]
                    #current_doc_backup = getDocumentInformationApi(doc['id'])[0]
                    current_doc = doc.copy()
                    precision_after = matchTopics(current_doc, "log_test_after_v1.csv", rule, int(row[4]))
                    csv_precision = ','.join(row) + "," + current_doc['id'] + "," + precision_after.split(";")[0] + "," + ''.join(precision_after.split(";")[1]) + "," + rule + "," + row[4]
                    file = open("log_precision_results_after_v1.csv", 'a')
                    file.write("\n" + csv_precision)
                    file.close()
    except:
        pass

def matchTopics(main_doc, name_file, rule, number_precision_eval):
    list_count_match_labels = []
    csv_final = ""
    relevant_documents_retrieved = 0
    data = readJsonFile(rank_body_template)
    data['reference']['document']['id'] = main_doc['id']
    data['dataSource']['cache'] = str(data['dataSource']['cache']).lower()
    data['size'] = (number_precision_eval-1)
    document_rank = getDocumentRank(data)
    labels_main_doc = list(main_doc['labels_t'].split(" "))

    if len(document_rank) == 0:
        main_doc_aux_1 = use_response_1(main_doc)
        main_doc_aux = use_response_2(main_doc_aux_1)
        csv_info = "\n" + main_doc_aux['id'] + "," + main_doc_aux['topics0_t'] + "," + main_doc_aux['topics1_t'] + "," + \
                   main_doc_aux['topics2_t'] + "," + \
                   ' '.join(labels_main_doc) + ",null,null,null,null,null,null,"+' '.join(rule)+",0"
        csv_final = csv_info
    else:
        for doc_rank in document_rank:
            print("entró")
            try:
                print("entró aquí")
                main_doc_aux_1 = use_response_1(main_doc)
                main_doc_aux = use_response_2(main_doc_aux_1)
                doc_ranking_1 = use_response_1(getDocumentInformationApi(doc_rank)[0])
                doc_ranking_aux = use_response_2(doc_ranking_1)

                labels_ranking_doc = list(doc_ranking_aux['labels_t'].split(" "))
                match_labels = [val for val in labels_main_doc if val in labels_ranking_doc]
                csv_info = main_doc_aux['id']+","+main_doc_aux['topics0_t']+","+main_doc_aux['topics1_t']+","+main_doc_aux['topics2_t']+","+\
                           ' '.join(labels_main_doc)+","+doc_ranking_aux['id']+","+doc_ranking_aux['topics0_t']+","+\
                           doc_ranking_aux['topics1_t']+","+doc_ranking_aux['topics2_t']+","+' '.join(labels_ranking_doc)+","+\
                           ("null" if len(match_labels) == 0 else ' '.join(match_labels))+","+' '.join(rule)+','+str(len(match_labels))
                csv_final = csv_final + "\n" + csv_info
                if len(match_labels) != 0:
                    list_count_match_labels.append(len(match_labels))
                    relevant_documents_retrieved = relevant_documents_retrieved + 1
                else:
                    list_count_match_labels.append(0)
                    relevant_documents_retrieved = relevant_documents_retrieved
            except:
                pass
    file = open(name_file, 'a')
    file.write(csv_final)
    file.close()

    # if relevant_documents_retrieved != 0:
    precision = relevant_documents_retrieved/len(document_rank)
    match_labels_aux = " ".join([str(_) for _ in list_count_match_labels])
    return str(precision) + ";" + match_labels_aux
    # else:
    #     return 0

if __name__ == '__main__':
    print(ifPutRule())