from QQLoginTool.QQtool import OAuthQQ
from django.conf import settings
from django.shortcuts import render

# Create your views here.

from rest_framework.response import Response
from rest_framework.views import APIView

from carts.utils import merge_cart_cookie_to_redis
from ouath.models import OAuthQQUser
from ouath.serializers import QQUserSerializer
from ouath.utils import generate_encrypted_openid


class QQURLView(APIView):
    #显示qq登陆页面
    def get(self,request):
    #获取回调页
    # /oauth/qq/authorization/?next=xxx

    # next = request.GET.get()
    #获取url地址参数
        next = request.query_params.get('next')

    # 创建第三方sdk OAuthQQ对象

        oauth = OAuthQQ(client_id=settings.QQ_CLIENT_ID,
                        client_secret=settings.QQ_CLIENT_SECRET,
                        redirect_uri=settings.QQ_REDIRECT_URI, # 登录成功的回调地址
                        state=next)   # 登录成功进入的界面地址，比如： /index_backup.html


        #通过这个对象可以获取QQ登陆界面的url地址
        login_url = oauth.get_qq_url()
        #json格式
        return Response({
            'login_url':login_url
        })


class QQUserView(APIView):


    # GET /oauth/qq/user/?code=xxx
    def get(self,request):
        """QQ认证接口"""

        # 1. 获取请求参数：code
        # code = request.GET.get('code')
        code = request.query_params.get('code')
        # print(code)
        # 2. 校验code参数
        if not code:
            return Response({'message':'code不能为空'},status=400)

        # 创建第三方sdk OAuthQQ对象,在上一个类中不能用，所以要自己在创建，里面封装了方法
        oauth = OAuthQQ(client_id=settings.QQ_CLIENT_ID,
                        client_secret=settings.QQ_CLIENT_SECRET,
                        redirect_uri=settings.QQ_REDIRECT_URI)  # 登录成功进入的界面地址，比如： /index_backup.html

        try:
            #3.使用QQ登陆sdk，通过code获取 access_token

            access_token = oauth.get_access_token(code)

            # 4. 使用QQ登录sdk， 通过 access_token 获取 openid
            openid = oauth.get_open_id(access_token)
            print(openid)

        except:
            return Response({'message': 'QQ服务器出错'}, status=500)

        # 5. 根据openid，从映射表中查询绑定的美多用户对象
        try:
            qquser = OAuthQQUser.objects.get(openid=openid)

        except OAuthQQUser.DoesNotExist:
        # - 查询不到美多用户，说明是第一次使用QQ登录，则返回openid, 等待后续用户的绑定操作
        # 使用itdangerous签名openid后,再响应给客户端
            openid = generate_encrypted_openid(openid)
            return Response({'openid': openid})

        else:
            # - 能查询到美多用户，则生成并响应：jwt，user_id, username，完成QQ登录流程
            user = qquser.user  # 绑定openid绑定的美多用户对象

            # 生成jwt
            from rest_framework_jwt.settings import api_settings
            jwt_payload_handler = api_settings.JWT_PAYLOAD_HANDLER  # 生payload部分的方法(函数)
            jwt_encode_handler = api_settings.JWT_ENCODE_HANDLER  # 生成jwt的方法(函数)

            payload = jwt_payload_handler(user)  # 生成payload, 得到字典
            token = jwt_encode_handler(payload)  # 生成jwt字符串

            #响应数据
            context = {
                #在前已经加了token属性
                'token': token,
                'user_id': user.id,
                'username': user.username
            }
            response = Response(context)
            #合并购物车商品

            merge_cart_cookie_to_redis(request, response, user)
            return Response(context)


    # POST /oauth/qq/user/  是以表单方式
    def post(self,request):

        # 1. 创建序列化器,表单形式--requesnt.data
        s = QQUserSerializer(data=request.data)

        # 2. 校验请求参数是否合法: serializer.is_valid()
        s.is_valid(raise_exception=True)

        # 3. 绑定openid与美多用户:  serializer.save()   -> serializer.create()
        #创建绑定的梅朵用户对象并且返回
        user = s.save()  # 返回绑定的美多用户对象


        # 4. 生成并响应 jwt, user_id, username，完成QQ登录
        # 生成jwt
        from rest_framework_jwt.settings import api_settings
        jwt_payload_handler = api_settings.JWT_PAYLOAD_HANDLER  # 生payload部分的方法(函数)
        jwt_encode_handler = api_settings.JWT_ENCODE_HANDLER  # 生成jwt的方法(函数)

        payload = jwt_payload_handler(user)  # 生成payload, 得到字典
        token = jwt_encode_handler(payload)  # 生成jwt字符串

        # 响应数据
        context = {
            'token': token,
            'user_id': user.id,
            'username': user.username
        }

        response = Response(context)
        # 合并购物车商品
        merge_cart_cookie_to_redis(request, response, user)
        return Response(context)
