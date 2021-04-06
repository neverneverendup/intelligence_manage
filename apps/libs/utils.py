import json
from ..services.modelsCRUD import *
from datetime import date, datetime

def pact_response_json_data(success, respCode, respMsg, data):
    respones_data = {}
    respones_data['success'] = success
    respones_data['respCode'] = respCode
    respones_data['respMsg'] = respMsg
    respones_data['data'] = data
    #print(respones_data)
    return json.dumps(respones_data, ensure_ascii=False,cls=DateEncoder)

def userTokenValidation(token):
    user = db_select_user_by_token(token)
    if not user:
        return False
    return True

def token_type_validation(token):
    print(type(token))
    if type(token)==str:
        return True
    else:
        return False

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