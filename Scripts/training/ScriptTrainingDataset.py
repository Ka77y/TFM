import csv
import json

from training.Main import selectSolution

with open('pairs_en.csv') as csv_file:
    csv_reader = csv.reader(csv_file, delimiter=',')

    line_count = 0
    main_document_id = ""
    main_document_comparisons = []
    all_documents_ranking = []
    rank_list = []

    for row in csv_reader:
        if line_count == 0:
            main_document_id = row[0]
            line_count = 1
        rank = 1 if row[3] == 'HIGH' else 2 if row[3] == 'MEDIUM' else 3 if row[3] == 'LOW' else 0
        if row[0] == main_document_id:
            main_document_comparisons.append(row[1])
            rank_item = {"id": row[1], "rank": rank}
            rank_list.append(rank_item)
        else:
            json_rank_training = {"Model": "relevance", "DocPrincipal": main_document_id, "Rank": rank_list}
            all_documents_ranking.append(json_rank_training)
            jsonString = json.dumps(json_rank_training)
            with open("results_rank_test.json", 'w') as fileJSON:
                fileJSON.write(jsonString)
            fileJSON.close()
            selectSolution()
            main_document_id = row[0]
            rank_list = []
            main_document_comparisons.append(row[1])
            rank_item = {"id": row[1], "rank": rank}
            rank_list.append(rank_item)


    file1 = open("../all_documents_ranking_all_en.txt", "w")  # write mode
    file1.write(str(all_documents_ranking))
    file1.close()
