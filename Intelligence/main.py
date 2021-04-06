from flask import Flask,request, jsonify
import json
from models import app
import services

@app.route('/')
def hello_world():
    print("访问主页成功")
    return 'hello world'

@app.route('/index/', methods=['GET','POST'])
def index():
    if request.method == 'POST':
        data = request.get_data()
        data = json.loads(data)
        print(data)
        return jsonify({"success":True,"data":None})
    elif request.method=="GET":
        print('GET')
    return 'index'

@app.route('/api/startAssignTask/', methods=['POST'])
def api_startAssignTask():
    if request.method == 'POST':
        data = request.get_data()
        data = json.loads(data)
        print(data)
        return services.startAssignTask(data['id'], data['name'], data['description'], bytes(json.dumps(data['demand'],ensure_ascii=False),encoding='utf8'), data['reward'], data['field'], data['document'], data['token'])

@app.route('/api/jumpIntoAssignTask/', methods=['POST'])
def jumpIntoAssignTask():
    if request.method == 'POST':
        data = request.get_data()
        data = json.loads(data)
        print(data)
        return services.jumpIntoAssignTask(data['id'], data['token'])

@app.route('/api/startTask/', methods=['POST'])
def startTask():
    if request.method == 'POST':
        data = request.get_data()
        data = json.loads(data)
        print(data)
        return services.startTask(data['taskId'], data['resultFileType'], data['member'])

@app.route('/api/getRate/', methods=['POST'])
def getRate():
    if request.method == 'POST':
        data = request.get_data()
        data = json.loads(data)
        print(data)
        return services.getRate(data['taskId'])

@app.route('/api/subTask/', methods=['POST'])
def subTask():
    if request.method == 'POST':
        data = request.get_data()
        data = json.loads(data)
        print(data)
        return services.subTask(data['taskId'], data['token'])

@app.route('/api/entry/initSubjectAssignment', methods=['POST'])
def initSubjectAssignment():
    if request.method == 'POST':
        data = request.get_data()
        data = json.loads(data)
        services.initTaskItems(data)
        print(data)
        return services.pact_response_json_data(True,"0","",None)

if __name__ == '__main__':
    #apps.run(debug=True)
    app.run(host="0.0.0.0", port=8081, debug=True)