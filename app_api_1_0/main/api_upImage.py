
import os, time
from flask import request, send_from_directory, url_for, Response
from werkzeug.utils import secure_filename
from config import basedir
from . import main
from app_api_1_0.main.user_help import kCheckUser
from libs.api_extended import kResponseJosn
from app_api_1_0 import db
from app_api_1_0.models import UserDetailModel


ALLOWED_EXTENSIONS = set(['txt', 'png', 'jpg', 'xls', 'JPG', 'PNG', 'xlsx', 'gif', 'GIF'])  # 允许上传的文件后缀


def allowed_file(filename):
    # 判断文件的扩展名是否在配置项ALLOWED_EXTENSIONS中
    return '.' in filename and \
           filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS


@main.route('/api/1.0/upContentImage', methods=['POST'])
def up():
    """
    上传发布文章的图片
    :return:
    """
    file_dir = os.path.join(basedir, "app_api_1_0/static")  # 拼接成合法文件夹地址

    if not os.path.exists(file_dir):
        os.makedirs(file_dir)  # 文件夹不存在就创建
    if 'file' not in request.files:
        return kResponseJosn(code=500, codeString="No file part")

    file = request.files['file']

    if file and allowed_file(file.filename):

        filename = secure_filename(file.filename)

        ext = filename.rsplit('.', 1)[1]  # 获取文件后缀
        unix_time = int(time.time())
        new_filename = "Content" + str(unix_time) + '.' + ext  # 修改文件名

        file.save(os.path.join(file_dir, new_filename))  # 保存文件到upload目录
        img_url = url_for("static", _external=True, filename=new_filename)

        print("----文件地址=", img_url)
        return kResponseJosn(code=200, codeString="上传成功", obj=img_url)

    return kResponseJosn(code=500, codeString="上传失败")


@main.route('/api/1.0/upUserImage', methods=['POST'])
def upImage():
    """
    上传用户头像
    :return:
    """
    file_dir = os.path.join(basedir, "app_api_1_0/static")  # 拼接成合法文件夹地址

    if not os.path.exists(file_dir):
        os.makedirs(file_dir)  # 文件夹不存在就创建

    token = request.form["Token"]
    userid = request.form["UserId"]

    if not kCheckUser(userId=userid, token=token):
        return kResponseJosn(code=500, codeString="token 无效！")

    # 检查post请求是否含有文件
    if 'file' not in request.files:
        return kResponseJosn(code=500, codeString="No file part")

    find_my_user = db.session.query(UserDetailModel).filter_by(UserId=userid).first()  # 查询第一个
    if not find_my_user:
         return kResponseJosn(code=500, codeString="no find user")

    file = request.files['file']
    # 浏览器也会提交没有文件名的空部分 如果用户没有选择文件
    if file and allowed_file(file.filename):

        filename = secure_filename(file.filename)

        ext = filename.rsplit('.', 1)[1]  # 获取文件后缀
        unix_time = int(time.time())
        new_filename = userid + str(unix_time) + '.' + ext  # 修改文件名

        file.save(os.path.join(file_dir, new_filename))  # 保存文件到upload目录
        # 返回服务器的图片地址
        img_url = url_for("static", _external=True, filename=new_filename)

        print("----文件地址=", img_url)
        find_my_user.UserImageUrl = img_url
        db.session.add(find_my_user)
        try:
            db.session.commit()
        except:
            db.session.rollback()
        db.session.close()

        return kResponseJosn(code=200, codeString="上传成功！")

    return kResponseJosn(code=500, codeString="errors")

    # 检查文件类型是否合法





