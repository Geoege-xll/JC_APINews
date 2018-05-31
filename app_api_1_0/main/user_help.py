
from app_api_1_0.models import UserModel
from app_api_1_0 import db


def kCheckUser(userId, token):
    """
    验证用户信息是否有效
    :param USERCLASS: 绑定用户的Class类
    :param UserId: 用户id
    :param token:  token
    :return:
    """

    if userId is None or token is None:
        return False
    find_my_user = db.session.query(UserModel).filter_by(UserId=userId).first()  # 查询第一个

    if find_my_user is None:
        return False

    # 判断user数据库存的token和参数的tokon 是否一致 不一致被挤下来了
    print("数据库存储的token：", find_my_user.Token)
    if find_my_user.Token == token:
        return True
    #     print("token 是否有效：", certify_token(key=token_key, token=token))
        # 暂时隐藏token的校验
        # if certify_token(key=token_key, token=token) == True:
        #     return True

    return False