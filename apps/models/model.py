from flask_sqlalchemy import SQLAlchemy
from flask import Flask
import pymysql
from .. import config
import json
import datetime

app = Flask(__name__)
app.config.from_object(config.Config)
db = SQLAlchemy(app)

# 用户、子任务映射表，多对多关系， 注意是大写Table不是小写！！！！！！！
# user_subtask_mapping = db.Table('user_subtask_mapping',
#                                      # db.Column('usid',db.Integer,primary_key=True, autoincrement=True),
#                                      db.Column('user_id',db.Integer,db.ForeignKey('user.id')),
#                                      db.Column('subtask_id',db.Integer, db.ForeignKey('subtask.id'))
#                                      # ,db.Column('status',db.Integer,nullable=False,default=1)
#                                      )

# 词条、子任务映射表，多对多关系， 注意是大写Table不是小写！！！！！！！
# item_subtask_mapping = db.Table('item_subtask_mapping',
#                                      # db.Column('usid',db.Integer,primary_key=True, autoincrement=True),
#                                      db.Column('item_id',db.Integer,db.ForeignKey('item.id')),
#                                      db.Column('subtask_id',db.Integer, db.ForeignKey('subtask.id'))
#                                      # ,db.Column('status',db.Integer,nullable=False,default=1)
#                                      )

class User(db.Model):
    __tablename__ = 'user'
    id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    name = db.Column(db.String(255),nullable=True)
    # 用户角色1 2 3 对应负责人、普通成员和审核成员
    role = db.Column(db.Integer, nullable=False)
    token = db.Column(db.String(255),nullable=False,unique=True)
    # 一个用户可以完成多个子任务
    #subtasks = db.relationship('Subtask', secondary=user_subtask_relationship, back_populates=db.backref('users'))
    def __repr__(self):
        return '<User %r %r %r %r>' % (self.id, self.name, self.role, self.token)

    def serialization(self):
        return {
            "id": self.id,
            "name": self.name,
            "role": self.role,
            "token": self.token
        }

class Item(db.Model):
    __tablename__ = 'item'
    id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    name = db.Column(db.String(255),nullable=True)
    content = db.Column(db.TEXT, nullable=True)
    imageUrl = db.Column(db.String(255), nullable=True)
    status = db.Column(db.Integer, nullable=False) # 1 2 3 已创建 已完成 已审核
    isInitialize = db.Column(db.Integer)
    # 0 刚创建， 1已初始化  2 待完善 3 等待审核中 4 通过审核 5 未审核通过，需要继续编辑
    # 0 空状态  1 初始化状态 2 待编辑状态 3 待审核状态 4 审核未通过状态 5 已审核状态
    field = db.Column(db.String(255))
    info_box = db.Column(db.TEXT)
    intro = db.Column(db.TEXT)
    original_id = db.Column(db.Integer)
    relation = db.Column(db.TEXT)
    task_id = db.Column(db.Integer, db.ForeignKey('task.id'))

    # 外键
    #subtask_id = db.Column(db.Integer,db.ForeignKey('subtask.id'))

    def __repr__(self):
        return '<Item %r %r %r %r>' % (self.id, self.name, self.status, self.task_id)

    def serialization(self):
        return {
            "id":self.id,
            "name":self.name,
            "content":self.content,
            "imageUrl":self.imageUrl,
            "status":self.status,
            "field":json.loads(self.field),
            "info_box":json.loads(self.info_box),
            "isInitialize": self.isInitialize,
            "original_id": self.original_id,
            "task_id":self.task_id,
            "intro":self.intro,
            "relation":json.loads(self.relation)
        }

class Validator_Item_Mapping(db.Model):
    __tablename__ = 'validator_item_mapping'
    id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    item_id = db.Column(db.Integer, autoincrement=True)
    user_id = db.Column(db.Integer, autoincrement=True)

    # 审核结果 ，0驳回，1通过，
    result = db.Column(db.Integer,nullable=True)
    # 审核意见
    content = db.Column(db.TEXT, nullable=True)

    def __repr__(self):
        return '<Item %r %r %r %r %r>' % (self.id, self.user_id, self.item_id, self.result, self.content)

class Task(db.Model):
    __tablename__ = 'task'
    id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    name = db.Column(db.String(255),nullable=False)
    description = db.Column(db.TEXT)
    # 需求存json串, 测试一下BLOB类型
    #demand = db.Column(db.BLOB,nullable=True)
    # 注意时间要求是截止时间
    timeDemand = db.Column(db.DateTime)
    createTime = db.Column(db.DateTime,default=datetime.datetime.now)
    subtaskDemand = db.Column(db.Integer)
    teamDemand = db.Column(db.String(255))


    reward = db.Column(db.DECIMAL(20,6),nullable=True)
    field = db.Column(db.String(255),nullable=True)
    # 文档可能要存Json
    document = db.Column(db.TEXT)
    token = db.Column(db.String(255),nullable=False)
    resultFileType = db.Column(db.String(30), nullable=True)
    # 一个任务对应多个子任务
    subtasks = db.relationship('Subtask', backref='task')
    items = db.relationship('Item', backref='task')

    # 是否初始化完毕，0代表未初始化，1代表已初始化
    hasInitialize = db.Column(db.Integer,default=0)

    def __repr__(self):
        return '<Task %r %r %r %r>' % (self.id, self.name, self.description, self.token)

    def serialization(self):
        #print(type(self.reward))
        return {
            "id":self.id,
            "headId":self.get_header_id(),
            "name":self.name,
            "description":self.description,
            #"demand":json.loads(self.demand),
            "timeDemand": self.timeDemand,
            "subtaskDemand": self.subtaskDemand,
            "teamDemand": self.teamDemand,
            "reward":str(self.reward),
            "field":self.field,
            "document":self.document,
            "token":self.token,
            "resultFileType":self.resultFileType,
            "hasInitialize":self.hasInitialize
        }

    def get_header_id(self):
        header = User.query.filter(User.token==self.token).first()
        if header:
            return header.id
        else:
            return None

    def initialize(self):
        self.hasInitialize = 1
        db.session.commit()

    def get_items(self):
        data = []
        for it in self.items:
            data.append(it.serialization())
        return data


class Subtask(db.Model):
    __tablename__ = 'subtask'
    id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    name = db.Column(db.String(255),nullable=True)
    content = db.Column(db.TEXT, nullable=True)
    money = db.Column(db.DECIMAL(20,6),nullable=True)
    type = db.Column(db.Integer,nullable=False)
    itemCount = db.Column(db.Integer, nullable=True)
    # 外键
    task_id = db.Column(db.Integer, db.ForeignKey('task.id'))
    # 外键
    item_id = db.Column(db.Integer)
    user_id = db.Column(db.String(255))


    # 一个子任务包含多个词条
    #items = db.relationship('Item', secondary=item_subtask_mapping, backref='subtask',lazy='dynamic')
    # 一个子任务可以由多个人完成, 多对多关系
    #users = db.relationship('User', secondary=user_subtask_mapping, backref='subtask',lazy='dynamic')

    def __repr__(self):
        return '<Subtask %r %r %r %r>' % (self.id, self.name, self.content, self.task_id)

    def serialization(self):
        return {
            "id":self.id,
            "name":self.name,
            "content":self.content,
            "money":str(self.money),
            "type":self.type,
            "itemCount":self.itemCount
        }

    def add_user(self, uid):
        if not self.user_id:
            self.user_id = json.dumps([uid])
        else:
            old = json.loads(self.user_id)
            old.append(uid)
            self.user_id = json.dumps(old)
        db.session.commit()

if __name__ == '__main__':
    # db.drop_all()
    # db.create_all()
    pass
