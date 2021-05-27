from flask import request, Blueprint
import json
from apps.services import outServices
api = Blueprint('api', __name__, url_prefix='/api/entry')

@api.route('/startAssignTask', methods=['GET', 'POST'])
def api_startAssignTask():
    if request.method == 'POST':
        data = request.get_data()
        data = json.loads(data)
        print(data)
        if 'description' not in data.keys():
            data['description'] = ''
            print('description为空')
        return outServices.startAssignTask(data['taskId'], data['taskName'], data['description'], data['reward'], data['field'], data['document'])
    return 'you see this /startAssignTask in get!'

@api.route('/resultNotice', methods=['POST'])
def resultNotice():
    if request.method == 'POST':
        data = request.get_data()
        data = json.loads(data)
        print(data)
        return outServices.resultNotice(data)

@api.route('/startTask', methods=['POST'])
def startTask():
    if request.method == 'POST':
        data = request.get_data()
        data = json.loads(data)
        print(data)
        return outServices.startTask(data['taskId'], data['resultFileType'], data['member'])

@api.route('/getRate', methods=['POST'])
def getRate():
    if request.method == 'POST':
        data = request.get_data()
        data = json.loads(data)
        print(data)
        return outServices.getRate(data['taskId'])

@api.route('/subTask', methods=['POST'])
def subTask():
    if request.method == 'POST':
        data = request.get_data()
        data = json.loads(data)
        print(data)
        return outServices.subTask(data['taskId'], data['token'])

@api.route('/initSubjectAssignment', methods=['POST'])
def initSubjectAssignment():
    if request.method == 'POST':
        data = request.get_data()
        data = json.loads(data)
        outServices.initTaskItems(data)
        print(data)
        return outServices.pact_response_json_data(True, "0", "", None)

@api.route('/changeTask', methods=['POST'])
def changeTask():
    if request.method == 'POST':
        data = request.get_data()
        data = json.loads(data)
        print(data)
        return outServices.changeTask(data["taskId"], data["DetailsTaskId"], data["userID"], data["userName"])

if __name__ == '__main__':
    pass
    #apps.run(debug=True)
    #apps.run(host="0.0.0.0", port=8081, debug=True)