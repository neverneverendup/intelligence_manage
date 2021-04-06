#coding=utf-8
import requests
from werkzeug.exceptions import NotFound
from apps.services.modelsCRUD import *
from apps.libs.utils import *

def startAssignTask(id, name, description, demand, reward, field, document, token):
    if not userTokenValidation(token):
        return pact_response_json_data(False, "-1", "用户校验失败", None)

    result = send_task_info_to_gengxin_server(id,description,document)
    if result["status"] == "success":
        # 插入初始化词条
        initTaskItems(result)
    timeDemand = demand['timeDemand']
    subtaskDemand = demand['subtaskDemand']
    teamDemand = demand['teamDemand']
    db_add_task(id, name, description, timeDemand, subtaskDemand, teamDemand, reward, json.dumps(field, ensure_ascii=False), json.dumps(document, ensure_ascii=False), token)
    return pact_response_json_data(True,"0","操作成功",None)

def initTaskItems(result):
    task_id = result["subjectId"]
    try:
        task = db_select_task_by_id(id)
    except NotFound as e:
        print(e)
        return pact_response_json_data(False, "-1", "任务未找到", None)
    data = result
    d = {}
    for edg in data["edges"]:

        n1 = edg["node1"]
        n2 = edg["node2"]
        if n1 not in d.keys():
            d[n1] = []
        if n2 not in d.keys():
            d[n2] = []

        if edg["rel_type"] == "co-occurrence":
            d[n1].append({"entry":n2, "type":"共现词"})
            d[n2].append({"entry":n1, "type":"共现词"})

        if edg["rel_type"] == "is-a":
            d[n1].append({"entry":n2, "type":"上位词"})
            d[n2].append({"entry":n1, "type":"下位词"})

    for node in data["nodes"]:
        #item = Item(original_id=node["originalId"], field=node["category"], info_box=node["info"]["intro_box"], intro=node["info"]["intro"], imageUrl=node["info"]["imageUrl"], content=node["info"]["content"])
        info = node["info"]
        if info:
            db_add_item(original_id=node["id"], name=node["name"],relation=json.dumps(d[node["name"]] if node["name"] in d.keys() else None, ensure_ascii=False) ,field=json.dumps(node["category"],ensure_ascii=False), info_box=json.dumps(node["info"]["infoBox"],ensure_ascii=False), intro=node["info"]["intro"], imageUrl=node["info"]["imageUrl"], content=node["info"]["content"], task_id=task_id, status=1)
        else:
            db_add_item(original_id=node["id"], name=node["name"],relation=json.dumps(d[node["name"]] if node["name"] in d.keys() else None, ensure_ascii=False) ,field=json.dumps(node["category"],ensure_ascii=False), info_box="", intro="", imageUrl="", content="",task_id=task_id, status=1)

    #task.hasInitialize = 1
    #db.session.commit()
    task.initialize()
# 把发送过去的所有数据全部都接收并存在vue中，等任务负责人划分完任务后，把子任务信息和专题信息一并发送给课题组屋的resultNotice接口
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
        print(task.hasInitialize)
        if task.hasInitialize == 0 :
            print('未通过')
            return pact_response_json_data(False, "-1", "稍作等待，任务未初始化完毕", None)
        print('已通过')
        task_data = task.serialization()
        items_data = task.get_items()
        data = {}
        data['task'] = task_data
        data['items'] = items_data
        return pact_response_json_data(True, "0", "成功", data)
    else:
        return pact_response_json_data(False, "-1", "任务-负责人不匹配", None)

def resultNotice(post_data):
    url = 'http:// 113.207.56.4:9527/process/task/resultNotice'
    resp = requests.post(url, json.dumps(post_data, ensure_ascii=False))
    # print(resp.content)
    resp = resp.json()
    print(resp)
    if resp['success'] == True:
        print("任务划分结果数据发送成功！")
        print(resp['data'])
    return resp

# 提交任务划分结果，这里要做的事情包括三类子任务，新建任务、完善任务和审核任务。
# 新建任务需要提交完整的子任务信息，审核任务需要提交审核人员数量，完善任务需要提交已初始化词条id。
def taskSplit(taskId, token, subtask):
    # 接收子任务详情情况，将数据插入数据库
    try:
        task = db_select_task_by_id(taskId)
    except NotFound as e:
        print(e)
        return pact_response_json_data(False, "-1", "任务未找到", None)

    if not userTokenValidation(token):
        return pact_response_json_data(False, "-1", "用户校验失败", None)

    if token != task.token:
        return pact_response_json_data(False, "-1", "任务-负责人不匹配", None)

    for subt in subtask:
        if subt["type"] == 1:
            db_add_batch_insert_subtask(name=subt["name"],content=subt["content"],money=subt["money"],type=subt["type"],task_id=taskId,itemCount=subt["itemCount"])
            # for _ in range(subt["itemCount"]):
            #     db_add_insert_subtask(name=subt["name"],content=subt["content"],money=subt["money"],type=subt["type"],task_id=taskId)
        if subt["type"] == 2:
            inited_item_ids = subt["inited_item_ids"]
            db_add_batch_supply_subtask(name=subt["name"],content=subt["content"],money=subt["money"],type=subt["type"],task_id=taskId, inited_item_ids=inited_item_ids)
        if subt["type"] == 3:
            db_add_subtask(name=subt["name"],content=subt["content"],money=subt["money"],type=subt["type"],task_id=taskId,itemCount=0)


    return pact_response_json_data(True, "0", "成功", None)

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
                #db_add_user_subtask_mapping(uid, subt_id)
                subt = db_select_subtask_by_id(subt_id)
                subt.add_user(uid)
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
    rate = 0.0
    # for subt in task.subtasks:
    #     total_subtask_count += 1
    #     finished_item_count = 0.0
    #     validated_item_count = 0.0
    #     done_flag = False
    #     for item in subt.items:
    #         if item.status == 2:
    #             finished_item_count += 1
    #         elif item.status == 3:
    #             finished_item_count += 1
    #             validated_item_count +=1
    #         else:
    #             pass
    #
    #     print(subt,subt.type,subt.itemCount, finished_item_count, validated_item_count)
    #
    #     if subt.type == 1 and finished_item_count == subt.itemCount:
    #         print('该子任务下词条已全部编辑完毕')
    #         done_flag = True
    #         done_subtask_count += 1
    #
    #     if subt.type == 2 and finished_item_count == subt.itemCount:
    #         print('该子任务下词条已全部编辑完毕')
    #         done_flag = True
    #         done_subtask_count += 1
    #
    #     if subt.type == 3 and validated_item_count == subt.itemCount:
    #         print('该子任务下词条已全部审核完毕')
    #         done_flag = True
    #         done_subtask_count += 1
    #
    #     for user in subt.users:
    #         d = {}
    #         d['userId'] = user.id
    #         d['userName'] = user.name
    #         d['role'] = user.role
    #         if user.role == 3:
    #             d['rate'] = validated_item_count / subt.itemCount
    #         else:
    #             d['rate'] = finished_item_count / subt.itemCount
    #
    #         if done_flag:
    #             d['status'] = 2
    #             user_finished_status.append(d)
    #         else:
    #             d['status'] = 1
    #             user_finished_status.append(d)
    #
    # print('子任务数', total_subtask_count,'完成子任务数' , done_subtask_count )
    #rate = done_subtask_count / total_subtask_count

    return_dict = {"rate":rate, "member":user_finished_status}
    return pact_response_json_data(True,"0","操作成功",return_dict)

# 知识加工跳转接口
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

def send_task_info_to_gengxin_server(id, description, documents):
    # entry data server
    #dataServer.initSubject.url = http://106.2.224.58:1019/occurance
    #dataServer.submitted.url = http://106.2.224.58:1019/updatePage

    # other server
    #otherServer.checkToken.url = http://113.207.56.4:9527/user/check

    url = 'http://106.2.224.58:1019/occurance'
    data ={}
    data["subjectId"] = id
    data["topic_name"] = "宠物"
    data["need_domain"] = 0
    data["description"] = description
    # "狗（拉丁文Canis lupus familiaris）属于脊索动物门、脊椎动物亚门、哺乳纲、真兽亚纲、食肉目、裂脚亚目、犬科动物。中文亦称“犬”，狗分布于世界各地。狗与马、牛、羊、猪、鸡并称“六畜”。有科学家认为哈士奇狗是由早期人类从灰狼驯化而来，驯养时间在4万年前~1.5万年前。被称为“人类最忠实的朋友”，是饲养率最高的宠物，其寿命大约在12~18年 [1]  。在中国文化中，狗属于十二生肖之一，在十二生肖中的第11位。 [2]"
    data["documents"] = documents
    # ["狗（拉丁文Canis lupus familiaris）属于脊索动物门、脊椎动物亚门、哺乳纲、真兽亚纲、食肉目、裂脚亚目、犬科动物。中文亦称“犬”，狗分布于世界各地。狗与马、牛、羊、猪、鸡并称“六畜”。有科学家认为哈士奇狗是由早期人类从灰狼驯化而来，驯养时间在4万年前~1.5万年前。被称为“人类最忠实的朋友”，是饲养率最高的宠物，其寿命大约在12~18年 [1]  。在中国文化中，狗属于十二生肖之一，在十二生肖中的第11位","宠物（pet）指人们为了精神目的，而不是为了经济目的而豢养的生物。传统的宠物是指哺乳纲或鸟纲的动物，养着用于玩赏和作伴。实际生活中的宠物包括鱼纲、爬行纲、两栖纲、昆虫，甚至植物，用于观赏、作伴、舒缓人们的精神压力。 [1]"]
    resp = requests.post(url,json.dumps(data))
    #print(resp.content)
    resp = resp.json()
    print(resp)
    if resp['status'] == "success":
        print("数据解析成功！")
        print(resp['data'])
    return resp

    # 问问学长 接口要传的数据的含义，以及为什么status一直是数据正在解析

def get_item_info_from_gengxin_server():
    # entry data server
    #dataServer.initSubject.url = http://106.2.224.58:1019/occurance
    #dataServer.submitted.url = http://106.2.224.58:1019/updatePage

    # other server
    #otherServer.checkToken.url = http://113.207.56.4:9527/user/check

    url = 'http://106.2.224.58:1019/occurance'
    data ={}
    data["subjectId"] = 1
    data["topic_name"] = "宠物"
    data["need_domain"] = 0
    data["description"] = "狗（拉丁文Canis lupus familiaris）属于脊索动物门、脊椎动物亚门、哺乳纲、真兽亚纲、食肉目、裂脚亚目、犬科动物。中文亦称“犬”，狗分布于世界各地。狗与马、牛、羊、猪、鸡并称“六畜”。有科学家认为哈士奇狗是由早期人类从灰狼驯化而来，驯养时间在4万年前~1.5万年前。被称为“人类最忠实的朋友”，是饲养率最高的宠物，其寿命大约在12~18年 [1]  。在中国文化中，狗属于十二生肖之一，在十二生肖中的第11位。 [2]"
    data["documents"] = ["狗（拉丁文Canis lupus familiaris）属于脊索动物门、脊椎动物亚门、哺乳纲、真兽亚纲、食肉目、裂脚亚目、犬科动物。中文亦称“犬”，狗分布于世界各地。狗与马、牛、羊、猪、鸡并称“六畜”。有科学家认为哈士奇狗是由早期人类从灰狼驯化而来，驯养时间在4万年前~1.5万年前。被称为“人类最忠实的朋友”，是饲养率最高的宠物，其寿命大约在12~18年 [1]  。在中国文化中，狗属于十二生肖之一，在十二生肖中的第11位","宠物（pet）指人们为了精神目的，而不是为了经济目的而豢养的生物。传统的宠物是指哺乳纲或鸟纲的动物，养着用于玩赏和作伴。实际生活中的宠物包括鱼纲、爬行纲、两栖纲、昆虫，甚至植物，用于观赏、作伴、舒缓人们的精神压力。 [1]"]
    resp = requests.post(url,json.dumps(data))
    #print(resp.content)
    resp = resp.json()
    print(resp)
    if resp['status'] == "success":
        print("数据解析成功！")
        print(resp['data'])

if __name__ == '__main__':
    #data = test_return_json()
    #print(data)

    #data = jumpIntoAssignTask(2,"19980308")
    #print(data)

    #get_item_info_from_gengxin_server()
    subtask = [{"name":"新建词条","content":"新建五条词条","type":1,"money":500.00,"itemCount":5},{"name":"审核词条","content":"需要五个审核人员，审核词条,itemCount代表审核人员数量","type":3,"money":500.00,"userCount":5},{"name":"完善词条","content":"完善初始化词条","type":2,"money":100.00,"itemCount":5,"inited_item_ids":[17, 18]}]
    print(taskSplit(12345678, "19980308", subtask))