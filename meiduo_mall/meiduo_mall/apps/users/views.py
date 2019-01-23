from django.conf import settings
from django.shortcuts import render

# Create your views here.
from django.views import View

# /test/
from django_redis import get_redis_connection
from itsdangerous import TimedJSONWebSignatureSerializer
from rest_framework.generics import CreateAPIView, RetrieveAPIView, UpdateAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_jwt.views import ObtainJSONWebToken

from carts.utils import merge_cart_cookie_to_redis
from goods.models import SKU
from goods.serializers import SKUSerializer
from users.models import User
from users.serializers import CreateUserSerializer, UserDetailSerializer, EmailSerializer, AddBrowseHistorySerializer


class TestView(View):

    def get(self,request):
        return render(request, 'test.html')

# /test2/
class TestView2(APIView):

    def get(self, request):
        response = Response({'message': 'get请求'})
        # 添加响应头数据
        # response['Access-Control-Allow-Origin'] = 'http://127.0.0.1:8080'
        # response['Access-Control-Allow-Origin'] = 'http://www.meiduo.site:8080'
        return response


    def post(self, request):
        response = Response({'message': 'post请求'})
        # 添加响应头数据
        # response['Access-Control-Allow-Origin'] = 'http://127.0.0.1:8080'
        return response


# class UsernameCountView(APIView):
#
# # `usernames/(?P<username>\w{5,20})/count/
#
#     def get(self,request,username):
#
#         #查询数据：获取用户名的个数QuerySet
#         count = User.

#不涉及数据库的增删该，用APIView父类就行
class UsernameCountView(APIView):

    # usernames/(?P<username>\w{5,20})/count/
    def get(self,request,username):

        #查询数据：获取用户名的个数 QuerySet
        #是查询集，可以用count
        count = User.objects.filter(username=username).count()
        #要返回用户名和个数给前端校验
        context ={
            'username':username,
            'count':count
        }
        return Response(context)

#继承的是GenericAPIView CreateModelMixin---其他子类
class CreateUserView(CreateAPIView):
    #新增不用查询,直接指定序列化器
    # queryset = User.objects.all()

    #返回user对象，.data获取对象

    # return Response(serializer.data)--已经封装号
    serializer_class = CreateUserSerializer

class MyObtainJSONWebToken(ObtainJSONWebToken):
    '''登陆接口'''

    def post(self, request, *args, **kwargs):
        """登录接口"""
        response = super().post(request, *args, **kwargs)

        # 仿照drf jwt扩展对于用户登录的认证方式，判断用户是否认证登录成功
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid(): # true: 表示用户名和密码正确, 如果用户登录认证成功，则合并购物车

            # serializer: JSONWebTokenSerializer
            # 序列化器校验通过后返回了登录成功的user对象
            # 还没有登陆，刚开始是控制user = request.user                            # error
            user = serializer.validated_data.get('user')  # ok
            # 合并购物车商品
            merge_cart_cookie_to_redis(request, response, user)

        return response

class UserDetailView(RetrieveAPIView):

    # queryset = User.objects.all()

    serializer_class = UserDetailSerializer

    # 登录后才能调用此接口
    permission_classes = [IsAuthenticated]
    #get_object已经实现了查询user功能，可以直接返回对象,只是要一个对象
    def get_object(self):
        #返回当前登陆的用户对象
        return self.request.user


#/email/
#UpdateAPIView是其他子类
class EmailView(UpdateAPIView):
    """
       修改用户邮箱（修改用户的邮箱字段）
    """
    #因为自带get_objext,所以不用查询
    #权限验证
    permission_classes = [IsAuthenticated]
    serializer_class = EmailSerializer

    # 重写GenericAPIView的方法，指定要修改的是哪一条用户数据
    def get_object(self):
        #序列化器已经指明哪个表
        return self.request.user


# GET /email/verification/?token=xxx
class VerifyEmailView(APIView):
    '''激活用户邮箱'''

    def get(self,request):
        # 1,获取请求参数：token
        token = request.query_params.get('token')

        # 2. 校验token合法性
        # {'user_id': 'xx', 'email': 'xxx'}
        if not token:
            return Response({'message':'缺少token参数'},status=400)

        try:
            s = TimedJSONWebSignatureSerializer(settings.SECRET_KEY)
            dict_data = s.loads(token) # 返回字典

        except:
            return Response({'message':'缺少token参数'}, status=400)


        # 3. 从token中获取： user_id, email
        user_id = dict_data.get('user_id')
        email = dict_data.get('email')


        # 4. 查询出要激活的用户对象
        try:
            #查id=user_id即可，但是为了更精确，可以一起查email
            user = User.objects.get(id=user_id, email=email)

        except:
            return Response({'message': '用户不存在'}, status=400)

        # 5. 修改用户对象的激活字段为true:  email_active=True
        user.email_active = True
        user.save()

        # 6. 响应数据： {'message': 'ok'}
        return Response({'message': 'ok'})


class BrowseHistoryView(CreateAPIView):
    '''
    用户浏览记录
    11保存用户浏览记录
    2.查询用户浏览记录
    '''
    #登陆才能查看
    permission_classes = [IsAuthenticated]
    serializer_class = AddBrowseHistorySerializer


    # GET /browser_histories/
    def get(self,request):
        '''查询用户浏览记录
        '''

        # history_1 =  [2, 1, 3]
        # 获取用户id

        user_id = request.user.id

        # 获取商品id
        strict_redis = get_redis_connection('history')  # type: StrictRedis
        sku_ids = strict_redis.lrange('history_%s' % user_id, 0, -1)

        # 从mysql中查询商品详情信息 (QuerySet)
        # SKU.objects.filter(id__in=[2,1,3])
        # SKU.objects.filter(id__in=sku_ids)   # 元素: bytes

        skus =[]
        for sku_id in sku_ids:
            sku = SKU.objects.get(id=int(sku_id))  # bytes -> int
            skus.append(sku)

            # 序列化商品数据, 返回商品数据,instance指定字段
        s = SKUSerializer(instance=skus, many=True)
        # s.data  # 列表数据

        # 响应数据
        return Response(s.data)