# Create your views here.
import logging

from django_redis import get_redis_connection
from rest_framework.exceptions import ValidationError
from rest_framework.response import Response
from rest_framework.views import APIView
from celery_tasks.sms.tasks import send_sms_code
#生成短信验证码用日志记录

logger = logging.getLogger('django')


class SmsCodeView(APIView):
    #发送短信验证码

    #  /sms_codes/(?P<mobile>1[3-9]\d{9})/
    def get(self,requenst,mobile):

        # 4.判断是否重复发送短信验证码
        #获取对象，sms_codes是在配置文件设置的
        strict_redis = get_redis_connection('sms_codes')  # type : StrictRedis
        #从redis获取标识，redis.get(键)就是在获取值
        send_flag = strict_redis.get('sms_flag_%s'%mobile)
        #没有的话是None
        print(send_flag)
        if send_flag:#60秒内还存在
            # return Response({'message':'禁止重复发送短信验证码'},status=400)
            raise ValidationError({'message':'禁止重复发送短信验证码'}) # status=400

        # 1.生成短信验证码 不够把0补全
        import random
        sms_code = '%06d' %random.randint(0,999999)
        logger.info('获取短信验证码：%s' %sms_code)

        # 2使用云联通来发送短信验证码
        # [sms_code, 5]  [短信验证码， 有效期]   1表示id为1的短信测试模板，项目上线换成自己的模板id


        #返回值0就是成功，-1就是不成功
        # print(CCP().send_template_sms(mobile, [sms_code, 5], 1))
        # sleep(5)
        #使用delay发送短信：保存函数名，函数参数,任务标识等redis中，主要是做异步
        # send_sms_code(mobile, sms_code)
        send_sms_code.delay(mobile,sms_code)

        # 3保存短信验证码

        #sms_codes 在redis配置中设置的，连接到redis数据库，取得sms_codes

        # sms_13600000001       111111     (验证码 1分钟过期)
        # sms_13600000002       222222     (验证码 1分钟过期)
        # send_flag_13600000001      1     （发送标识：1分钟过期）
        # send_flag_13600000002      1     （发送标识：1分钟过期）
        #设置短信验证码到redis数据库，同时设置标识
        # strict_redis.setex('sms_%s'%mobile,60*5,sms_code)
        # strict_redis.setex('sms_flag_%s'%mobile,60,1)
        #
        #

        '''使用管道'''
        pipeline = strict_redis.pipeline()
        #验证码只保存5分钟，失效后得重新发
        #验证标识60秒
        pipeline.setex('sms_%s'%mobile,60*5,sms_code)
        pipeline.setex('sms_flag_%s'%mobile,60,1)
        result = pipeline.execute()
        #是一个列表，传输成功就true，否则就是false
        print(result)

        # 5.响应数据
        return Response({'message': 'OK'})