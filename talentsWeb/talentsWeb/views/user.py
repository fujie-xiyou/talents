import re
from talentsWeb.utils.FPDecorator import request_decorator, login_decorator, dump_form_data
from talentsWeb.utils.FPExceptions import FormException
from talentsWeb.settings import db

user_col = db["user"]


@request_decorator
@dump_form_data
def login(request, form_data):
    username = form_data.get('username')
    password = form_data.get('password')

    if not username:
        raise FormException("用户名为空")
    if not password:
        raise FormException('密码为空')
    db_user = user_col.find_one({"username": username}, {"_id": 0})
    if not db_user:
        raise FormException('用户不存在')
    if db_user.get('password') != password:
        raise FormException('密码错误')
    del db_user['password']
    request.session['user'] = db_user
    return "登录成功"


@request_decorator
@dump_form_data
def register(request, form_data):
    username = form_data.get('username')
    if not username or len(username) < 3 or len(username) > 10:
        raise FormException('用户名不合法')

    password = form_data.get('password')
    if not password or len(password) < 6 or len(password) > 50:
        raise FormException('密码不合法')

    phone = form_data.get('phone')
    if not phone or not re.match(r'^[1]([3-9])[0-9]{9}$', phone):
        raise FormException('手机号不合法')

    email = form_data.get('email')
    if not email or not re.match(r'^[A-Za-z0-9\u4e00-\u9fa5.\-_]+@[a-zA-Z0-9_-]+(\.[a-zA-Z0-9_-]+)+$', email):
        raise FormException('邮箱不合法')

    db_user_count = user_col.count_documents({"username": username})
    if db_user_count > 0:
        raise FormException('用户名已被使用')
    user_col.insert_one(form_data)
    return "注册成功"


@request_decorator
@login_decorator
def myInfo(request):
    user = request.session.get('user')
    return user


@request_decorator
@login_decorator
def logout(request):
    request.session.clear()
    return "注销成功"


@request_decorator
@login_decorator
@dump_form_data
def update(request, form_data):
    new_user = {}
    username = form_data.get('username')
    if not username or len(username) < 3 or len(username) > 10:
        raise FormException('用户名不合法')
    new_user["username"] = username
    password = form_data.get('password')

    if password and (len(password) < 6 or len(password) > 50):
        raise FormException('密码不合法')
    if password:
        new_user["password"] = password
    phone = form_data.get('phone')
    if not phone or not re.match(r'^[1]([3-9])[0-9]{9}$', phone):
        raise FormException('手机号不合法')
    new_user["phone"] = phone
    email = form_data.get('email')
    if not email or not re.match(r'^[A-Za-z0-9\u4e00-\u9fa5.\-_]+@[a-zA-Z0-9_-]+(\.[a-zA-Z0-9_-]+)+$', email):
        raise FormException('邮箱不合法')
    new_user["email"] = email
    db_user_count = user_col.count_documents({"username": username})
    if db_user_count > 0:
        raise FormException('用户名已被使用')
    old_username = request.session.get("user").get("username")
    user_col.update({"username": old_username}, {"$set": new_user})
    db_user = user_col.find_one({"username": username}, {"_id": 0})
    del db_user['password']
    request.session['user'] = db_user

    return "修改成功"
