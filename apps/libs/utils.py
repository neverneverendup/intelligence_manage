from ..services.modelsCRUD import *
from datetime import date, datetime
import requests


def pact_response_json_data(success, respCode, respMsg, data):
    respones_data = {}
    respones_data['success'] = success
    respones_data['respCode'] = respCode
    respones_data['respMsg'] = respMsg
    respones_data['data'] = data
    #print(respones_data)
    return json.dumps(respones_data, ensure_ascii=False,cls=DateEncoder)


def ssologin(token):
    resp = outside_token_validation(token)
    print(resp)
    if  "success" not in resp.keys() or resp["success"] == False:
        return False, None
    user = check_and_add_user(resp=resp, token=token)
    return True, user


# 外部用户token校验接口
def outside_token_validation(token):
    url = 'http://113.207.56.4:9527/user/check'
    header = {"Content-Type": "multipart/form-data"}
    data = {}
    data['token'] = token
    resp = requests.post(url=url, data=data)
    return resp.json()


def check_and_add_user(resp, token):
    user_id = resp["data"]["data"]["id"]
    name=resp["data"]["data"]["name"]
    user = User.query.get(user_id)
    if not user:
        user = User(id=user_id, name=name)
    user.name = name
    return user


def user_role_subtask_type_validation(user_id, subtask_id):
    subtask = db_select_subtask_by_id(subtask_id)
    user = db_select_user_by_id(user_id)
    #if user.role!=1:
    if subtask.type==1 and user.role==2:
        return True
    elif subtask.type == 2 and user.role == 2:
        return True
    elif subtask.type==3 and user.role==3:
        return True
    else:
        print('角色权限与子任务不匹配')
        return False

class DateEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, datetime):
            return obj.strftime('%Y-%m-%d %H:%M:%S')
        elif isinstance(obj, date):
            return obj.strftime("%Y-%m-%d")
        else:
            return json.JSONEncoder.default(self, obj)