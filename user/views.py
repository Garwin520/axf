import uuid

from django.contrib.auth.hashers import make_password, check_password
from django.shortcuts import render
from rest_framework import status

from user.models import UserModel,UserTokenModel
from .serializers import *
# Create your views here.
from rest_framework.decorators import api_view
from rest_framework.response import Response


@api_view(['POST'])     #装饰器
def register(request):
    if request.method == 'POST':
        data = request.data
        serializer = UserRegisterSerializers(data=data)
        result = serializer.is_valid()
        if result:
            pwd1 = data.get('u_password')
            pwd2 = data.get('u_password2')
            if pwd1 != pwd2:
                res = {
                    'code':1002,
                    'msg':'密码和确认密码不一致'
                }
        else:
            res = {
                'code':1001,
                'msg':'校验失败',
                'data':serializer.errors
            }
            return Response(res)
        if UserModel.objects.filter(username=data.get('u_username')).exists() or\
                UserModel.objects.filter(email=data.get('u_email')).exists():
            res = {
                'code':1003,
                'msg':'账号或者邮箱已存在'
            }
            return Response(res)
        user = UserModel.objects.create(username=data.get('u_username'),password=make_password(data.get('u_password')),
                                        email=data.get('u_email'))
        res = {
            'code':200,
            'msg':'注册成功',
            'data':{
                'user_id':user.id
            }
        }
        return Response(res)
    else:
        pass
@api_view(['POST'])
def login(request):
    if request.method == 'POST':
        data = request.data
        serializer = UserLoginSerializer(data=data)
        if serializer.is_valid():
            user_by_username = UserModel.objects.filter(username=data.get('u_username')).first()
            user_by_email = UserModel.objects.filter(email=data.get('u_username')).first()
            if (not user_by_email) and (not user_by_username):
                res = {
                    'code':1005,
                    'msg':'登录账号不存在，请去注册'
                }
                return Response(res)

            if user_by_username:
                user = user_by_username
            else:
                user = user_by_email

            if not check_password(data.get('u_password'),user.password):
                res = {
                    'code':1006,
                    'msg':'登录密码错误，请重新输入密码'
                }
                return Response(res)
            token = uuid.uuid4().hex
            UserTokenModel.objects.create(token=token,user=user)
            res = {
                'code':200,
                'msg':'登录成功',
                'data':{
                    'token':token,
                }
            }
            return Response(res)
        else:
            res = {
                'code':1004,
                'msg':'登录账号或密码不符合规则，请重新输入'
            }
            return Response(res)

@api_view(['GET'])
def user_info(request):
    if request.method == 'GET':
        # 1. 获取前段传过来的登录标识符token
        token = request.query_params.get('token')
        user_token = UserTokenModel.objects.filter(token=token).first()
        if user_token:
            username = user_token.user.username
            res = {
                'code':200,
                'msg':'请求成功',
                'data':{
                    'user_info':{
                        'u_username':username
                    },
                    'orders_not_pay_num':0,
                    'orders_not_send_num':0,
                }
            }
            return Response(res)
        else:
            res = {
                'msg':'服务端没有相应的token值'
            }
            return Response(res,status=status.HTTP_401_UNAUTHORIZED)    #状态码401