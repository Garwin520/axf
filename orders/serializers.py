from rest_framework  import serializers

from goods.serializers import GoodsSerializer
from .models import *

class OrderSerializer(serializers.ModelSerializer):

    class Meta:
        model = OrderModel
        fields = '__all__'

    def to_representation(self, instance):
        data = super().to_representation(instance)
        data['order_goods_info'] = OrderGoodsSerializer(instance.ordergoodsmodel_set.all(),many=True).data
        data['o_price'] = 20
        return data

class OrderGoodsSerializer(serializers.ModelSerializer):

    class Meta:
        model = OrderGoodsModel
        fields = '__all__'

    def to_representation(self, instance):
        data = super().to_representation(instance)
        data['o_goods'] = GoodsSerializer(instance.goods).data
        return data