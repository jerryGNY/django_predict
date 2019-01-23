from alipay import AliPay
from django.conf import settings
from django.shortcuts import render
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from orders.models import OrderInfo


class PaymentView(APIView):
    """支付接口"""

    permission_classes = (IsAuthenticated,)

    # GET /orders/(?P<order_id>\d+)/payment/
    def get(self, request, order_id):

        # 获取订单对象，判断订单信息是否正确
        try:
            order = OrderInfo.objects.get(order_id=order_id,
                                          user=request.user,  # 当前登录用户的订单
                                          pay_method=OrderInfo.PAY_METHODS_ENUM.get('ALIPAY'),  # 订单为阿里支付
                                          status=OrderInfo.ORDER_STATUS_ENUM.get('UNPAID'))  # 未支付的订单
        except OrderInfo.DoesNotExist:
            return Response({'message': '无效的订单'}, status=400)

        # 读取rsa密钥
        app_private_key_string = open("meiduo_mall/apps/payment/keys/app_private_key.pem").read()
        alipay_public_key_string = open("meiduo_mall/apps/payment/keys/alipay_public_key.pem").read()

        print(app_private_key_string)
        print(alipay_public_key_string)
        print(settings.ALIPAY_APPID)

        # 创建第三方sdk的 AliPay 支付对象
        alipay = AliPay(
            appid=settings.ALIPAY_APPID,
            # 默认回调url: 接收接收结果参数,没有
            app_notify_url='http://www.meiduo.site:8080/pay_success.html',
            app_private_key_string=app_private_key_string,
            # 支付宝的公钥，验证支付宝回传消息使用，不是你自己的公钥,
            alipay_public_key_string=alipay_public_key_string,
            sign_type="RSA2",  # RSA 或者 RSA2
            debug=False)

        # 调用AliPay 支付对象的支付方法api_alipay_trade_page_pay，发起支付请求
        order_string = alipay.api_alipay_trade_page_pay(
            out_trade_no=order_id,
            total_amount=str(order.total_amount),  # [注意]: 必须要传递字符串
            subject='美多订单: %s' % order_id,
            return_url="http://www.meiduo.site:8080/pay_success.html",
            notify_url="http://www.meiduo.site:8080/pay_success.html")

        # 需要跳转到：https://openapi.alipay.com/gateway.do? + order_string
        alipay_url = settings.ALIPAY_URL + '?' + order_string

        # 拼接链接返回前端
        return Response({'alipay_url': alipay_url})
