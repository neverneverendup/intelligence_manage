from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from models import Config

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

# 配置数据库信息
# apps.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:mysql@127.0.0.1/student_course'
# apps.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False


# 多对多模型需要添加一张单独的表去记录两张表之间的对应关系
tb_student_course = db.Table('tb_student_course',
                             db.Column('student_id', db.Integer, db.ForeignKey('students.id')),
                             db.Column('course_id', db.Integer, db.ForeignKey('courses.id'))
                             )


# 创建学生表
class Students(db.Model):
    __tablename__ = 'students'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), unique=True)


# 创建课程表
class Course(db.Model):
    __tablename__ = 'courses'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), unique=True)
    # 在任意一个模型中添加关系引用
    students = db.relationship('Students',
                               secondary=tb_student_course,  #### 引用实例对象，不加引号
                               backref='courses',
                               lazy='dynamic')

if __name__ == '__main__':
    db.drop_all()
    db.create_all()

    # 添加测试数据

    stu1 = Students(name='张三')
    stu2 = Students(name='李四')
    stu3 = Students(name='王五')

    cou1 = Course(name='物理')
    cou2 = Course(name='化学')
    cou3 = Course(name='生物')

    stu1.courses = [cou2, cou3]
    stu2.courses = [cou2]
    stu3.courses = [cou1, cou2, cou3]

    db.session.add_all([stu1, stu2, stu2])
    db.session.add_all([cou1, cou2, cou3])

    db.session.commit()
