#coding=utf-8
import requests
from werkzeug.exceptions import NotFound
from datetime import date,datetime
from apps.services.modelsCRUD import *
from apps.services import inServices
from apps.libs.utils import *

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

class DateEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, datetime):
            return obj.strftime('%Y-%m-%d %H:%M:%S')
        elif isinstance(obj, date):
            return obj.strftime("%Y-%m-%d")
        else:
            return json.JSONEncoder.default(self, obj)

def send_data_to_startAssignTask_server():
    #demand["test_data"] = {"a":100.00,"b":None,"c":["d","e","f"]}
    # data = json.dumps(demand,ensure_ascii=False)

    url = 'http://101.200.34.92:8081/api/entry/startAssignTask'
    data = {}
    data['taskId'] = 9
    data['taskName'] = '众智化专题'
    data['description'] = '众智化专题项目测试'
    data['reward'] = 6666.999
    data['field'] = ['生物','医学']
    data['document'] = ["猫，属于猫科动物，分家猫、野猫，是全世界家庭中较为广泛的宠物。家猫的祖先据推测是古埃及的沙漠猫，波斯的波斯猫，已经被人类驯化了3500年（但未像狗一样完全地被驯化）。一般的猫：头圆、颜面部短，前肢五指，后肢四趾，趾端具锐利而弯曲的爪，爪能伸缩。夜行性。以伏击的方式猎捕其它动物，大多能攀援上树。猫的趾底有脂肪质肉垫，以免在行走时发出声响，捕猎时也不会惊跑鼠。行进时爪子处于收缩状态，防止爪被磨钝，在捕鼠和攀岩时会伸出来。"]
    data['token'] = '1'
    print(data)
    print(json.dumps(data,cls=DateEncoder))
    resp = requests.post(url, json.dumps(data,cls=DateEncoder))
    print(resp.content)
    resp = resp.json()
    print(resp)

def send_data_to_jumpIntoAssignTask_server():

    url = 'http://127.0.0.1:5000/api/entry/assignTask'
    data = {}
    data['taskId'] = 5
    data['token'] = '19980307'

    resp = requests.post(url, json.dumps(data))
    #print(resp.content)
    resp = resp.json()
    print(resp)

def send_data_to_startTask_server():

    url = 'http://127.0.0.1:5000/api/entry/startTask'
    data = {}
    data['taskId'] = 5
    data['resultFileType'] = 'pdf'
    data['member'] = [{"userId":8,"role":2,"subTaskId":[108,109,110,111,112]},{"userId":5,"role":2,"subTaskId":[116]}, {"userId":9,"role":3,"subTaskId":[115]},{"userId":6,"role":3,"subTaskId":[114]},{"userId":7,"role":3,"subTaskId":[113]}]

    resp = requests.post(url, json.dumps(data))
    #print(resp.content)
    resp = resp.json()
    print(resp)


def send_data_to_taskSplit_server():
    url = 'http://127.0.0.1:5000/api/entry/taskSplit'
    data = {}
    data['task_id'] = 5
    data['token'] = "19980307"
    data["subtask"] =[{"name":"新建词条","content":"新建3条词条","type":1,"money":500.00,"itemCount":5},{"name":"审核词条","content":"需要五个审核人员，审核词条,itemCount代表审核人员数量","type":3,"money":500.00,"itemCount":[1,2,2]},{"name":"完善词条","content":"完善初始化词条","type":2,"money":100.00,"itemCount":5,"inited_item_ids":[119]}]
    # 新的审核任务
    resp = requests.post(url, json.dumps(data))
    #print(resp.content)
    resp = resp.json()
    print(resp)

def send_data_to_changeTask_server():
    url = 'http://127.0.0.1:5000/api/entry/changeTask'
    data = {}
    data['taskId'] = 5
    data['DetailsTaskId'] = 111
    data['userID'] = 3
    data['userName'] = "jay"

    # 新的审核任务
    resp = requests.post(url, json.dumps(data))
    #print(resp.content)
    resp = resp.json()
    print(resp)

def send_data_to_getRate_server():

    url = 'http://127.0.0.1:5000/api/entry/getRate'
    data = {}
    data['taskId'] = 5
    resp = requests.post(url, json.dumps(data))
    resp = resp.json()
    print(resp)

def send_data_to_subTask_server():

    url = 'http://127.0.0.1:5000/api/entry/subTask'
    data = {}
    data['taskId'] = 5
    data['token'] = "19980101"
    resp = requests.post(url, json.dumps(data))
    resp = resp.json()
    print(resp)


def send_data_to_searchUserId_server():

    url = 'http://127.0.0.1:5000/inside_api/entry/searchUserId'
    data = {}
    data['taskId'] = 888
    data['userId'] = 4
    #data["JWT"] = 'eyJhbGciOiJIUzUxMiIsImlhdCI6MTYyMDIxMzM2OSwiZXhwIjoxNjIwMjE2OTY5fQ.eyJ1c2VyX2lkIjoxfQ.noCfpLGn2EBHYt5W2dcKlUCKAGPTy7ZfycPreDfYyyjqf3gJHlDk3PNynsREMA_Y14UL2agdHexbp6yO7fg3lA'
    test_user = User.query.get(3)
    inside_token = test_user.create_token()
    print(inside_token)
    headers = {'Authorization' : 'JWT '+ inside_token}
    resp = requests.post(url, headers=headers, data=json.dumps(data))
    print(resp.content)

    resp = resp.json()
    print(resp)

def send_data_to_updateEditItem_server():

    url = 'http://101.200.34.92:8081/api/inside/updateEditItem'
    data = {}
    data["item_id"] = 94
    data["original_id"] = 123
    data["name"] = "兽亚纲12345"
    data["relation"] = []
    data["field"] = []
    data["info_box"] = []
    data["intro"] = ""
    data["imageUrl"] = ""
    data["content"] = ""
    data["task_id"] = 1
    data["reference"] = []

    resp = requests.post(url, json.dumps(data))
    #print(resp.content)
    resp = resp.json()
    print(resp)

def send_data_to_userLogin_server():
    url = 'http://127.0.0.1:5000/inside_api/entry/userLogin'
    data = {}
    data['token'] = '1231212312'
    resp = requests.post(url, data=json.dumps(data))
    resp = resp.json()
    print(resp)


def send_data_to_huafentaskresult():
    headers = {}
    headers={"Content-Type": "application/json"}
    headers["token"] = "eyJhbGciOiJIUzI1NiJ9.eyJsb2dpblR5cGUiOjAsInVzZXIiOnsiY2VsZWJyaXR5Ijp0cnVlLCJpbWciOiJcL3Jlc291cmNlc1wvdHJhZGluZ1wvdXBsb2FkXC9qcGdcL2Q0MWI5YTRjLTBlZjktNDYxYy1hMGE5LWIxOWEyN2NkMzQwOC5qcGciLCJmaXJzdExhYmxlIjoi6K6h566X5py6IiwiYXJ0aWNsZU51bSI6MCwibGV2ZWwiOjAsIndkQWNjZXB0TnVtIjoyLCJ0aGlyZExhYmxlIjoi56eR5oqAIiwiaW5kdXN0cnkiOiLorqHnrpfmnLrnp5HlraYiLCJmdHBwYXRoIjoiQzpcL2Z0cFwvYWRtaW4iLCJpc0FkbWluIjoxLCJzZWNvbmRMYWJsZSI6IuadkOaWmSIsIm1vbmV5IjozMzUsInBob25lIjoiMTMxNTIxMzQwMDAiLCJjb25jZXJuTnVtIjoxLCJpbnRlZ3JhbCI6MTg2LCJsb2dpbk5hbWUiOiJkaiIsIm5hbWUiOiLkuIHpnIEiLCJ3ZEFuc3dlck51bSI6NSwiaWQiOjI2LCJlbWFpbCI6IjEyMzQxMjQ0NDVAcXEuY29tIn0sInJhbmRvbSI6IjIxMzMzZDFiLWIwZjktNDIzZS1iYTEzLTcxN2ExYjNkMzc5NyJ9.q1EHXZXsi7VKty5QGorNdqdLXAfEX0UDeTCJvPmP8hE"

    post_data = {}
    task_id = 5
    task = db_select_task_by_id(task_id)
    post_data["taskId"] = task.id
    post_data["taskName"] = task.name
    post_data["taskType"] = 3
    post_data["fzrId"] = task.user_id
    header = db_select_user_by_id(task.user_id)
    post_data["fzrName"] = header.name
    post_data["childTasks"] = []

    for sub in task.subtasks:
        t = {}
        t["childTaskId"] = sub.id
        t["childTaskName"] = sub.name
        t["childTaskDescribe"] = sub.content
        t["childTaskMoney"] = str(sub.money)
        t["childTaskDay"] = 10
        # t["jgUserId"] = sub.id
        # t["jgUserName"] = sub.id
        post_data["childTasks"].append(t)

    print(post_data)
    url = 'http://113.207.56.4:9527/common/huaFenTaskResult'
    resp = requests.post(url=url,headers=headers, data=json.dumps(post_data))
    resp = resp.json()
    print(resp)


if __name__ == '__main__':
    #send_data_to_http_server()
    #send_data_to_startAssignTask_server()
    #send_data_to_jumpIntoAssignTask_server()
    #send_data_to_startTask_server()
    #send_data_to_changeTask_server()
    #send_data_to_getRate_server()
    #send_data_to_subTask_server()

    get_item_info_from_gengxin_server()

    #send_data_to_taskSplit_server()
    #send_data_to_searchUserId_server()

    #send_data_to_updateEditItem_server()

    #send_data_to_userLogin_server()

    #send_data_to_huafentaskresult()

    #token = "eyJhbGciOiJIUzI1NiJ9.eyJsb2dpblR5cGUiOjAsInVzZXIiOnsiY2VsZWJyaXR5Ijp0cnVlLCJpbWciOiJcL3Jlc291cmNlc1wvdHJhZGluZ1wvdXBsb2FkXC9qcGdcL2Q0MWI5YTRjLTBlZjktNDYxYy1hMGE5LWIxOWEyN2NkMzQwOC5qcGciLCJmaXJzdExhYmxlIjoi6K6h566X5py6IiwiYXJ0aWNsZU51bSI6MCwibGV2ZWwiOjAsIndkQWNjZXB0TnVtIjoyLCJ0aGlyZExhYmxlIjoi56eR5oqAIiwiaW5kdXN0cnkiOiLorqHnrpfmnLrnp5HlraYiLCJmdHBwYXRoIjoiQzpcL2Z0cFwvYWRtaW4iLCJpc0FkbWluIjoxLCJzZWNvbmRMYWJsZSI6IuadkOaWmSIsIm1vbmV5IjozMzUsInBob25lIjoiMTMxNTIxMzQwMDAiLCJjb25jZXJuTnVtIjoxLCJpbnRlZ3JhbCI6MTg2LCJsb2dpbk5hbWUiOiJkaiIsIm5hbWUiOiLkuIHpnIEiLCJ3ZEFuc3dlck51bSI6NSwiaWQiOjI2LCJlbWFpbCI6IjEyMzQxMjQ0NDVAcXEuY29tIn0sInJhbmRvbSI6Ijk2OWQ1YTBkLTNmOTItNGYwNC04Y2ZlLTUwNzk4NjIyNTNkZCJ9.rj9PVyX0r05Nw_VLPJpD-F_YH7Eum3xLsrVB9eEVSOM"
    #print(outside_token_validation(token))