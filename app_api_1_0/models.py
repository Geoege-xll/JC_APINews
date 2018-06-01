from app_api_1_0 import db


# https://blog.csdn.net/hyman_c/article/details/54382161  分页处理
# https://blog.csdn.net/guoqianqian5812/article/details/78860572  分页处理


# 认证类模型
class CertifiedModel(db.Model):
    __tablename__ = 'Certified'  # 表名

    CertifiedId = db.Column(db.String, primary_key=True)
    CertifiedUserId = db.Column(db.Integer)
    ManagementId = db.Column(db.Integer)
    State = db.Column(db.Integer)
    Title = db.Column(db.String)
    Content = db.Column(db.String)
    SendTime = db.Column(db.String)
    CertifiedTime = db.Column(db.String)
    CertifiedType = db.Column(db.Integer)


# 文章类模型
class ContentModel(db.Model):
    __tablename__ = 'Content'  # 表名

    ContentId = db.Column(db.String, primary_key=True)
    ReleaseTime = db.Column(db.Integer)
    ReleasePeopleId = db.Column(db.Integer)
    ContentTitle = db.Column(db.String)
    PhoneNum = db.Column(db.String)
    weixinId = db.Column(db.String)
    ContentHtml = db.Column(db.String)
    ContentString = db.Column(db.String)

    def toJson(self):
        jsonDic = {
            'ContentId': self.ContentId,
            'ReleaseTime': self.ReleaseTime,
            'ReleasePeopleId': self.ReleasePeopleId,
            'ContentTitle': self.ContentTitle,
            'ReleasePeopleName': self.ReleasePeopleName,
            'ReleasePeopleCompany': self.ReleasePeopleCompany,
            'PhoneNum': self.PhoneNum,
            'weixinId': self.weixinId,

        }
        return jsonDic


# 用户
class UserModel(db.Model):
    # 表名
    __tablename__ = 'User'  # 表名

    UserId = db.Column(db.Integer)
    UserName = db.Column(db.Integer)
    PassWord = db.Column(db.Integer)
    Token = db.Column(db.Integer)
    Name = db.Column(db.Integer, nullable=True)
    ID = db.Column(db.Integer, primary_key=True)

    r'''
        返回json的方法
       # 1、建立一个属性是为 db.PickleType
    # user_info = db.Column(db.PickleType)
     # 2、

     # 返回json 第一种方法
    def __repr__(self):
        print('---------', self.ID)

        return self.user_info
     3.   
    USER = Users(user_info={"UserId":"nisiwa", "UserName":"范德萨范德萨"})
    db.session.add(USER)
    db.session.add(STUDENT)ddd
    db.session.commit()

    '''

    def __init__(self, newName, newPass, newToken):
        self.UserName = newName
        self.PassWord = newPass
        self.Token = newToken

    # 返回json 第二种方法
    def to_json(self):
        json_student = {
            'student_id': self.user_id,
        }
        return json_student


# 用户详情
class UserDetailModel(db.Model):
    __tablename__ = 'UserDetail'  # 表名

    UserId = db.Column(db.Integer, primary_key=True)
    UserType = db.Column(db.Integer)
    IDNum = db.Column(db.String(64))
    Sex = db.Column(db.String)
    Adress = db.Column(db.String(64))
    CompanyId = db.Column(db.String)
    CompanyUserType = db.Column(db.Integer)
    PhoneNum = db.Column(db.String)
    Name = db.Column(db.String)
    Age = db.Column(db.Integer)
    State = db.Column(db.Integer)
    CompanyName = db.Column(db.String)
    Birthday = db.Column(db.String)
    Education = db.Column(db.String)
    UserImageUrl = db.Column(db.String)

    def __init__(self, kUserId):
        self.UserId = kUserId


# 关注表
class AttebtonModel(db.Model):
    __tablename__ = "Attention"

    Id = db.Column(db.Integer, default=0, primary_key=True)
    FollowersUserId = db.Column(db.String)
    B_FollowersUserId = db.Column(db.String)
    FollowersTime = db.Column(db.String)

    def __init__(self):
        pass
