from services import *

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

    # taskId = 2
    # resultFileType = 'pdf'
    # member = [{"userId":3,"role":2,"subTaskId":[3]},{"userId":4,"role":2,"subTaskId":[3]},{"userId":7,"role":3,"subTaskId":[4]}]
    #
    # test_startTask(taskId, resultFileType, member)

    #test_jumpIntoAssignTask(2, "19980308")

    test_getRate(1)
