import uuid

# Create your views here.
from rest_framework.decorators import api_view
from rest_framework.response import Response

from .serializers import OrderGoodsSerializer, OrderSerializer
from cart.models import CartModel
from .models import OrderModel, OrderGoodsModel
from user.models import UserTokenModel


@api_view(['GET','POST'])
def orders(request):
    if request.method == 'GET':
        token = request.GET.get('token')
        o_status = request.GET.get('o_status')
        user_token = UserTokenModel.objects.filter(token=token).first()
        orders = OrderModel.objects.filter(user=user_token.user).all()
        order_data = OrderSerializer(orders,many=True).data
        print(order_data)
        res = {
            'code':200,
            'data':order_data,
            'msg':'GET请求',
        }
        return Response(res)
    elif request.method == 'POST':
        token = request.data.get('token')
        user_token = UserTokenModel.objects.filter(token=token).first()
        if not user_token:
            res = {
                'code':1010,
                'msg':'请先登录再执行此操作'
            }
            return Response(res)
        carts = CartModel.objects.filter(user=user_token.user,is_select=True).all()
        if carts.first():
            o_num = uuid.uuid4().hex
            order = OrderModel.objects.create(user=user_token.user, o_num=o_num)
            for cart in carts:
                OrderGoodsModel.objects.create(goods=cart.goods, order=order,goods_num=cart.c_num)
                cart.delete()

            res = {
                'code':200,
                'msg':'POST请求'
            }
            return Response(res)
        else:
            res = {
                'code':1009,
                'msg':'请选择购物车商品再下单',
            }
            return Response(res)