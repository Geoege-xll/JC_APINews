from app_api_1_0.main.user_help import kCheckUser
from app_api_1_0 import db
from app_api_1_0.models import ContentModel, UserDetailModel, AttebtonModel
from libs.api_extended import singlerandom, kResponseJosn, classTodic

from flask import request

import time
from . import main


@main.route('/api/1.0/writeContent', methods=['POST'])
def writeContent():
    '''
    写文章
    :return:
    '''

    Token = request.json.get('Token')
    qReleasePeopleId = request.json.get("UserId")
    qContentTitle = request.json.get('ContentTitle')
    qContentBox = request.json.get("HTMLString")
    qContentStr = request.json.get("ContentString")

    qContentId = singlerandom(16)
    qReleaseTime = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())

    if not kCheckUser(userId=qReleasePeopleId, token=Token):
        return kResponseJosn(code=500, codeString="token 无效")

    find_User = db.session.query(UserDetailModel).filter_by(UserId=qReleasePeopleId).first()

    if find_User.UserType != 1:
        kResponseJosn(code=500, codeString="您的权限不是供应商身份不能发布文章！")

    installContent = ContentModel()
    installContent.ContentId = qContentId
    installContent.ReleaseTime = qReleaseTime
    installContent.ContentTitle = qContentTitle
    installContent.ReleasePeopleId = qReleasePeopleId
    installContent.ContentHtml = qContentBox
    installContent.ContentString = qContentStr

    db.session.add(installContent)
    try:
        db.session.commit()
    except:
        pass
        # db.session.rollback()
    db.session.close()

    return kResponseJosn(code=200, codeString='文章发布成功！')


@main.route('/api/1.0/getContList', methods=['POST'])
def getContList():
    '''
    获取app首页文章列表，后期添加 类目筛选等 目前分页获取全部
    :return:
    '''

    page = request.json.get('Page')
    pageSize = request.json.get('PageSize')
    token = request.json.get('Token')
    userid = request.json.get('UserId')
    # 利用flask 进行分页查询
    if kCheckUser(userId=userid, token=token):

        pagination = ContentModel.query \
            .order_by(ContentModel.ReleaseTime.desc()) \
            .paginate(int(page), per_page=int(pageSize), error_out=False)

        posts = pagination.items
        tList = []

        for t in posts:
            find_my_user = db.session.query(UserDetailModel).filter_by(UserId=t.ReleasePeopleId).first()

            dic = {
                "ContentTitle": t.ContentTitle,
                "ReleaseTime": t.ReleaseTime,
                "ContentId": t.ContentId,
                "Content": t.ContentString,
                "UserHeader": find_my_user.UserImageUrl,
                "Name": find_my_user.Name,
                "CompanyName": find_my_user.CompanyName
            }
            tList.append(dic)
            
        return kResponseJosn(code=200, codeString="查询成功！", obj=tList)
    else:
        return kResponseJosn(code=500, codeString="无效Token")


@main.route('/api/1.0/getContentDetail', methods=['POST'])
def getContentDetail():
    """
    获取文章详情
    :return:
    """
    token = request.json.get('Token')
    userid = request.json.get('UserId')
    contentId = request.json.get('ContentId')

    if not kCheckUser(userId=userid, token=token):
        return kResponseJosn(code=500, codeString="无效Token")

    find_my_Conten = db.session.query(ContentModel).filter_by(ContentId=contentId).first()

    if not find_my_Conten:
        return kResponseJosn(code=400, codeString="查询失败！")

    find_my_user = db.session.query(UserDetailModel).filter_by(UserId=find_my_Conten.ReleasePeopleId).first()

    if not find_my_user:
        return kResponseJosn(code=400, codeString="查询失败！")

    find_attebon = db.session.query(AttebtonModel).filter_by(FollowersUserId=userid, B_FollowersUserId=find_my_Conten.ReleasePeopleId).first()

    dic = classTodic(find_my_Conten)
    dic["UserHeader"] = find_my_user.UserImageUrl
    dic["CompanyName"] = find_my_user.CompanyName
    dic["Name"] = find_my_user.Name
    if find_attebon:
        dic["IsAttebon"] = "1"
    else:
        dic["IsAttebon"] = "0"

    return kResponseJosn(code=200, codeString="查询成功！", obj=dic)


@main.route('/api/1.0/getMyContList', methods=['POST'])
def getMyContList():
    """
    获取用户的发布的文章
    :return:
    """

    page = request.json.get('Page')
    pageSize = request.json.get('PageSize')
    token = request.json.get('Token')
    userId = request.json.get('UserId')

    if not kCheckUser(userId=userId, token=token):
        return kResponseJosn(code=400, codeString="token 无效")

    """
     filter_by 查找
     order_by 排序
     paginate  分页
    """
    pagination = ContentModel.query \
        .filter_by(ReleasePeopleId=userId) \
        .order_by(ContentModel.ReleaseTime.desc()) \
        .paginate(int(page), per_page=int(pageSize), error_out=False)

    posts = pagination.items
    tList = []
    for t in posts:
        # obj = classTodic(t)
        obj = {
            "ContentTitle": t.ContentTitle,
            "ReleaseTime": t.ReleaseTime,
            "ContentId": t.ContentId,
            "Content": t.ContentString,
        }

        tList.append(obj)

    return kResponseJosn(code=200, codeString="查询成功！", obj=tList)


@main.route('/api/1.0/deleteContent', methods=['POST'])
def deleteContet():
    """
    删除文章
    :return:
    """

    token = request.json.get('Token')
    userId = request.json.get('UserId')
    contentId = request.json["ContentId"]
    if not kCheckUser(userId=userId, token=token):
        return kResponseJosn(code=400, codeString="token 无效")

    find_my_Conten = db.session.query(ContentModel).filter_by(ContentId=contentId).first()
    if not find_my_Conten:
        return kResponseJosn(code=400, codeString="查询失败！")

    db.session.delete(find_my_Conten)
    try:
        db.session.commit()
    except:
        pass
    db.session.close()
    return kResponseJosn(code=200, codeString="删除文章成功！")

