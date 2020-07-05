from rest_framework import serializers

class UserRegisterSerializers(serializers.Serializer):

    u_username = serializers.CharField(required=True,max_length=10,min_length=5,
                                       error_messages={
                                           'max_length':'账号长度超过10字符，请修改账号',
                                           'min_length':'账号长度短于5字符，请修改账号',
                                       })
    u_password = serializers.CharField(required=True,max_length=10,min_length=5,
                                       error_messages={
                                           'max_length': '注册密码长度超过10字符，请修改密码',
                                           'min_length': '注册密码长度短于5字符，请修改密码',
                                       })
    u_password2 = serializers.CharField(required=True, max_length=10, min_length=5,
                                       error_messages={
                                           'max_length': '注册密码长度超过10字符，请修改密码',
                                           'min_length': '注册密码长度短于5字符，请修改密码',
                                       })
    u_email = serializers.CharField(required=True)

class UserLoginSerializer(serializers.Serializer):
    u_username = serializers.CharField(required=True, max_length=10, min_length=5,
                                       error_messages={
                                           'max_length': '登录账号长度超过10字符',
                                           'min_length': '登录账号长度短于5字符',
                                       })
    u_password = serializers.CharField(required=True, max_length=10, min_length=5,
                                       error_messages={
                                           'max_length': '登录密码长度超过10字符',
                                           'min_length': '登录密码长度短于5字符',
                                       })