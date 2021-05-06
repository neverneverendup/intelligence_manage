from werkzeug.exceptions import NotFound
from apps.libs.utils import *
from apps.services.outServices import ssologin

def userLogin(outside_token):
    # 目前外部校验接口虽然开放了，但是无测试数据，先注释代码
    # flag, user = ssologin(outside_token)
    # if not flag:
    #     return pact_response_json_data(False, "-1", "外部token校验失败", None)
    user = User.query.get(1)
    if user:
        inside_token = user.create_token()
        user.inside_token = inside_token
        user.outside_token = outside_token
        db_update_user(user)
        data = {}
        data["inside_token"] = inside_token
        data["outside_token"] = outside_token
        data["user_id"] = user.id
        return pact_response_json_data(True,"0","操作成功", data)

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

def updateEditItem(item_id, original_id, name,relation ,field, info_box,intro, imageUrl, content,task_id,reference):
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
    item.status = 3
    item.reference = json.dumps(reference, ensure_ascii=False)
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
    db_add_validator_item_mapping(item_id=item_id, user_id=user_id, result=checkResult, content=content)

    return pact_response_json_data(True,"0","操作成功",None)

if __name__ == '__main__':
    # txt = ""
    # data = json.dumps(txt)
    # print(json.loads(data))
    # print('11111111111111111111111111111111111')
    print(searchUserId(3, 987654))
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