from apps.services.outServices import *

def test_subTask(taskId, token):
    json_data = subTask(taskId, token)
    print(json_data)

# view接收的是json数据，需要解析json数据再传值
def test_startTask(taskId, resultFileType, member):
    json_data = startTask(taskId, resultFileType, member)
    print(json_data)

def test_jumpIntoAssignTask(taskId, token):
    json_data = jumpIntoAssignTask(taskId, token)
    print(json_data)

def test_getRate(taskId):
    json_data = getRate(taskId)
    print(json_data)

if __name__ == '__main__':
    #test_subTask(1, "19980307")


    #subtask = {["name":"新建词条","content":"新建3条词条","type":1,"money":500.00,"itemCount":3},{"name":"审核词条","content":"需要五个审核人员，审核词条,itemCount代表审核人员数量","type":3,"money":500.00,"userCount":5},{"name":"完善词条","content":"完善初始化词条","type":2,"money":100.00,"itemCount":5,"inited_item_ids":[17, 18]}]
    #print(taskSplit(8888, "19980307", subtask))

    # taskId = 8888
    # resultFileType = 'pdf'
    # member = [{"userId":3,"role":2,"subTaskId":[28, 29]},{"userId":4,"role":2,"subTaskId":[30,32,33]},{"userId":6,"role":3,"subTaskId":[31]},{"userId":7,"role":3,"subTaskId":[31]}]
    #
    # test_startTask(taskId, resultFileType, member)

    #test_jumpIntoAssignTask(2, "19980308")
    #test_getRate(1)


    startAssignTask()