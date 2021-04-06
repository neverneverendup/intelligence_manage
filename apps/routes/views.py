from flask import request, jsonify, Blueprint
import json
#from apps.models.models import apps
from apps.services import outServices

api = Blueprint('api', __name__, url_prefix='/api')

# @apps.route('/')
# def hello_world():
#     print("访问主页成功")
#     return 'hello world'
#
# @apps.route('/index/', methods=['GET','POST'])
# def index():
#     if request.method == 'POST':
#         data = request.get_data()
#         data = json.loads(data)
#         print(data)
#         return jsonify({"success":True,"data":None})
#     elif request.method=="GET":
#         print('GET')
#     return 'index'

#@apps.route('/api/startAssignTask/', methods=['POST'])
@api.route('/startAssignTask', methods=['GET', 'POST'])
def api_startAssignTask():
    if request.method == 'POST':
        data = request.get_data()
        data = json.loads(data)
        print(data)
        return outServices.startAssignTask(data['id'], data['name'], data['description'], data['demand'], data['reward'], data['field'], data['document'], data['token'])
    return 'you see this /startAssignTask in get!'

#@apps.route('/api/jumpIntoAssignTask/', methods=['POST'])
@api.route('/assignTask', methods=['GET', 'POST'])
def jumpIntoAssignTask():
    if request.method == 'POST':
        data = request.get_data()
        data = json.loads(data)
        print(data)
        return outServices.jumpIntoAssignTask(data['id'], data['token'])
    return 'you see this /jumpIntoAssignTask in get!'

@api.route('/resultNotice', methods=['POST'])
def resultNotice():
    if request.method == 'POST':
        data = request.get_data()
        data = json.loads(data)
        print(data)
        return outServices.resultNotice(data)

#@apps.route('/api/startTask/', methods=['POST'])
@api.route('/startTask', methods=['POST'])
def startTask():
    if request.method == 'POST':
        data = request.get_data()
        data = json.loads(data)
        print(data)
        return outServices.startTask(data['taskId'], data['resultFileType'], data['member'])

#@apps.route('/api/getRate/', methods=['POST'])
@api.route('/getRate', methods=['POST'])
def getRate():
    if request.method == 'POST':
        data = request.get_data()
        data = json.loads(data)
        print(data)
        return outServices.getRate(data['taskId'])

#@apps.route('/api/subTask/', methods=['POST'])
@api.route('/subTask', methods=['POST'])
def subTask():
    if request.method == 'POST':
        data = request.get_data()
        data = json.loads(data)
        print(data)
        return outServices.subTask(data['taskId'], data['token'])

#@apps.route('/api/entry/initSubjectAssignment', methods=['POST'])
@api.route('/initSubjectAssignment', methods=['POST'])
def initSubjectAssignment():
    if request.method == 'POST':
        data = request.get_data()
        data = json.loads(data)
        outServices.initTaskItems(data)
        print(data)
        return outServices.pact_response_json_data(True, "0", "", None)

if __name__ == '__main__':
    #apps.run(debug=True)
    pass
    #apps.run(host="0.0.0.0", port=8081, debug=True)