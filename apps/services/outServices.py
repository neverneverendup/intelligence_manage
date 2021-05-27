#coding=utf-8
from werkzeug.exceptions import NotFound
from apps.libs.utils import *

def startAssignTask(id, name, description, reward, field, document):
    #flag, user = ssologin(token)
    # print(flag, user)
    # if not flag:
    #     return pact_response_json_data(False, "-1", "用户校验失败", None)

    # result = send_task_info_to_gengxin_server(id,description,document)
    # if result["status"] == "success":
    #     # 插入初始化词条
    #     initTaskItems(result)
    task = db_select_task_by_id(id)
    if task:
        return pact_response_json_data(False, "-1", "失败，任务id已存在", None)

    db_add_task(id, name, description, reward, json.dumps(field, ensure_ascii=False), json.dumps(document, ensure_ascii=False),user_id=-1)
    task = db_select_task_by_id(id)
    task.initialize()
    return pact_response_json_data(True,"0","操作成功",None)

# 这个接口插入数据默认值有待继续调整，不知道为何空串json不能解析出来
def initTaskItems(result):
    task_id = result["subjectId"]
    print(task_id)
    try:
        task = db_select_task_by_id(task_id)
    except NotFound as e:
        print(e)
        return pact_response_json_data(False, "-1", "任务未找到", None)
    print("task", task)
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
        if not node["category"]:
            node["category"] = "[]"

        if info:
            db_add_item(original_id=node["id"], name=node["name"],relation=json.dumps(d[node["name"]] if node["name"] in d.keys() else None, ensure_ascii=False) ,field=json.dumps(node["category"],ensure_ascii=False), info_box=json.dumps(node["info"]["infoBox"],ensure_ascii=False), intro=node["info"]["intro"], imageUrl=node["info"]["imageUrl"], content=node["info"]["content"], task_id=task_id, status=1,reference="[]",isInitialize=1)
        else:
            db_add_item(original_id=node["id"], name=node["name"],relation=json.dumps(d[node["name"]] if node["name"] in d.keys() else None, ensure_ascii=False) ,field=json.dumps(node["category"] if node["category"]!='' in d.keys() else "[]",ensure_ascii=False), info_box="[]", intro="", imageUrl="", content="",task_id=task_id, status=1,reference="[]",isInitialize=1)

    task.initialize()

# 现在的resultFileType还都是字符串类型
def startTask(taskId, resultFileType, member):

    header_id = 0
    task = db_select_task_by_id(taskId)
    if not task:
        return pact_response_json_data(False, "-1", "任务未找到", None)

    for m in member:
        uid = m['userId']
        user = db_select_user_by_id(uid)
        if not user:
            user = User(id=uid, role=m["role"])
        else:
            user.role = m["role"]
        user.save()

        if m["role"] == 1:
            header_id = m['userId']
            task.user_id = m['userId']
            #continue

        user.add_subtask(m['subTaskId'])

    # 更新任务信息
    task.resultFileType = resultFileType
    task.save()

    # 确定任务划分结果之后, 新建词条
    if header_id != 0:
        db_batch_insert_items(user_id=header_id, task_id=task.id)

    return pact_response_json_data(True, "0", "操作成功", None)

def add_validator_item_mapping(user_id, item_id, result, content):
    db_add_validator_item_mapping(user_id, item_id, result, content)
    return pact_response_json_data(True, "0", "操作成功", None)

# 这里变更的话，要取消子任务的之前人员，并且不需要用户名，需要和汪松反馈
def changeTask(taskId, DetailsTaskId, userId, userName):

    task = db_select_task_by_id(taskId)
    if not task:
        return pact_response_json_data(False, "-1", "任务不存在", None)

    # 更新任务信息
    user = db_select_user_by_id(userId)
    subtask = db_select_subtask_by_id(DetailsTaskId)
    if not user:
        user = User(id=userId, name=userName)
        user.save()

    if not subtask:
        return pact_response_json_data(False, "-2", "子任务不存在", None)

    if subtask not in task.subtasks:
        return pact_response_json_data(False, "-3", "任务下不存在当前子任务", None)

    users = User.query.all()
    for u in users:
        if DetailsTaskId in json.loads(u.subtasks):
            u.remove_subtask(DetailsTaskId)
    user.add_subtask([DetailsTaskId])
    return pact_response_json_data(True, "0", "操作成功", None)

def getRate(taskId):
    task = db_select_task_by_id(taskId)
    if not task:
        return pact_response_json_data(False, "-1", "任务不存在", None)

    total_subtask_count = 0.0
    done_subtask_count = 0.0
    user_finished_status = []
    subt_ids = []
    finished_subt_ids = []
    for subt in task.subtasks:
        subt_ids.append(subt.id)
        if subt.type!=3:
            total_subtask_count += 1

        validated_item_count = 0.0
        #print('目前处理subtid',subt.id)
        if subt.type ==1 or subt.type == 2: # 新建任务 或 完善任务
            item = db_select_item_by_id(subt.item_id)
            if not item:
                continue
            if item.status == 5:
                done_subtask_count += 1
                validated_item_count += 1
                finished_subt_ids.append(subt.id)

    print("finished_subt_ids",finished_subt_ids)
    rate = (done_subtask_count ) / (total_subtask_count )

    users = User.query.all()
    for user in users:
        in_task = False
        total_subt_count = 0.0
        finished_subt_count = 0.0
        u_subt = json.loads(user.subtasks)
        validator_subt = None
        for s in u_subt:
            if s in subt_ids:
                validator_subt = Subtask.query.get(s)
                in_task = True
                total_subt_count += 1
                if s in finished_subt_ids:
                    finished_subt_count += 1

        if in_task:
            if user.role == 2:
                u_rate = finished_subt_count / total_subt_count
                status = 2 if u_rate == 1.0 else 1
                user_finished_status.append({"userId": user.id,"userName":user.name, "role":user.role, "status":status,"rate":u_rate})
            if user.role == 3:
                user_validated_item_count = Validator_Item_Mapping.query.filter_by(task_id=taskId, user_id=user.id).count()
                u_rate = user_validated_item_count / validator_subt.itemCount
                status = 2 if u_rate == 1.0 else 1
                user_finished_status.append({"userId": user.id, "userName": user.name, "role": user.role, "status": status, "rate": u_rate})

    return_dict = {"rate":rate, "member":user_finished_status}
    return pact_response_json_data(True,"0","操作成功",return_dict)

# 知识加工跳转接口
def subTask(taskId, token):

    flag, user = ssologin(token)
    if not flag:
        return pact_response_json_data(False, "-2", "用户校验失败", None)

    task = db_select_task_by_id(taskId)
    if not task:
        return pact_response_json_data(False, "-1", "未找到id对应任务", None)

    subtask_ids = json.loads(user.subtasks)
    print(subtask_ids)
    data = []
    for subt_id in subtask_ids:
        print(subt_id, taskId)
        subt = Subtask.query.filter_by(id=subt_id, task_id=taskId).first()
        if not subt:
            continue
        item_id = subt.item_id
        item = Item.query.get(item_id)
        if item:
            data.append(item.serialization())
    return pact_response_json_data(True, "0", "操作成功", data)

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
    print(resp.content)
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
    # 接收数据地址 http://101.200.34.92:8081/api/entry/initSujectAssignment
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

def test_startAssignTask():
    demand = {}
    demand["subtaskDemand"] = 10
    demand["teamDemand"] = "需要十个人"
    demand["timeDemand"] = datetime.now()

    url = 'http://127.0.0.1:5000/api/startAssignTask'
    data = {}
    data['id'] = 8888
    data['name'] = '众智化专题'
    data['description'] = '众智化专题项目测试'
    data['demand'] = demand
    data['reward'] = 888
    data['field'] = ['生物', '医学']
    data['document'] = ["文档串1", "文档串2"]
    data['token'] = '19980307'
    print(data)
    print(json.dumps(data, cls=DateEncoder))
    resp = requests.post(url, json.dumps(data, cls=DateEncoder))
    print(resp.content)
    resp = resp.json()
    print(resp)

if __name__ == '__main__':
    #data = test_return_json()
    #print(data)

    #data = jumpIntoAssignTask(987654,"19980307")
    #print(data)

    #get_item_info_from_gengxin_server()
    #subtask = [{"name":"新建词条","content":"新建五条词条","type":1,"money":500.00,"itemCount":5},{"name":"审核词条","content":"需要五个审核人员，审核词条,itemCount代表审核人员数量","type":3,"money":500.00,"userCount":5},{"name":"完善词条","content":"完善初始化词条","type":2,"money":100.00,"itemCount":5,"inited_item_ids":[17, 18]}]
    subtask = [{"name":"完善词条","content":"完善初始化词条","type":2,"money":100.00,"itemCount":5,"inited_item_ids":[17, 18]}]

    #print(taskSplit(12345678, "19980308", subtask))

    #print(getRate(8888))