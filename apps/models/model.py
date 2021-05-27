from flask_sqlalchemy import SQLAlchemy
from flask import Flask
from .. import config
import json
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer

app = Flask(__name__)
app.config.from_object(config.Config)
db = SQLAlchemy(app)

class BaseModel(object):

    def save(self):
        """Saves the object to the database."""
        db.session.add(self)
        db.session.commit()
        return self

    def delete(self):
        """Delete the object from the database."""
        db.session.delete(self)
        db.session.commit()
        return self


class User(db.Model, BaseModel):

    __tablename__ = 'user'
    id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    name = db.Column(db.String(255),nullable=True)
    # 用户角色1 2 3 对应负责人、普通成员和审核成员
    role = db.Column(db.Integer, nullable=True)
    outside_token = db.Column(db.String(255))
    inside_token = db.Column(db.String(255),unique=True)
    subtasks = db.Column(db.String(255), default="[]")

    def __repr__(self):
        return '<User %r %r %r>' % (self.id, self.name, self.role)

    def serialization(self):
        return {
            "user_id": self.id,
            "name": self.name,
            "role": self.role,
            "outside_token": self.outside_token,
            "inside_token":self.inside_token
        }

    def add_subtask(self, subtaskId):
        if not subtaskId:
            return

        if not self.subtasks:
            self.subtasks = json.dumps(subtaskId)
        else:
            old = json.loads(self.subtasks)
            old = list(set(old + subtaskId))
            self.subtasks = json.dumps(old)
        db.session.commit()

    def remove_subtask(self, subtaskId):
        old = json.loads(self.subtasks)
        print(old)
        old.remove(subtaskId)
        print(old)
        self.subtasks = json.dumps(old)
        db.session.commit()

    def create_token(self):
        # 接收用户id转换与编码
        s = Serializer(config.Config.SECRET_KEY)
        token = s.dumps({"user_id": self.id}).decode('ascii')
        return token


class Task(db.Model, BaseModel):

    __tablename__ = 'task'
    id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    name = db.Column(db.String(255),nullable=False)
    description = db.Column(db.TEXT)
    reward = db.Column(db.DECIMAL(20,6),nullable=True)
    field = db.Column(db.String(255),nullable=True)
    document = db.Column(db.TEXT)
    user_id = db.Column(db.Integer,nullable=False)
    resultFileType = db.Column(db.String(30), nullable=True)
    # 一个任务对应多个子任务
    subtasks = db.relationship('Subtask', backref='task')
    items = db.relationship('Item', backref='task')
    # 是否初始化完毕，0代表未初始化，1代表已初始化
    hasInitialize = db.Column(db.Integer,default=0)

    def __repr__(self):
        return '<Task %r %r %r>' % (self.id, self.name, self.description)

    def serialization(self):
        return {
            "task_id":self.id,
            "name":self.name,
            "description":self.description,
            "reward":str(self.reward),
            "field":self.field,
            "document":self.document,
            "resultFileType":self.resultFileType,
            "hasInitialize":self.hasInitialize
        }

    def initialize(self):
        self.hasInitialize = 1
        self.save()

    def get_items(self):
        data = []
        for it in self.items:
            data.append(it.serialization())
        return data


class Subtask(db.Model, BaseModel):

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
    # 应聘负责人id
    user_id = db.Column(db.Integer)

    def __repr__(self):
        return '<Subtask %r %r %r %r>' % (self.id, self.name, self.content, self.task_id)

    def serialization(self):
        return {
            "subtask_id":self.id,
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
        self.save()


class Item(db.Model, BaseModel):

    __tablename__ = 'item'
    id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    name = db.Column(db.String(255),nullable=True)
    content = db.Column(db.TEXT, nullable=True)
    imageUrl = db.Column(db.String(255), nullable=True)
    # 0 空状态  1 初始化状态 2 待编辑状态 3 待审核状态 4 审核未通过状态 5 已审核状态
    status = db.Column(db.Integer, nullable=False)
    isInitialize = db.Column(db.Integer, default=0)
    field = db.Column(db.String(255), nullable=True, default="[]")
    info_box = db.Column(db.TEXT, nullable=True, default="[]")
    intro = db.Column(db.TEXT, default="")
    original_id = db.Column(db.Integer)
    relation = db.Column(db.TEXT, default="[]")
    reference = db.Column(db.TEXT, default="[]")
    task_id = db.Column(db.Integer, db.ForeignKey('task.id'))
    has_selected_supply = db.Column(db.Integer, default=0)

    def __repr__(self):
        return '<Item %r %r %r %r>' % (self.id, self.name, self.status, self.task_id)

    def serialization(self):
        return {
            "item_id":self.id,
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
            "relation":json.loads(self.relation),
            "reference": json.loads(self.reference),
            "has_selected_supply":self.has_selected_supply
        }


class Validator_Item_Mapping(db.Model, BaseModel):

    __tablename__ = 'validator_item_mapping'
    id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    item_id = db.Column(db.Integer)
    user_id = db.Column(db.Integer)
    task_id = db.Column(db.Integer)
    # 审核结果 ，0驳回，1通过，
    result = db.Column(db.Integer,nullable=True)
    # 审核意见
    content = db.Column(db.TEXT, nullable=True)

    def __repr__(self):
        return '<Item %r %r %r %r %r>' % (self.id, self.user_id, self.item_id, self.result, self.content)


if __name__ == '__main__':
    # db.drop_all()
    # db.create_all()
    pass
