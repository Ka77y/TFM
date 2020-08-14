import json
from flask import Flask, request, abort
import sys
sys.path.insert(1, '../')
from training.Main import selectSolutionFeedbackSystem

# implementacion del servicio

app = Flask(__name__)

@app.route('/')
def hello_world():
    return "Hello world"

@app.route('/feedbackRankDocuments', methods=['POST'])
def feedbackRankDocuments():
    print("aquiiiiiiiiiiiiiiiiiiiii vieeeeeeeeeeeeeeeeneeeeeeeeeeeeeeeee \n")
    print(request.get_json())
    data = request.get_json()
    print(data['DocPrincipal'])
    # results_rank = request.args.get('results_rank')
    try:
        data_aux = json.dumps(data)
        selectSolutionFeedbackSystem(data_aux)
        return "OK"
    except Exception as e:
        return "something was wrong :("

if __name__ == '__main__':
    app.run(host='0.0.0.0',
            debug=True,
            port=9200)
