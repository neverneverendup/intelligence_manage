
from apps.services.modelsCRUD import *


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

    task = db_select_task_by_id(1)
    print(task, task.hasInitialize)
    task.initialize()
    print(task.hasInitialize)

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

    #print(db_select_item_by_id(25).serialization())