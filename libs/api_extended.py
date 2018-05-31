import base64
import hmac
import time
from sqlalchemy.ext.declarative import DeclarativeMeta
import json
import datetime
from flask import jsonify
import random
import string
from sqlalchemy.orm import class_mapper


token_key = "JD98Dskw=23njQndW9D"
x = "AaBbCcDdEeFfGgHhIiJjKkLlMmNnOoPpQqRrSsTtUuVvWwXxYyZz0123456789"


def singlerandom(number):
    r'''
    此函数的作用为生成number位不重复的随机字符串，number最大为62
    :param number: 生成的位数
    :return:
    '''
    stringy = ''.join(random.sample(x, number)).replace(' ', '')
    return stringy


def couplerandom(number):
    r'''
    此函数的作用为生成number位可重复的随机字符串，number没有上限
    :param number: 生成的位数
    :return:
    '''
    stringx = ''.join(random.choice(x) for i in range(number))
    return stringx

def couplerandom2(number):
    r'''
    此函数的作用为生成number位随机字符串，number没有上限
    :param number: 生成的位数
    :return:
    '''
    cont = ''.join(random.sample(string.ascii_letters + string.digits, number))
    return cont


def classTodic(model):
  """
   将orm sqlalchemy 查询出来的class对象转成 dic
  """
  # first we get the names of all the columns on your model
  columns = [c.key for c in class_mapper(model.__class__).columns]
  # then we return their values in a dict
  return dict((c, getattr(model, c)) for c in columns)



def generate_token(key, expire=3600):
    r''' 生成token
        @Args:
            key: str (用户给定的key，需要用户保存以便之后验证token,每次产生token时的key 都可以是同一个key)
            expire: int(最大有效时间，单位为s)
        @Return:
            state: str
    '''
    ts_str = str(time.time() + expire)
    ts_byte = ts_str.encode("utf-8")
    sha1_tshexstr  = hmac.new(key.encode("utf-8"),ts_byte,'sha1').hexdigest()
    token = ts_str+':'+sha1_tshexstr
    b64_token = base64.urlsafe_b64encode(token.encode("utf-8"))
    return b64_token.decode("utf-8")



def certify_token(key, token):
    r''' 验证token
        @Args:
            key: str
            token: str
        @Returns:
            boolean
    '''
    token_str = base64.urlsafe_b64decode(token).decode('utf-8')
    token_list = token_str.split(':')
    if len(token_list) != 2:
        return False
    ts_str = token_list[0]
    if float(ts_str) < time.time():
        # token expired
        return False
    known_sha1_tsstr = token_list[1]
    sha1 = hmac.new(key.encode("utf-8"),ts_str.encode('utf-8'),'sha1')
    calc_sha1_tsstr = sha1.hexdigest()
    if calc_sha1_tsstr != known_sha1_tsstr:
        # token certification failed
        return False
    # token certification success
    return True
#
def kResponseJosn(code,codeString="",obj=""):
    r''' 固定返回json 格式

    :param code: 返回码
    :param codeString: 描述
    :param obj: 数据
    :return: 返回json
    '''
    return jsonify({"Code": code,
             "CodeString": codeString,
             "CodeData": obj
             })



# 对mysql的查询出来的结果进行json处理  使用的
# c = YourAlchemyClass()
# print json.dumps(c, cls=AlchemyEncoder)
class AlchemyEncoder(json.JSONEncoder):

    def default(self, obj):

        if isinstance(obj.__class__, DeclarativeMeta):
            # an SQLAlchemy class
            fieldsDic = {}
            for field in [x for x in dir(obj) if not x.startswith('_') and x != 'metadata']:
                data = obj.__getattribute__(field)
                try:
                    json.dumps(data)     # this will fail on non-encodable values, like other classes
                    fieldsDic[field] = data
                except TypeError:    # 添加了对datetime的处理
                    if isinstance(data, datetime.datetime):
                        fieldsDic[field] = data.isoformat()
                    elif isinstance(data, datetime.date):
                        fieldsDic[field] = data.isoformat()
                    elif isinstance(data, datetime.timedelta):
                        fieldsDic[field] = (datetime.datetime.min + data).time().isoformat()
                    else:
                        fieldsDic[field] = None
            # a json-encodable dict
            return fieldsDic

        return json.JSONEncoder.default(self, obj)





