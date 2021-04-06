from flask_sqlalchemy import SQLAlchemy
from flask import Flask
import pymysql
import json

app = Flask(__name__)
class Config(object):
    user = 'gzy'
    password = 'buaanlp'
    database = 'gzy_test_db'
    app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://%s:%s@101.200.34.92:3306/%s' %(user, password, database)
    # 设置sqlalchemy自动更跟踪数据库
    SQLALCHEMY_TRACK_MODIFICATIONS = True
    # 查询时会显示原始SQL语句
    app.config['SQLALCHEMY_ECHO'] = True
    # 禁止自动提交数据处理
    app.config['SQLALCHEMY_COMMIT_ON_TEARDOWN'] = False

app.config.from_object(Config)
db = SQLAlchemy(app)

# 用户、子任务映射表，多对多关系， 注意是大写Table不是小写！！！！！！！
user_subtask_mapping = db.Table('user_subtask_mapping',
                                     # db.Column('usid',db.Integer,primary_key=True, autoincrement=True),
                                     db.Column('user_id',db.Integer,db.ForeignKey('user.id')),
                                     db.Column('subtask_id',db.Integer, db.ForeignKey('subtask.id'))
                                     # ,db.Column('status',db.Integer,nullable=False,default=1)
                                     )

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
            "status":self.status
        }

class Task(db.Model):
    __tablename__ = 'task'
    id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    name = db.Column(db.String(255),nullable=False)
    description = db.Column(db.TEXT)
    # 需求存json串, 测试一下BLOB类型
    demand = db.Column(db.BLOB,nullable=True)
    reward = db.Column(db.DECIMAL(20,6),nullable=True)
    field = db.Column(db.String(255),nullable=True)
    # 文档可能要存Json
    document = db.Column(db.TEXT)
    token = db.Column(db.String(255),nullable=False)
    resultFileType = db.Column(db.String(30), nullable=True)
    # 一个任务对应多个子任务
    subtasks = db.relationship('Subtask', backref='task')
    items = db.relationship('Item', backref='task')

    def __repr__(self):
        return '<Task %r %r %r %r>' % (self.id, self.name, self.description, self.token)

    def serialization(self):
        print(type(self.reward))
        return {
            "id":self.id,
            "name":self.name,
            "description":self.description,
            "demand":json.loads(self.demand),
            "reward":str(self.reward),
            "field":self.field,
            "document":self.document,
            "token":self.token,
            "resultFileType":self.resultFileType
        }

class Subtask(db.Model):
    __tablename__ = 'subtask'
    id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    name = db.Column(db.String(255),nullable=False)
    content = db.Column(db.TEXT, nullable=True)
    money = db.Column(db.DECIMAL(20,6),nullable=True)
    type = db.Column(db.Integer,nullable=False)
    itemCount = db.Column(db.Integer, nullable=False)
    # 外键
    task_id = db.Column(db.Integer, db.ForeignKey('task.id'))
    # 一个子任务包含多个词条
    #items = db.relationship('Item', secondary=item_subtask_mapping, backref='subtask',lazy='dynamic')
    # 一个子任务可以由多个人完成, 多对多关系
    users = db.relationship('User', secondary=user_subtask_mapping, backref='subtask',lazy='dynamic')



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

if __name__ == '__main__':
    # db.drop_all()
    # db.create_all()
    pass
