from apps import create_app
from flask import Flask, request, jsonify, flash,redirect,url_for
import json

app = create_app()
#apps.app_context().push()
@app.route('/')
def hello_world():
    print("访问主页成功")
    flash("访问主页成功")
    return redirect(url_for('index'))

@app.route('/index', methods=['GET','POST'])
def index():
    if request.method == 'POST':
        data = request.get_data()
        data = json.loads(data)
        print(data)
        return jsonify({"success":True,"data":None})
    elif request.method=="GET":
        print('GET')
        return 'you find index through GET'
    return 'index'

if __name__ == '__main__':
    app.run(debug=True)
    #apps.run(host="0.0.0.0", port=8081, debug=True)