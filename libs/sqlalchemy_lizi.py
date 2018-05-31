# 使用mysql 需要pip mysql-connector-python 模块
# 然后引入 SQLAlchemy框架进行接入数据库
# 导入:
from sqlalchemy import Column, String, create_engine, Integer,Table, MetaData
from sqlalchemy.orm import sessionmaker, mapper
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.types import INTEGER

# http://blog.csdn.net/fgf00/article/details/52949973 数据库相关教程


# 创建orm基类
SQLAtiveBase = declarative_base()
# 初始化数据库连接:
SQLCreateEngine = create_engine('mysql+mysqlconnector://root:szy920514@localhost:3306/NewPro', encoding='utf-8')
# 创建DBSession类型:
SQLDBSession = sessionmaker(bind=SQLCreateEngine)
# # 创建sesion对象，他用来操作数据
session = SQLDBSession()

# 第一种数据绑定方法
# 数据类型和数据绑定 需要继承orm
class User(SQLAtiveBase):

    __tablename__ = 'user'  # 表名

    id = Column(Integer, primary_key=True)
    name = Column(String(32))
    password = Column(String(64))

    def __init__(self,newName,newPass):
        self.name = newName
        self.password = newPass


# 第二种数据绑定方法 MetaData() 数据表名 类型
userTable = Table('user', MetaData(),
            Column('id', Integer, primary_key=True),
            Column('name', String(50)),
            Column('password', String(12))
        )

class User2(object):

    def __init__(self,newName,newPass):
        self.name = newName
        self.password = newPass
#      @property 是把方法可以当成属性进行调用
    @property
    def id(self,value):
        pass

# 类User 和 表user关联起来
mapper(User2, userTable)


def installData():

    newUser = User(newName="hahahhapython",newPass="1234556")
    # newUser.name = "nnnn"
    # newUser.password = "gdsgsdgdsgs"
# 将对象添加到session
    session.add(newUser)
# 通过session提交到数据库
    session.commit()
    session.close()

# SqlativeBase.metadata.create_all(SqlCreateEngine)  # 创建表结构 （这里是父类调子类）
# #
#
#


