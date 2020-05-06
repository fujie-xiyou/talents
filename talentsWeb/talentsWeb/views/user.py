import re

from talentsWeb.models import User
from talentsWeb.utils.FPDecorator import request_decorator, login_decorator, dump_form_data
from talentsWeb.utils.FPExceptions import FormException


@request_decorator
@dump_form_data
def login(request, form_data):
    username = form_data.get('username')
    password = form_data.get('password')

    if not username:
        raise FormException("用户名为空")
    if not password:
        raise FormException('密码为空')
    try:
        db_user = User.objects.values().get(username=username)
    except User.DoesNotExist:
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

    db_user = User.objects.filter(username=username).all()
    if len(db_user) > 0:
        raise FormException('用户名已被使用')
    user = User(username=username, phone=phone, email=email, password=password)
    try:
        user.save()
        return "注册成功"
    except Exception as e:
        raise e


@request_decorator
@login_decorator
def myInfo(request):
    user = request.session.get('user')
    return user

