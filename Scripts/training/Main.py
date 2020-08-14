import json
from FiRankTestDataset import getDocumentInformationApi
from training.Algorithm1 import relevanceFirstTopicSolution
from training.Algorithm2 import relevanceSecondTopicSolution
from training.GeneralFunctions import readJsonFile, results_rank_feedback, getDocumentListInformation

PRINCIPAL_DOC = {}
LIST_DOCS_HIGH = []

def selectSolution():
    global PRINCIPAL_DOC
    global FOCUS_DOC_SOLUTION
    FOCUS_DOC_SOLUTION = 0
    data_info = json.dumps(readJsonFile(results_rank_feedback));
    data = json.loads(data_info)
    ranking_model = data['Model'];
    PRINCIPAL_DOC = getDocumentInformationApi(data['DocPrincipal'])[0].copy();

    if ranking_model == 'relevance':
        defineRelevanceModelSolution(data['Rank']);
    if ranking_model == 'position':
        defineRelevanceModelSolution(data['Rank']);

def selectSolutionFeedbackSystem(results_rank_feedback):
    global PRINCIPAL_DOC
    global FOCUS_DOC_SOLUTION
    FOCUS_DOC_SOLUTION = 0
    data_info = results_rank_feedback
    data = json.loads(data_info)
    ranking_model = data['Model'];
    PRINCIPAL_DOC = getDocumentInformationApi(data['DocPrincipal'])[0].copy();

    if ranking_model == 'relevance':
        defineRelevanceModelSolution(data['Rank']);
    if ranking_model == 'position':
        defineRelevanceModelSolution(data['Rank']);

def defineRelevanceModelSolution(data):
    ID_RANK_1 = []
    for documentsRanked in range(len(data)):
        if str(data[documentsRanked]['rank']) == '1':
            ID_RANK_1.append(data[documentsRanked]['id'])
        # elif str(data[documentsRanked]['rank']) == '2':
        #     ID_RANK_2.append(data[documentsRanked]['id'])
        # elif str(data[documentsRanked]['rank']) == '3':
        #     ID_RANK_3.append(data[documentsRanked]['id'])
    if len(ID_RANK_1)>0:
        LIST_DOCS_HIGH[:] = getDocumentListInformation(ID_RANK_1)
        print("lista documentos high", LIST_DOCS_HIGH[:])
        relevanceFirstTopicSolution(PRINCIPAL_DOC, LIST_DOCS_HIGH)
        relevanceSecondTopicSolution(PRINCIPAL_DOC, LIST_DOCS_HIGH)