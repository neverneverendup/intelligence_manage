

class Config(object):
    user = 'gzy'
    password = 'buaanlp'
    database = 'gzy_test_db'
    SQLALCHEMY_DATABASE_URI = 'mysql://%s:%s@101.200.34.92:3306/%s' %(user, password, database)
    # 设置sqlalchemy自动更跟踪数据库
    SQLALCHEMY_TRACK_MODIFICATIONS = True
    # 查询时会显示原始SQL语句
    SQLALCHEMY_ECHO = True
    # 禁止自动提交数据处理
    SQLALCHEMY_COMMIT_ON_TEARDOWN = False

    SECRET_KEY = '123456'