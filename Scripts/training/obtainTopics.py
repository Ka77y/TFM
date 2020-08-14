import json
import requests;

URI_TOPICS = 'http://librairy.linkeddata.es/jrc-en-model/topics'
URI_INFERENCES = 'https://librairy.linkeddata.es/jrc-en-model/inferences';
INFERENCES = []
TOPICS = []


def getDocumentInferences(document_text):
    body = {"text": "" + document_text + "", "topics": "true"}
    headers = {'content-type': 'application/json'}
    r = requests.post(URI_INFERENCES, data=json.dumps(body), auth=('demo', '2019'), headers=headers).content
    input_array = json.loads(r.decode('utf-8'))['vector']
    INFERENCES[:] = input_array


def getVocabTopics():
    request = URI_TOPICS
    r = requests.get(request).json()
    TOPICS[:] = r


def obtainDocumentTopics(text, library_executed):
    max_value_inferences = []
    getDocumentInferences(text)
    if (library_executed == 0):
        getVocabTopics()
    maxs = []
    indices = []
    topicsDocument = []
    count = 0
    while len(maxs) < len(INFERENCES) and count < 10:
        index = 0
        max_val = 0
        for i, val in enumerate(INFERENCES):
            value = float(val)
            if i not in indices:
                if value >= max_val:
                    index = i
                    max_val = value
        count += 1
        maxs.append(max_val)
        indices.append(index)
        print(max_val)
        print(TOPICS[index]['name'])
        topicsDocument.append(TOPICS[index]['name'])
    return topicsDocument


# print(maxs)
# print(indices)
# print(topicsDocument)

# if __name__ == '__main__':
#     text = 'Commission Regulation (EC) No 418/2006. of 10 March 2006. amending Regulation (EC) No 343/2006 opening the buying-in of butter in certain Member States for the period 1 March to 31 August 2006. THE COMMISSION OF THE EUROPEAN COMMUNITIES, Having regard to the Treaty establishing the European Community, Having regard to Council Regulation (EC) No 1255/1999 of 17 May 1999 on the common organisation of the market in milk and milk products [1], Having regard to Commission Regulation (EC) No 2771/1999 of 16 December 1999 laying down detailed rules for the application of Council Regulation (EC) No 1255/1999 as regards intervention on the market in butter and cream [2], and in particular Article 2 thereof, Whereas: (1) Commission Regulation (EC) No 343/2006 [3] establishes the list of Member States in which buying-in for butter is open, as provided for in Article 6(1) of Regulation (EC) No 1255/1999. (2) On the basis of most recent communications by Italy, pursuant to Article 8 of Regulation (EC) No 2771/1999, the Commission has observed that butter market prices have been below 92 % of the intervention price for two consecutive weeks. Intervention buying-in should therefore be opened in those Member States. Italy should therefore be added to the list established in Regulation (EC) No 343/2006. (3) Regulation (EC) No 343/2006 should therefore be amended accordingly, HAS ADOPTED THIS REGULATION: Article 1. Article 1 of Regulation (EC) No 343/2006 is replaced by the following text: \'Article 1. Buying-in of butter as provided for in Article 6(1) of Regulation (EC) No 1255/1999 is hereby open in the following Member States: - Germany. - Estonia. - Spain. - France. - Italy. - Ireland. - Latvia. - Netherlands. - Poland. - Portugal. - Finland. - Sweden. - United Kingdom.\'. Article 2. This Regulation shall enter into force on 11 March 2006. This Regulation shall be binding in its entirety and directly applicable in all Member States.'
#     print(obtainDocumentTopics(text, 0))
#     print(INFERENCES)
#     print(TOPICS)
