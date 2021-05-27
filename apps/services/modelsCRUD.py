import json
from apps.models.model import User, Item, Task, Subtask, db, Validator_Item_Mapping

def db_add_user(name, role, token):
    # 1 2 3 对应管理者 普通人员 审核人员
    user = User(name=name, role=role, outside_token=token)
    db.session.add(user)
    db.session.commit()

def db_add_user_with_id(id, name):
    # 1 2 3 对应管理者 普通人员 审核人员
    user = User(id=id, name=name)
    db.session.add(user)
    db.session.commit()

def db_add_task(id, name, description, reward, field, document, user_id):
    if id != None:
        task = Task(id=id, name=name, description=description, reward=reward, field=field, document=document, user_id=user_id)
    else:
        task = Task(name=name, description=description, reward=reward, field=field, document=document, user_id=user_id)
    db.session.add(task)
    db.session.commit()

def db_add_item(name, original_id, relation, field, info_box, intro, imageUrl, content, task_id, status, reference,isInitialize):
    item = Item(name=name, original_id=original_id,status=status, relation=relation, field=field, info_box=info_box, intro=intro, imageUrl=imageUrl, content=content, task_id=task_id ,reference=reference,isInitialize=isInitialize)
    db.session.add(item)
    db.session.commit()

def db_add_subtask(name, content, money, type, itemCount, task_id,user_id):
    task = Task.query.filter(Task.id==task_id).first()
    subtask = Subtask(name=name, content=content, money=money, type=type, itemCount=itemCount, task=task,user_id=user_id)
    db.session.add(subtask)
    db.session.commit()

def db_add_insert_subtask(name, content, money, type, task_id):
    item = Item(name=name, status=0, task_id=task_id)
    db.session.add(item)
    db.session.commit()
    item_id = item.id

    subtask = Subtask(name=name, content=content, money=money, type=type, task_id=task_id, item_id=item_id)
    db.session.add(subtask)
    db.session.commit()

def db_add_batch_insert_subtask(name, content, money, type, task_id, itemCount,user_id):

    latest_item_id = Item.query.order_by(Item.id.desc()).first().id
    #item_list = []
    subtask_list = []
    for idx in range(1, itemCount+1):
        #nid = latest_item_id + idx
        #item = Item(name="", status=0, task_id=task_id, field="[]",info_box="[]", relation="[]",reference="[]")
        #item_list.append(item)
        subtask = Subtask(name=name, content=content, money=money, type=type, task_id=task_id, user_id=user_id)
        subtask_list.append(subtask)

    #db.session.add_all(item_list + subtask_list)
    db.session.add_all(subtask_list)
    db.session.commit()

def db_batch_insert_items(user_id, task_id):
    # 首先检索当前负责人新建任务
    #db_select_subtask_by_id()
    subtasks = Subtask.query.filter_by(user_id=user_id, task_id=task_id).all()
    print(subtasks)
    for sub in subtasks:
        item = Item(name="", status=0, task_id=task_id, field="[]",info_box="[]", relation="[]",reference="[]")
        item.save()
        sub.item_id = item.id
        sub.save()

def db_add_batch_supply_subtask(name, content, money, type, task_id, inited_item_ids,user_id):
    subtask_list = []
    for item_id in inited_item_ids:
        item = db_select_item_by_id(item_id)
        if item:
            item.has_selected_supply = 1
            db_update_item(item)
        subtask = Subtask(name=name, content=content, money=money, type=type, task_id=task_id, item_id=item_id,user_id=user_id)
        subtask_list.append(subtask)

    db.session.add_all(subtask_list)
    db.session.commit()

def db_add_user_subtask_mapping(user_id, subtask_id):
    subtask = Subtask.query.filter(Subtask.id==subtask_id).first()
    user = User.query.filter(User.id==user_id).first()
    user.subtask.append(subtask)
    db.session.add(subtask)
    db.session.add(user)
    db.session.commit()
    return True

    #if user.role!=1:
    # if subtask.type==1 or subtask.type==2 and user.role==2:
    #     user.subtask.append(subtask)
    #     db.session.add(subtask)
    #     db.session.add(user)
    #     db.session.commit()
    #     return True
    # elif subtask.type==3 and user.role==3:
    #     user.subtask.append(subtask)
    #     db.session.add(subtask)
    #     db.session.add(user)
    #     db.session.commit()
    #     return True
    # else:
    #     print('角色权限与子任务不匹配')
    #     return False
def db_add_validator_item_mapping(user_id, item_id, result, content):
    vim = Validator_Item_Mapping(item_id=item_id, user_id=user_id, result=result, content=content)
    db.session.add(vim)
    db.session.commit()

def db_update_task(task):
    db.session.add(task)
    db.session.commit()

def db_update_user(user):
    db.session.add(user)
    db.session.commit()

def db_update_subtask(subtask):
    db.session.add(subtask)
    db.session.commit()

def db_update_item(item):
    db.session.add(item)
    db.session.commit()

def db_update_vim(vim):
    db.session.add(vim)
    db.session.commit()


def db_select_user_by_id(id):
    #user = User.query.filter(User.id==id).first()
    user = User.query.get(id)
    return user

def db_select_user_by_token(token):
    user = User.query.filter(User.token==token).first()
    return user

def db_select_task_by_id(id):
    return Task.query.get(id)

def db_select_item_by_id(id):
    #with app.app_context():
    return Item.query.get(id)

def db_select_subtask_by_id(id):
    return Subtask.query.get(id)

def db_select_subtask_bu_userToken_and_taskId(token, id):
    user = db_select_user_by_token(token)
    sub_tasks = []
    if user:
        for subt in user.subtask:
            if subt.task_id == id:
                sub_tasks.append(subt)
    return sub_tasks

def test_add_user():
    db_add_user('tom',1,'19980308')

def test_add_task():
    db_add_task('新建词条','新建一百条词条','{ "subtaskDemand":10, "teamDemand":"需要三个人", "timeDemand":"2021-01-12" }',20000.000,'领域json串','["文档串1","文档串2"]','19980308')

def test_add_item():
    db_add_item(name='吉娃娃', content='吉娃娃是一种很调皮的狗', imageUrl='/home/gzy/images/dog.jpg', status=1, subtask_id=1)

def test_add_subtask():
    db_add_subtask(name='新建词条', content='新建一百条词条', money=100.23, type=1, itemCount=100, task_id=1)

def test_add_user_subtask_mapping():
    db_add_user_subtask_mapping(user_id=2,subtask_id=1)

def test_add_task_insert_json_data():
    demand = {}
    demand["subtaskDemand"] = 100
    demand["teamDemand"] = "需要十个人"
    demand["timeDemand"] = "2021-01-01"
    demand["test_data"] = {"a":100.00,"b":None,"c":["d","e","f"]}
    data = json.dumps(demand,ensure_ascii=False)
    print(data, type(data))

    db_add_task(None,'测试json数据存储:创建宠物专题','创建宠物专题包含一百个宠物的详细信息',bytes(data,encoding='utf8'),20000.000,'领域json串','["文档串1","文档串2"]','19980308')

def test_select_task_contained_json_data():
    task = db_select_task_by_id(12345678)
    print(task)
    print(task.serialization())
    data = task.demand
    print(data)
    data = json.loads(data)
    print(data)

if __name__ == '__main__':
    #test_add_user()
    #test_add_task()
    #test_add_subtask()
    #test_add_item()
    #test_add_user_subtask_mapping()

    # user = db_select_user_by_id(2)
    # print(user)
    # print(user.subtask)

    # db_add_user_subtask_mapping(3,1)
    # db_add_user_subtask_mapping(4,1)
    # db_add_user_subtask_mapping(5,1)
    #
    # db_add_user_subtask_mapping(6, 2)
    # db_add_user_subtask_mapping(7, 2)

    #task = db_select_task_by_id(100)
    # print(task)
    # for subt in task.subtasks:
    #     print(subt)
    #     for user in subt.users:
    #         print(user)
    # user = db_select_user_by_id(6)
    # print(user, user.subtask)

    #print(db_select_subtask_bu_userToken_and_taskId('19960302',1))

    #test_add_task_insert_json_data()
    #test_select_task_contained_json_data()

    #db_select_item_by_id(25)

    db_batch_insert_items(user_id=1, task_id=5)