#segundo algoritmo de asociación de tópicos
from scipy import stats as s
from training import GeneralFunctions as gf

def putTopicWhenNotExists(i, topic, main_doc_response):
    main_doc_topics = gf.obtainArrayDocTopics(main_doc_response)

    #analiza si el tópico no existe en el documento principal
    if topic not in main_doc_topics[0] and topic not in main_doc_topics[1] and topic not in main_doc_topics[2]:
        return main_doc_topics[i]
    else:
        return 0

def relevanceSecondTopicSolution(main_doc_response, LIST_DOCS_HIGH):
    global do_modification
    high_topic_repeated = []
    high_topic_index = []
    topic = []
    high_topics = []
    do_modification = 0

    for doc in LIST_DOCS_HIGH:
        #una lista de todos los tópicos presentes en todos los documentos con relevancia HIGH
        high_topic_repeated.extend([doc['topics0_t'], doc['topics1_t'], doc['topics2_t']]);
        # una lista de todos los tópicos presentes en todos los documentos con relevancia HIGH
        high_topic_index.extend([{'topic': doc['topics0_t'], 'index': 0}, {'topic': doc['topics1_t'], 'index': 1},
                                 {'topic': doc['topics2_t'], 'index': 2}]);

    while len(high_topic_repeated) != 0:
        # escoge el topic más comun, most_common_value, de la lista de topics de los documentos con relevance HIGH
        most_common_value = list(s.mode(high_topic_repeated)[0])[0]
        # crea una lista, topic, de las posiciones en las que se encuentra el tópico (most_common_value)
        topic.append(next(item["index"] for item in high_topic_index if item["topic"] == most_common_value))
        # escoge la posición más común, most_common_index, de la lista topic
        most_common_index = list(s.mode(topic)[0])[0]
        # llama a la función que procesa si existe o no el tópico en el main document
            # retorna 1 si no existe y topic_main_document si existe
            # si no existe, se hace la operación de modificación de tópicos en el main document y retorna el tópico del main document que fue modificado
            # si existe, no hace nada y evalúa la solución con el siguiente tópico más repetido
        val = putTopicWhenNotExists(most_common_index, most_common_value, main_doc_response)
        # crea una lista de los tópicos más repetidos que ya se usaron
        high_topics.append(most_common_value)
        # elimina de la lista de tópicos de documnents con relevance HIGH los tópicos que ya se usaron como
        # most_common_value
        high_topic_repeated = [top for top in high_topic_repeated if top not in high_topics]
        topic[:]=[]

        #se termina la operación cuando ya se ha hecho la modificación de tópicos al main document
        if val != 0:
            gf.createRulesCSV("relevance_2", val, "put", most_common_value)
            break