from flask import request, Blueprint
import json
from apps.auth.auth import auth
from apps.services import inServices
inside_api = Blueprint('inside_api', __name__, url_prefix='/inside_api/entry')

@inside_api.route('/userLogin', methods=['GET','POST'])
def userLogin():
    if request.method == 'POST':
        data = request.get_data()
        data = json.loads(data)
        print(data)
        return inServices.userLogin(data["token"])

@inside_api.route('/taskSplit', methods=['POST'])
@auth.login_required
def taskSplit():
    if request.method == 'POST':
        data = request.get_data()
        data = json.loads(data)
        print(data)
        return inServices.taskSplit(data["task_id"], data["subtask"],data["inside_token"], data["outside_token"], data["fbzId"])

@inside_api.route('/searchUserId', methods=['GET','POST'])
@auth.login_required
def searchUserId():
    if request.method == 'POST':
        data = request.get_data()
        data = json.loads(data)
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

if __name__ == '__main__':
    #apps.run(debug=True)
    pass
    #apps.run(host="0.0.0.0", port=8081, debug=True)