from drf_haystack.serializers import HaystackSerializer
from rest_framework.serializers import ModelSerializer

from goods.models import GoodsCategory, GoodsChannel, SKU
from goods.search_indexes import SKUIndex


class CategorySerializer(ModelSerializer):
    """ 类别序列化器 """
    class Meta:
        model = GoodsCategory

        fields = ('id','name')


class ChannelSerializer(ModelSerializer):
    """ 频道序列化器 """
    category = CategorySerializer()


    class Meta:
        model = GoodsChannel
        fields = ('category', 'url')

class SKUSerializer(ModelSerializer):
    '''序列化器序列化输出商品SKU信息'''

    class Meta:
        model = SKU
        # 输出：序列化的字段
        fields = ('id', 'name', 'price', 'default_image_url', 'comments')

class SKUIndexSerializer(HaystackSerializer):
    '''商品搜索的序列化器'''

    class Meta:

        #关联的索引类
        index_classes = [SKUIndex]
        # 索引类中的字段
        fields = [
            "text", "id", "name", "price", "default_image_url", "comments"
        ]