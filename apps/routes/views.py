from flask import request, jsonify, Blueprint
import json
from apps.auth.auth import auth
from apps.services import outServices, inServices
api = Blueprint('api', __name__, url_prefix='/api/entry')
inside_api = Blueprint('inside_api', __name__, url_prefix='/inside_api/entry')

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

@inside_api.route('/assignTask', methods=['GET', 'POST'])
@auth.login_required()
def jumpIntoAssignTask():
    if request.method == 'POST':
        data = request.get_data()
        data = json.loads(data)
        print(data)
        return outServices.jumpIntoAssignTask(data['taskId'])
    return 'you see this /jumpIntoAssignTask in get!'

@inside_api.route('/taskSplit', methods=['POST'])
@auth.login_required
def taskSplit():
    if request.method == 'POST':
        data = request.get_data()
        data = json.loads(data)
        print(data)
        return inServices.taskSplit(data["task_id"], data["subtask"],data["inside_token"])

@inside_api.route('/searchUserId', methods=['GET','POST'])
@auth.login_required
def searchUserId():
    if request.method == 'POST':
        data = request.get_data()
        data = json.loads(data)
        #inServices.searchUserId(data["userId"], data["taskId"])
        print(data)
        return inServices.searchUserId(data["user_id"], data["task_id"])

@inside_api.route('/updateEditItem', methods=['POST'])
@auth.login_required
def updateEditItem():
    if request.method == 'POST':
        data = request.get_data()
        data = json.loads(data)
        print(data)
        return inServices.updateEditItem(data["item_id"], data["original_id"], data["name"],data["relation"] ,data["field"], data["info_box"],data["intro"], data["imageUrl"], data["content"],data["task_id"],data["reference"],data["operation"])

@inside_api.route('/getCheckItem', methods=['POST'])
@auth.login_required
def getCheckItem():
    if request.method == 'POST':
        data = request.get_data()
        data = json.loads(data)
        print(data)
        return inServices.getCheckItem(data["task_id"])

@inside_api.route('/updateCheckItem', methods=['POST'])
@auth.login_required
def updateCheckItem():
    if request.method == 'POST':
        data = request.get_data()
        data = json.loads(data)
        print(data)
        return inServices.updateCheckItem(data["item_id"], data["checkResult"], data["user_id"],data["content"])

@inside_api.route('/userLogin', methods=['GET','POST'])
def userLogin():
    if request.method == 'POST':
        data = request.get_data()
        data = json.loads(data)
        print(data)
        return inServices.userLogin(data["token"])

if __name__ == '__main__':
    #apps.run(debug=True)
    pass
    #apps.run(host="0.0.0.0", port=8081, debug=True)