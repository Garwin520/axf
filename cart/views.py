from django.shortcuts import render

# Create your views here.
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response

from goods.serializers import GoodsSerializer
from .models import *
from user.models import UserTokenModel
from .serializers import CartsSerializer


@api_view(['GET'])
def cart(request):
    if request.method == 'GET':
        token = request.GET.get('token')
        user_token = UserTokenModel.objects.filter(token=token).first()
        if not user_token:
            res = {
                'code':1008,
                'msg':'用户没有登录，无法查询购物车数据'
            }
            return Response(res)
        carts = CartModel.objects.filter(user=user_token.user)
        carts = CartsSerializer(carts,many=True).data
        total_price = 0
        for cart in carts:
            if cart['is_select']:
                total_price += cart['c_goods']['price'] * cart['c_num']
        res = {
            'code':200,
            'msg':'请求成功',
            'data':{
                'carts':carts,
                'total_price':'%.2f'%total_price,
            }
        }
        return Response(res)

@api_view(['POST'])
def add_cart(request):
    if request.method == 'POST':
        token = request.data.get('token')
        goodsid = request.data.get('goodsid')
        user_token = UserTokenModel.objects.filter(token=token).first()
        if user_token:
            cart = CartModel.objects.filter(goods_id=goodsid,user=user_token.user).first()
            if cart:
                cart.c_num += 1
                cart.save()
                # c_num = cart.c_num+1
                # CartModel.objects.filter(goods_id=goodsid,user=user_token.user).update(c_num=c_num)
            else:
                CartModel.objects.create(user=user_token.user,goods_id=goodsid)
            res = {
                'code':200,
                'msg':'当前商品加入购物车成功'
            }
            return Response(res)
        else:
            res = {
                'code':1007,
                'msg':'用户没有登录，请登录后再执行此操作'
            }
            return Response(res)

@api_view(['PATCH'])
def cart_select(request,id):
    if request.method == 'PATCH':
        goods_select = CartModel.objects.get(id=id)
        goods_select.is_select = not goods_select.is_select
        goods_select.save()
        res = {
            'code':200,
            'msg':'patch请求',
            'data':{

            }
        }
        return Response(res)

@api_view(['PATCH'])
def select_all(request):
    if request.method == 'PATCH':
        token = request.data.get('token')
        user_token = UserTokenModel.objects.filter(token=token).first()
        if CartModel.objects.filter(is_select=False).exists():
            select = True
        else:
            select = False
        CartModel.objects.filter(user=user_token.user).update(is_select=select)
        res = {
            'code': 200,
            'msg': 'patch请求',
            'data':{
                "select":select,
            }
        }
        return Response(res)

@api_view(['POST'])
def sub_cart(request):
    if request.method == 'POST':
        token = request.data.get('token')
        goods_id = request.data.get('goodsid')
        user_token = UserTokenModel.objects.filter(token=token).first()
        if user_token:
            cart = CartModel.objects.filter(goods_id=goods_id,user=user_token.user).first()
            cart.c_num -= 1
            cart.save()
            if cart.c_num <= 0:
                CartModel.objects.filter(goods_id=goods_id,user=user_token.user).delete()
            res = {
                'code': 200,
                'msg': 'post请求',
            }
            return Response(res)