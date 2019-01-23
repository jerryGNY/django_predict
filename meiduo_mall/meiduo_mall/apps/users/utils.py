from django.contrib.auth.backends import ModelBackend
from django.db.models import Q

from users.models import User
def jwt_response_payload_handler(token,user=None,request=None):
    '''
    自定义登陆成功响应数据，补充user_id和username
    :param token:
    :param users:
    :param request:
    :return:
    '''
    #返回到父类post方法里，已经封装成json字符串
    return {
        'user_id':user.id,
        'username':user.username,
        'token':token,

    }
#ModelBackend用户后台方法里认证登陆，在修改为手机号码认证
class UsernameMobileAuthBackend(ModelBackend):
    """自定义的认证后台: 支持使用手机号登录"""

    def authenticate(self, request, username=None, password=None, **kwargs):
        '''
        判断用户名（手机号）或者密码是否正确，返回对应的用户对象

        :param request:
        :param username:
        :param password:
        :param kwargs:
        :return:
        '''
        #username:输入的用户名或者手机号，Q对象,查询条件之间做逻辑运算
        #查询集有手机号或者用户名跟用户输入的符合
        query_set = User.objects.filter(Q(username=username) | Q(mobile=username))
        try:
            if query_set.exists():
                user = query_set.get()# 取出唯一的一条数据（取不到或者有多条数据都会出错）
                if user.check_password(password): # 进入一步判断密码是否正确
                    #返回user对象给前端用
                    return user

        except:
            #返回None就是没有
            return None