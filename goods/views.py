from django.shortcuts import render
from .serializers import *

# Create your views here.
from .models import *
from rest_framework.decorators import api_view
from rest_framework.response import Response


@api_view(['GET'])
def home(request):
    if request.method == 'GET':
        main_wheels = MainWheelSerializer(MainWheel.objects.all(),many=True).data
        main_navs = MainNavsSerializer(MainNav.objects.all(),many=True).data
        main_show = MainShowSerializer(MainShow.objects.all(),many=True).data
        res = {
            'code':200,
            'msg':'请求成功',
            'data':{
                'main_wheels':main_wheels,
                'main_navs':main_navs,
                'main_shows':main_show,
            }
        }
        return Response(res)

@api_view(['GET'])
def food_type(request):
    if request.method == 'GET':
        food_types = FoodType.objects.all()
        data = FoodTypeSerializer(food_types,many=True).data
        res = {
            'code': 200,
            'msg': '请求成功',
            'data':data,
        }
        return Response(res)
    pass

@api_view(['GET'])
def market(request):
    if request.method == 'GET':
        typeid = request.query_params.get('typeid')
        childcid = request.GET.get('childcid')
        order_rule = int(request.GET.get('order_rule'))
        if childcid == '0':
            goods = Goods.objects.filter(categoryid=typeid).all()
        else:
            goods = Goods.objects.filter(categoryid=typeid,childcid=childcid).all()
        sort_list = ['price','-price','productnum','-productnum']
        if order_rule != 0:
            goods = goods.order_by('%s'%sort_list[order_rule-1])
        goods_list = GoodsSerializer(goods,many=True).data
        food_type = FoodType.objects.filter(typeid=typeid).first()
        foodtype_childname_list = [{'child_value':i.split(':')[1],'child_name':i.split(':')[0]} for i in food_type.childtypenames.split('#')]
        order_rule_list = [{'order_value':'1','order_name':'价格升序'},{'order_value':'2','order_name':'价格降序'},
                            {'order_value': '3', 'order_name': '销量升序'},{'order_value':'4','order_name':'销量降序'},]
        res = {
            'code':200,
            'msg':'请求成功',
            'data':{
                'goods_list':goods_list,
                'order_rule_list':order_rule_list,
                'foodtype_childname_list':foodtype_childname_list,
            }
        }
        return Response(res)