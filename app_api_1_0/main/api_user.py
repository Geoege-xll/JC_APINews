import time, json
from flask import request
from libs.api_extended import generate_token, AlchemyEncoder, kResponseJosn, token_key, singlerandom, \
    classTodic

from app_api_1_0 import db
from app_api_1_0.models import UserModel, UserDetailModel
from app_api_1_0.models import CertifiedModel
from app_api_1_0.main.user_help import kCheckUser

from . import main


@main.route('/api/1.0/hello', methods=['POST'])
def printHello():
    request.form.get("key", type=str, default=None)
    # 获取表单数据
    request.args.get("key")
    # 获取get请求参数
    request.values.get("key")
    # 获取所有参数
    request.json.get("key")
    # 获取json参数
    return kResponseJosn(code=200, codeString="hello word")


@main.route('/api/1.0/login', methods=['POST'])
def login():
    """
    登录
    :return:
    """
    print("--------------", request.json)

    username = request.json.get('UserName')
    password = request.json.get('PassWord')
    if username is None or password is None:
        # abort(400)  # missing arguments
        return kResponseJosn(code=400, codeString="请输入账号密码！")

    my_user = db.session.query(UserModel).filter_by(UserName=username).first()  # 查询第一个
    print(my_user)
    if my_user is None:
        return kResponseJosn(code=400, codeString="该用户没注册！")

    if my_user.UserName == username and my_user.PassWord == password:
        print("=============", json.dumps(my_user, cls=AlchemyEncoder))
        newToken = generate_token(token_key, 3600)

        returndic = {
            "Token": newToken,
            "UserName": username,
            "UserId": my_user.UserId
        }

        my_user.Token = newToken
        db.session.add(my_user)
        try:
            db.session.commit()
        except:
            db.session.rollback()
        db.session.close()

        # return kResponseJosn(code=200, codeString="登录成功", obj= json.dumps(my_user, cls=AlchemyEncoder))
        return kResponseJosn(code=200,
                             codeString="登录成功",
                             obj=returndic)




@main.route('/api/1.0/registered', methods=['POST'])
def registered():
    """
    注册
    :return:
    """
    username = request.json.get('UserName')
    password = request.json.get('PassWord')
    if username is None or password is None:
        # abort(400)  # missing arguments
        return "缺少参数"
    else:
        find_my_user = db.session.query(UserModel).filter_by(UserName=username).first()  # 查询第一个

        # a = User.query.paginate(1, per_page=10)

        if find_my_user is None:

            returnTorn = generate_token(token_key, 3600)

            install_user = UserModel(newName=username, newPass=password, newToken=returnTorn)
            install_user.UserId = int(time.time())  # 生成时间戳
            db.session.add(install_user)
            try:
                db.session.commit()  # 提交到数据库
            except:
                db.session.rollback()  # 回滚
            db.session.close()
            return kResponseJosn(code=200, codeString="注册成功！", obj={"Token": returnTorn})

        else:
            return kResponseJosn(code=500, codeString="注册失败！已经存在该用户")


@main.route('/api/1.0/addUserDetail', methods=['POST'])
def addUserDetail():
    """
    完善用户信息或修改用户信息
    :return:
    """

    Token = request.json.get("Token")
    UserId = request.json.get('UserId')

    Name = request.json.get("Name")
    Birthday = request.json.get("Birthday")
    Adresss = request.json.get("Adress")
    Sex = request.json.get("Sex")
    PhoneNum = request.json.get("PhoneNum")
    CompanyName = request.json.get("CompanyName")
    Education = request.json.get("Education")
    Age = request.json.get("Age")

    # UserType = request.json.get('UserType')
    # CompanyId = request.json.get("CompanyId")
    # CompanyUserType = request.json.get("CompanyUserType")
    # IDNum = request.json.get("IDNum")

    if UserId is None or Token is None:
        return kResponseJosn(code='500', codeString="缺少参数")

    if kCheckUser(userId=UserId, token=Token):

        find_my_user = db.session.query(UserDetailModel).filter_by(UserId=UserId).first()  # 查询第一个

        if find_my_user is None:

            newUserd = UserDetailModel(kUserId=UserId)
            newUserd.Sex = Sex
            newUserd.Adress = Adresss
            newUserd.PhoneNum = PhoneNum
            newUserd.State = 0
            newUserd.CompanyName = CompanyName
            newUserd.Name = Name
            newUserd.Birthday = Birthday
            newUserd.Education = Education
            newUserd.Age = Age

            # newUserd.UserType = UserType
            # newUserd.IDNum = IDNum
            # newUserd.CompanyId = CompanyId
            # newUserd.CompanyUserType = CompanyUserType

            db.session.add(newUserd)
            try:
                db.session.commit()
            except:
                db.session.rollback()
            db.session.close()
            return kResponseJosn(code=200, codeString="完善信息成功！")
        else:

            find_my_user.PhoneNum = PhoneNum
            find_my_user.State = 0
            find_my_user.CompanyName = CompanyName
            find_my_user.Name = Name
            find_my_user.Birthday = Birthday
            find_my_user.Sex = Sex
            find_my_user.Adress = Adresss
            find_my_user.Education = Education
            find_my_user.Age = Age

            # find_my_user.UserType = UserType
            # find_my_user.IDNum = IDNum
            # find_my_user.CompanyId = CompanyId
            # find_my_user.CompanyUserType = CompanyUserType

            db.session.add(find_my_user)
            # db.session.commit()

            try:
                db.session.commit()
            except:
                db.session.rollback()
            db.session.close()

            return kResponseJosn(code=200, codeString="修改信息成功！")

    return kResponseJosn(code="900", codeString="token 无效！")


@main.route('/api/1.0/getUserDetail', methods=['POST'])
def getUserDetail():
    """
    获取用户详情
    :return:
    """
    token = request.json["Token"]
    userid = request.json["UserId"]

    if kCheckUser(userId=userid, token=token):

        find_my_user = db.session.query(UserDetailModel).filter_by(UserId=userid).first()  # 查询第一个
        if find_my_user:

            return kResponseJosn(code=200, codeString="用户信息查询成功！", obj=classTodic(find_my_user))
        else:
            return kResponseJosn(code=400, codeString="该用户没有用户信息！")


@main.route('/api/1.0/certifiedUser', methods=['POST'])
def certifiedUser():
    """
    实名认证企业高管信息信息
    :return:
    """

    Token = request.json.get("Token")
    UserId = request.json.get('UserId')
    BossId = request.json.get('BossId')  # 上级领导的id
    UserType = request.json.get('UserType')

    if kCheckUser(userId=UserId, token=Token):
        #
        find_boss_user = db.session.query(UserDetailModel).filter_by(UserId=BossId).first()  # 查询上级的状态是否正常

        print(find_boss_user.CompanyUserType)
        print(find_boss_user.State)

        if int(find_boss_user.CompanyUserType) == 1 and int(find_boss_user.State) == 1:

            '''
            将请求认证人的信息状态 临时存起来
            '''
            find_my_user = db.session.query(UserDetailModel).filter_by(UserId=UserId).first()
            find_my_user.UserType = UserType
            find_my_user.CompanyUserType = UserType
            find_my_user.State = 2
            db.session.add(find_my_user)
            try:
                db.session.commit()
            except:
                db.session.rollback()
            '''
            插入一条验证消息
            '''
            install_certif = CertifiedModel()
            install_certif.SendTime = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())
            install_certif.Title = "您有一条请求认证消息！"
            install_certif.CertifiedId = singlerandom(12)
            install_certif.CertifiedUserId = UserId
            install_certif.ManagementId = BossId
            install_certif.State = 0
            install_certif.CertifiedType = UserType
            db.session.add(install_certif)
            try:
                db.session.commit()
            except:
                db.session.rollback()

            db.session.close()
            '''
            这还得做个推送处理
            '''

            return kResponseJosn(code=200, codeString="申请认证成功！等待领导确定")
        else:
            return kResponseJosn(codeString="无效申请", code=400)

    return kResponseJosn(code="900", codeString="token 无效！")


@main.route('/api/1.0/fixCertifiedUser', methods=['POST'])
def fixCertifiedUser():
    """
    上级给下级审核确定认证
    :return: MTUyNjk1OTk0Ni41OTg0MTQyOjFjNGU3ODgyNGM1MWQxNDlmNWU1OTM2OWQ2YjkxOWQ0OGJlMTJmMWM=
    """
    Token = request.json.get('Token')
    CertifiedId = request.json.get('CertifiedId')
    UserId = request.json.get('UserId')

    if kCheckUser(userId=UserId, token=Token):

        # 找到该条验证消息
        find_cer = db.session.query(CertifiedModel).filter_by(CertifiedId=CertifiedId).first()
        # 验证登录用户和 该条验证消息 审核人的是否一致
        if find_cer.State != 0:
            return kResponseJosn(code=400, codeString="该条认证信息有问题！")

        if int(UserId) == find_cer.ManagementId:
            find_User = db.session.query(UserDetailModel).filter_by(UserId=UserId).first()
            # 看看确定验证申请人的权限是否问题
            if find_User.CompanyUserType < find_cer.CertifiedUserId:
                # 更改申请人的认证状态
                find_cerUser = db.session.query(UserModel).filter_by(UserId=find_cer.CertifiedUserId).first()
                find_cerUser.State = 1
                db.session.add(find_cerUser)

                find_cer.State = 1
                db.session.add(find_cer)
                try:
                    db.session.commit()
                except:
                    db.session.rollback()

                db.session.close()

                '''
                还需要做个推送处理
                '''
                return kResponseJosn(codeString='认证成功', code=200)


            else:
                return kResponseJosn(code=400, codeString="审核权限不正确")
        else:
            return kResponseJosn(code=400, codeString='审核人身份有问题！')
    else:
        return kResponseJosn(code=500)


class APIUser:

    def __init__(self):
        pass
