#coding=utf-8
from models import db
import requests
from werkzeug.exceptions import NotFound
from apps.services.modelsCRUD import *

def pact_response_json_data(success, respCode, respMsg, data):
    respones_data = {}
    respones_data['success'] = success
    respones_data['respCode'] = respCode
    respones_data['respMsg'] = respMsg
    respones_data['data'] = data
    #print(respones_data)
    return json.dumps(respones_data, ensure_ascii=False)

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

def startAssignTask(id, name, description, demand, reward, field, document, token):

    if not userTokenValidation(token):
        return pact_response_json_data(False, "-1", "用户校验失败", None)

    try:
        db_add_task(id, name, description, demand, reward, field, document, token)
        return pact_response_json_data(True,"0","操作成功",None)
    except Exception as e:
        print("操作失败"+str(e))
        return pact_response_json_data(False,"-1","操作失败,"+str(e),None)

def user_role_subtask_type_validation(user_id, subtask_id):
    subtask = db_select_subtask_by_id(subtask_id)
    user = db_select_user_by_id(user_id)
    #if user.role!=1:
    if subtask.type==1 and user.role==2:
        print("校验",user.role, subtask.type)
        user.subtask.append(subtask)
        db.session.add(subtask)
        db.session.add(user)
        db.session.commit()
        return True
    elif subtask.type == 2 and user.role == 2:
        print("校验", user.role, subtask.type)
        user.subtask.append(subtask)
        db.session.add(subtask)
        db.session.add(user)
        db.session.commit()
        return True
    elif subtask.type==3 and user.role==3:
        user.subtask.append(subtask)
        db.session.add(subtask)
        db.session.add(user)
        db.session.commit()
        return True
    else:
        print('角色权限与子任务不匹配')
        return False

def jumpIntoAssignTask(id, token):
    # 跳转进入任务划分界面
    try:
        task = db_select_task_by_id(id)
    except NotFound as e:
        print(e)
        return pact_response_json_data(False, "-1", "任务未找到", None)

    if not userTokenValidation(token):
        return pact_response_json_data(False, "-1", "用户校验失败", None)

    # 校验任务负责人token是否匹配
    if token == task.token:
        data = task.serialization()
        return pact_response_json_data(True, "0", "成功", data)
    else:
        return pact_response_json_data(False, "-1", "任务-负责人不匹配", None)

# 现在的resultFileType还都是字符串类型
def startTask(taskId, resultFileType, member):
    errMsg = ""
    try:
        task = db_select_task_by_id(taskId)
    except NotFound as e:
        print(e)
        return pact_response_json_data(False, 404, "任务未找到", None)

    #member = json.loads(member)
    for m in member:
        uid = m['userId']
        user = db_select_user_by_id(uid)
        if not user:
            print('当前角色用户预定义角色不匹配')
            errMsg += '当前用户不存在'
            return pact_response_json_data(False, "-1", "操作失败 " + errMsg, None)
        role = m['role']
        if role != user.role:
            print('当前用户角色与预定义角色不匹配')
            errMsg += '当前用户角色与预定义角色不匹配'
            return pact_response_json_data(False, "-1", "操作失败 " +errMsg, None)
        for subt_id in m['subTaskId']:
            if user_role_subtask_type_validation(uid, subt_id):
                #print(uid, subt_id,'通过校验')
                db_add_user_subtask_mapping(uid, subt_id)
            else:
                print('用户角色与子任务类型不匹配')
                errMsg += '用户角色与子任务类型不匹配'
                return pact_response_json_data(False, "-1", "操作失败 "+errMsg, None)

    # 更新任务信息
    task.resultFileType = resultFileType
    db_update_task(task)
    return pact_response_json_data(True, "0", "操作成功", None)

# 这个任务改动接口，所有信息都可能改动吗？ 包括任务的子任务信息完全改动吗 以及 人员子任务对应变更改动吗
def changeTask(taskId, taskName, description, resultFileType, member):
    errMsg = ""
    try:
        task = db_select_task_by_id(taskId)
    except NotFound as e:
        print(e)
        return pact_response_json_data(False, 404, "任务未找到", None)

    # 更新任务信息
    task.name = taskName
    task.description = description
    task.resultFileType = resultFileType
    db_update_task(task)

    # for m in member:
    #     uid = m['userId']
    #     user = db_select_user_by_id(uid)
    #     subt_id = m['subTaskId']
    #     if user_role_subtask_type_validation(uid, subt_id):
    #         subtask = db_select_subtask_by_id(subt_id)
    #         subtask.name = m['subTaskName']
    #         subtask.content = m['subTaskContent']
    #         subtask.money = m['subTaskMoney']
    #         db_update_subtask(subtask)
    #         user.subtask.clear()
    #         db_add_user_subtask_mapping(uid, subt_id)
    #     else:
    #

def getRate(taskId):
    task = db_select_task_by_id(taskId)
    total_subtask_count = 0.0
    done_subtask_count = 0.0
    user_finished_status = []

    for subt in task.subtasks:
        total_subtask_count += 1
        finished_item_count = 0.0
        validated_item_count = 0.0
        done_flag = False
        for item in subt.items:
            if item.status == 2:
                finished_item_count += 1
            elif item.status == 3:
                finished_item_count += 1
                validated_item_count +=1
            else:
                pass

        print(subt,subt.type,subt.itemCount, finished_item_count, validated_item_count)

        if subt.type == 1 and finished_item_count == subt.itemCount:
            print('该子任务下词条已全部编辑完毕')
            done_flag = True
            done_subtask_count += 1

        if subt.type == 2 and finished_item_count == subt.itemCount:
            print('该子任务下词条已全部编辑完毕')
            done_flag = True
            done_subtask_count += 1

        if subt.type == 3 and validated_item_count == subt.itemCount:
            print('该子任务下词条已全部审核完毕')
            done_flag = True
            done_subtask_count += 1

        for user in subt.users:
            d = {}
            d['userId'] = user.id
            d['userName'] = user.name
            d['role'] = user.role
            if user.role == 3:
                d['rate'] = validated_item_count / subt.itemCount
            else:
                d['rate'] = finished_item_count / subt.itemCount

            if done_flag:
                d['status'] = 2
                user_finished_status.append(d)
            else:
                d['status'] = 1
                user_finished_status.append(d)

    print('子任务数', total_subtask_count,'完成子任务数' , done_subtask_count )
    rate = done_subtask_count / total_subtask_count
    return_dict = {"rate":rate, "member":user_finished_status}
    return pact_response_json_data(True,"0","操作成功",return_dict)

def subTask(taskId, token):

    if not userTokenValidation(token):
        return pact_response_json_data(False, "-1", "用户校验失败", None)

    # if not token_type_validation(token):
    #     return pact_response_json_data(False, "-1", "Token类型错误", None)

    task = db_select_task_by_id(taskId)
    user = db_select_user_by_token(token)

    if not task:
        return pact_response_json_data(False, "-1", "未找到id对应任务", None)

    for subt in task.subtasks:
        if user in subt.users:
            print('找到用户对应子任务')
            return pact_response_json_data(True, "0", "操作成功", subt.serialization())

    return pact_response_json_data(False, "-3", "权限不足", None)

# 测试python数据类型和json类型之间的对应关系
def test_return_json():
    response_data = {}
    response_data["success"] = True
    response_data["test_num"] = 100.00
    response_data['test_array'] = {"id":1,"name":"jerry","test_list":[1,2,3]}
    response_data["respCoda"] = "0"
    response_data["respMsg"] = "操作成功"
    response_data["data"] = None
    return json.dumps(response_data, ensure_ascii=False)

def get_item_info_from_gengxin_server():
    # entry data server
    #dataServer.initSubject.url = http://106.2.224.58:1019/occurance
    #dataServer.submitted.url = http://106.2.224.58:1019/updatePage

    # other server
    #otherServer.checkToken.url = http://113.207.56.4:9527/user/check

    url = 'http://106.2.224.58:1019/occurance'
    data ={}
    data["subjectId"] = 100
    data["topic_name"] = "宠物"
    data["need_domain"] = 0
    data["description"] = "狗（拉丁文Canis lupus familiaris）属于脊索动物门、脊椎动物亚门、哺乳纲、真兽亚纲、食肉目、裂脚亚目、犬科动物。中文亦称“犬”，狗分布于世界各地。狗与马、牛、羊、猪、鸡并称“六畜”。有科学家认为哈士奇狗是由早期人类从灰狼驯化而来，驯养时间在4万年前~1.5万年前。被称为“人类最忠实的朋友”，是饲养率最高的宠物，其寿命大约在12~18年 [1]  。在中国文化中，狗属于十二生肖之一，在十二生肖中的第11位。 [2]"
    data["documents"] = ["狗（拉丁文Canis lupus familiaris）属于脊索动物门、脊椎动物亚门、哺乳纲、真兽亚纲、食肉目、裂脚亚目、犬科动物。中文亦称“犬”，狗分布于世界各地。狗与马、牛、羊、猪、鸡并称“六畜”。有科学家认为哈士奇狗是由早期人类从灰狼驯化而来，驯养时间在4万年前~1.5万年前。被称为“人类最忠实的朋友”，是饲养率最高的宠物，其寿命大约在12~18年 [1]  。在中国文化中，狗属于十二生肖之一，在十二生肖中的第11位","宠物（pet）指人们为了精神目的，而不是为了经济目的而豢养的生物。传统的宠物是指哺乳纲或鸟纲的动物，养着用于玩赏和作伴。实际生活中的宠物包括鱼纲、爬行纲、两栖纲、昆虫，甚至植物，用于观赏、作伴、舒缓人们的精神压力。 [1]"]
    resp = requests.post(url,json.dumps(data))
    print(resp.content)
    resp = resp.json()
    print(resp)
    if resp['status'] == "success":
        print("数据解析成功！")
        print(resp['data'])
    # 问问学长 接口要传的数据的含义，以及为什么status一直是数据正在解析

def send_data_to_http_server():
    url = 'http://127.0.0.1:5000/index/'
    data ={}
    data["subjectId"] = 100
    data["topic_name"] = "宠物"
    data["need_domain"] = 0
    data["description"] = "狗（拉丁文Canis lupus familiaris）属于脊索动物门、脊椎动物亚门、哺乳纲、真兽亚纲、食肉目、裂脚亚目、犬科动物。中文亦称“犬”，狗分布于世界各地。狗与马、牛、羊、猪、鸡并称“六畜”。有科学家认为哈士奇狗是由早期人类从灰狼驯化而来，驯养时间在4万年前~1.5万年前。被称为“人类最忠实的朋友”，是饲养率最高的宠物，其寿命大约在12~18年 [1]  。在中国文化中，狗属于十二生肖之一，在十二生肖中的第11位。 [2]"
    data["documents"] = ["狗（拉丁文Canis lupus familiaris）属于脊索动物门、脊椎动物亚门、哺乳纲、真兽亚纲、食肉目、裂脚亚目、犬科动物。中文亦称“犬”，狗分布于世界各地。狗与马、牛、羊、猪、鸡并称“六畜”。有科学家认为哈士奇狗是由早期人类从灰狼驯化而来，驯养时间在4万年前~1.5万年前。被称为“人类最忠实的朋友”，是饲养率最高的宠物，其寿命大约在12~18年 [1]  。在中国文化中，狗属于十二生肖之一，在十二生肖中的第11位","宠物（pet）指人们为了精神目的，而不是为了经济目的而豢养的生物。传统的宠物是指哺乳纲或鸟纲的动物，养着用于玩赏和作伴。实际生活中的宠物包括鱼纲、爬行纲、两栖纲、昆虫，甚至植物，用于观赏、作伴、舒缓人们的精神压力。 [1]"]
    resp = requests.post(url,json.dumps(data))
    print(resp.content)
    resp = resp.json()
    print(resp)
    # if resp['status'] == "success":
    #     print("数据解析成功！")
    #     print(resp['data'])
    # 问问学长 接口要传的数据的含义，以及为什么status一直是数据正

def send_data_to_startAssignTask_server():
    demand = {}
    demand["subtaskDemand"] = 100
    demand["teamDemand"] = "需要十个人"
    demand["timeDemand"] = "2021-01-01"
    demand["test_data"] = {"a":100.00,"b":None,"c":["d","e","f"]}
    # data = json.dumps(demand,ensure_ascii=False)

    url = 'http://127.0.0.1:5000/api/startAssignTask'
    data = {}
    data['id'] = 12345678
    data['name'] = '众智化专题'
    data['description'] = '众智化专题项目测试'
    data['demand'] = demand
    data['reward'] = 666.888
    data['field'] = '不详'
    data['document'] = '["文档串1","文档串2"]'
    data['token'] = '19980308'
    resp = requests.post(url, json.dumps(data))
    print(resp.content)
    resp = resp.json()
    print(resp)

def send_data_to_jumpIntoAssignTask_server():

    url = 'http://127.0.0.1:5000/api/jumpIntoAssignTask'
    data = {}
    data['id'] = 12345678
    data['token'] = '19980308'

    resp = requests.post(url, json.dumps(data))
    #print(resp.content)
    resp = resp.json()
    print(resp)

def send_data_to_startTask_server():

    url = 'http://127.0.0.1:5000/api/startTask'
    data = {}
    data['taskId'] = 12345678
    data['resultFileType'] = 'pdf'
    data['member'] = [{"userId":3,"role":2,"subTaskId":[5]},{"userId":4,"role":2,"subTaskId":[5]},{"userId":7,"role":3,"subTaskId":[6]}]

    resp = requests.post(url, json.dumps(data))
    #print(resp.content)
    resp = resp.json()
    print(resp)

def send_data_to_getRate_server():

    url = 'http://127.0.0.1:5000/api/getRate'
    data = {}
    data['taskId'] = 12345678

    resp = requests.post(url, json.dumps(data))
    #print(resp.content)
    resp = resp.json()
    print(resp)

def send_data_to_subTask_server():

    url = 'http://127.0.0.1:5000/api/subTask'
    data = {}
    data['taskId'] = 12345678
    data['token'] = "19980101"
    resp = requests.post(url, json.dumps(data))
    #print(resp.content)
    resp = resp.json()
    print(resp)

if __name__ == '__main__':
    #send_data_to_http_server()
    #send_data_to_startAssignTask_server()
    send_data_to_jumpIntoAssignTask_server()
    #send_data_to_startTask_server()
    #send_data_to_getRate_server()
    #send_data_to_subTask_server()