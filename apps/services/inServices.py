from werkzeug.exceptions import NotFound
from apps.libs.utils import *
from apps.services.outServices import ssologin
from apps.auth import auth
from apps.config import *

def userLogin(outside_token):
    # 目前外部校验接口虽然开放了，但是无测试数据，先注释代码
    flag, user = ssologin(outside_token)
    if not flag:
        return pact_response_json_data(False, "-1", "外部token校验失败", None)
    #user = User.query.get(int(outside_token))
    print(user)
    print('用户登录检查断点')
    if user:
        inside_token = user.create_token()
        user.inside_token = inside_token
        #user.outside_token = outside_token
        user.save()
        data = {}
        data["inside_token"] = inside_token
        data["outside_token"] = outside_token
        data["user_id"] = user.id
        data["role"] = user.role
        print('用户校验成功')
        return pact_response_json_data(True,"0","操作成功", data)
    else:
        print('用户不存在，校验失败')
        return pact_response_json_data(False,"-2","用户校验失败", None)

def resultNotice(post_data):
    url = 'http://113.207.56.4:9527/common/task/huaFenTaskResult'
    headers={"Content-Type": "multipart/form-data"}
    headers["token"] = "eyJhbGciOiJIUzI1NiJ9.eyJsb2dpblR5cGUiOjAsInVzZXIiOnsiY2VsZWJyaXR5Ijp0cnVlLCJpbWciOiJcL3Jlc291cmNlc1wvdHJhZGluZ1wvdXBsb2FkXC9qcGdcL2Q0MWI5YTRjLTBlZjktNDYxYy1hMGE5LWIxOWEyN2NkMzQwOC5qcGciLCJmaXJzdExhYmxlIjoi6K6h566X5py6IiwiYXJ0aWNsZU51bSI6MCwibGV2ZWwiOjAsIndkQWNjZXB0TnVtIjoyLCJ0aGlyZExhYmxlIjoi56eR5oqAIiwiaW5kdXN0cnkiOiLorqHnrpfmnLrnp5HlraYiLCJmdHBwYXRoIjoiQzpcL2Z0cFwvYWRtaW4iLCJpc0FkbWluIjoxLCJzZWNvbmRMYWJsZSI6IuadkOaWmSIsIm1vbmV5IjozMzUsInBob25lIjoiMTMxNTIxMzQwMDAiLCJjb25jZXJuTnVtIjoxLCJpbnRlZ3JhbCI6MTg2LCJsb2dpbk5hbWUiOiJkaiIsIm5hbWUiOiLkuIHpnIEiLCJ3ZEFuc3dlck51bSI6NSwiaWQiOjI2LCJlbWFpbCI6IjEyMzQxMjQ0NDVAcXEuY29tIn0sInJhbmRvbSI6IjIxMzMzZDFiLWIwZjktNDIzZS1iYTEzLTcxN2ExYjNkMzc5NyJ9.q1EHXZXsi7VKty5QGorNdqdLXAfEX0UDeTCJvPmP8hE"
    resp = requests.post(url, headers=headers, data=json.dumps(post_data))
    # print(resp.content)
    resp = resp.json()
    print(resp)
    if resp['success'] == True:
        print("任务划分结果数据发送成功！")
        print(resp['data'])
    return resp

# 提交任务划分结果，这里要做的事情包括三类子任务，新建任务、完善任务和审核任务。
# 新建任务需要提交完整的子任务信息，审核任务需要提交审核人员数量，完善任务需要提交已初始化词条id。
# 最新改动，取消输入token参数
def taskSplit(taskId, subtask, inside_token):
    # 接收子任务详情情况，将数据插入数据库
    s = Serializer(Config.SECRET_KEY)
    try:
        data = s.loads(inside_token)
        print(data)
    except SignatureExpired:
        return False
    except BadSignature:
        return False
    print(data)
    print(data.get('user_id'))
    user = User.query.get(data.get('user_id'))
    print(user)
    userId = user.id
    try:
        task = db_select_task_by_id(taskId)
    except NotFound as e:
        print(e)
        return pact_response_json_data(False, "-1", "任务未找到", None)

    for subt in subtask:
        if subt["type"] == 1:
            db_add_batch_insert_subtask(name=subt["name"],content=subt["content"],money=subt["money"],type=subt["type"],task_id=taskId,itemCount=subt["itemCount"], user_id = userId)
        if subt["type"] == 2:
            inited_item_ids = subt["itemTable"]
            db_add_batch_supply_subtask(name=subt["name"],content=subt["content"],money=subt["money"],type=subt["type"],task_id=taskId, inited_item_ids=inited_item_ids,user_id = userId)
        if subt["type"] == 3:
            for itemcount in subt["itemTable"]:
                db_add_subtask(name=subt["name"],content=subt["content"],money=subt["money"],type=subt["type"],task_id=taskId, itemCount=itemcount, user_id = userId)

    post_data = {}
    post_data["taskId"] = task.id
    post_data["taskName"] = task.name
    post_data["taskType"] = 3
    post_data["fzrId"] = user.id
    #header = db_select_user_by_id(task.user_id)
    post_data["fzrName"] = user.name
    post_data["childTasks"] = []

    for sub in task.subtasks:
        t = {}
        t["childTaskId"] = sub.id
        t["childTaskName"] = sub.name
        t["childTaskDescribe"] = sub.content
        t["childTaskMoney"] = str(sub.money)
        t["childTaskDay"] = 10
        t["jgUserId"] = sub.id
        t["jgUserName"] = sub.id
        post_data["childTasks"].append(t)

    resp = resultNotice(post_data)
    if resp['success'] == True:
        return pact_response_json_data(True, "0", "成功", None)
    else:
        return pact_response_json_data(False, "-1", resp['respMsg'], None)

def searchUserId(userId, taskId):
    user = db_select_user_by_id(userId)
    if not user:
        print('用户Id不存在')
        err_mgs = '用户Id不存在'
        return pact_response_json_data(False, "-1", err_mgs, None)
    if user.role != 2:
        err_mgs = '用户角色为非加工者'
        return pact_response_json_data(False,"0",err_mgs, None)

    subtask_ids = json.loads(user.subtasks)
    data = []
    for subt_id in subtask_ids:
        subt = Subtask.query.filter_by(id=subt_id, task_id=taskId).first()
        if not subt:
            continue
        item_id = subt.item_id
        item = Item.query.get(item_id)
        print(item)
        if item:
            data.append(item.serialization())
    return pact_response_json_data(True,"0","操作成功",data)

def updateEditItem(item_id, original_id, name,relation ,field, info_box,intro, imageUrl, content,task_id,reference, operation):
    item = db_select_item_by_id(item_id)
    item.original_id = original_id
    item.name=name
    item.relation=json.dumps(relation, ensure_ascii=False)
    item.field = json.dumps(field, ensure_ascii=False)
    item.info_box = json.dumps(info_box, ensure_ascii=False)
    item.intro = intro
    item.imageUrl = imageUrl
    item.content = content
    item.task_id = task_id
    item.reference = json.dumps(reference, ensure_ascii=False)
    # 0代表保存, 1代表提交审核
    if operation == 0:
        pass
    elif operation == 1:
        item.status = 3
    db_update_item(item)
    return pact_response_json_data(True,"0","操作成功",None)

def getCheckItem(task_id):
    try:
        task = db_select_task_by_id(task_id)
    except NotFound as e:
        print(e)
        return pact_response_json_data(False, "-1", "任务未找到", None)
    items = task.items
    data = [ ]
    for i in items:
        if i.status == 3:
            data.append(i.serialization())

    return pact_response_json_data(True,"0","操作成功",data)

def updateCheckItem(item_id, checkResult, user_id, content):
    try:
        item = db_select_item_by_id(item_id)
    except NotFound as e:
        print(e)
        return pact_response_json_data(False, "-1", "词条未找到", None)
    if not item:
        return pact_response_json_data(False, "-1", "词条未找到", None)

    if item.status !=3:
        return pact_response_json_data(False, "-1", "词条前置状态错误:"+str(item.status), None)

    if checkResult == 0:
        item.status = 4
    else:
        item.status = 5

    db_update_item(item)
    vim = Validator_Item_Mapping.query.filter_by(item_id=item_id, user_id=user_id).first()
    if vim:
        vim.result = checkResult
        vim.content = content
        db_update_vim(vim)
    else:
        db_add_validator_item_mapping(item_id=item_id, user_id=user_id, result=checkResult, content=content)

    return pact_response_json_data(True,"0","操作成功",None)

if __name__ == '__main__':
    # txt = ""
    # data = json.dumps(txt)
    # print(json.loads(data))
    # print('11111111111111111111111111111111111')
    #print(searchUserId(3, 987654))
    # print(getCheckItem(8888))
    # print(updateEditItem(42,1000,"无名词条","","","","","未知地址","内容",8888))
    # print(updateCheckItem(43, 1))

    #item = Item(id=name="", status=0, task_id=8888, field="[]", info_box="[]", relation="[]")
    #item = db_update_item(5)
    #
    # item = Item.query.get(50)
    # print(item.serialization())
    # print("值",item.relation)
    # item.relation = json.dumps(None)
    # db_update_item(item)
    # print(item.serialization())

    userLogin(1)