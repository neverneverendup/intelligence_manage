from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import pymysql

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

class Role(db.Model):
    # 定义表名
    __tablename__ = 'roles'
    # 定义字段
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(64), unique=True)
    users = db.relationship('User', backref='role')  # 反推与role关联的多个User模型对象

class User(db.Model):
    __tablename__ = 'user'
    # 定义字段
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(64), unique=True, index=True,nullable=True)
    #demand = db.Column(db.JSON,nullable=False)
    roid_id = db.Column(db.Integer, db.ForeignKey('roles.id'))


if __name__ == '__main__':
    # 根据model创建数据库表
    db.drop_all()
    db.create_all()

    # 插入数据，需要通过会话db.session提交才会改变数据库
    # role1 = Role(name='user')
    # db.session.add(role1)
    # db.session.commit()
    #
    # user1 = User(name='jey', roid_id=role1.id)
    # db.session.add(user1)
    # db.session.commit()

    # 查询操作
    # 精确查找
    # users = User.query.filter_by(name='t').all()
    # print(users)
    # for u in users:
    #     print(u.id, u.name)
    #
    # print(User.query.first())
    # print(User.query.all())
    # print(User.query.get(1))
