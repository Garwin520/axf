from rest_framework  import serializers
from cart.models import *
from goods.serializers import GoodsSerializer

class CartsSerializer(serializers.ModelSerializer):

    class Meta:
        model = CartModel
        fields = '__all__'

    def to_representation(self, instance):
        data = super().to_representation(instance)
        data['c_goods'] = GoodsSerializer(instance.goods).data
        return data
